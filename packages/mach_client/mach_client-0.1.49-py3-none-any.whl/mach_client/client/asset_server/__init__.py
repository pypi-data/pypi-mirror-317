from __future__ import annotations
import asyncio
from decimal import Decimal
import itertools
import logging
from typing import Any, Optional

from aiohttp import ClientSession
import cachebox
from cachebox import Cache
from pydantic import TypeAdapter

from ... import config
from ...account import AccountBase, AccountIDManager
from ...asset import Token
from ...chain import Chain, SupportedChain
from ...chain_client import ChainClient
from ...log import LogContextAdapter, Logger
from .. import utility
from ..types import MachChain
from .types import AssetInfo, AssetPricingData, UserAssetData


# This is a completely separate client instead of a mixin like the miles server because it has to be initialized, which is expensive and unnecessary for some use cases
class AssetServer:
    __slots__ = (
        "logger",
        "routes",
        "tokens",
        "session",
    )

    @classmethod
    @cachebox.cached(Cache(0), copy_level=2)
    async def create(
        cls,
        *,
        logger: Logger = logging.getLogger("mach-client"),
    ) -> AssetServer:
        client = cls(logger)
        await client.refresh_assets()
        return client

    def __init__(self, logger: Logger):
        self.logger = LogContextAdapter(logger, "Asset Server")
        self.routes = config.config.token_server.endpoints.add_url(
            config.config.token_server.url
        )
        self.tokens: dict[Chain, set[Token]] = {}
        self.session = ClientSession()
        self.session.headers.update(
            (
                ("accept", "application/json"),
                ("Content-Type", "application/json"),
            )
        )

    async def close(self) -> None:
        await self.session.close()

    def is_supported(self, token: Token) -> bool:
        return token.chain in self.tokens and token in self.tokens[token.chain]

    async def _process_chain_data(
        self, chain: Chain, chain_data: dict[str, dict[str, Any]]
    ) -> None:
        chain_client = await ChainClient.create(chain)

        if chain not in self.tokens:
            self.tokens[chain] = set()

        self.tokens[chain].update(
            await asyncio.gather(
                *[
                    Token.register(
                        client=chain_client,
                        address=address,
                        # TODO: The endpoint returns lowercased symbols
                        symbol=token_data["symbol"].upper(),
                        decimals=token_data["decimals"],
                    )
                    for address, token_data in chain_data.items()
                ]
            )
        )

    _assets_validator = TypeAdapter(dict[MachChain, dict[str, dict[str, Any]]])

    # This registers all the tokens returned by the GET /assets endpoint with the client
    async def refresh_assets(self) -> None:
        async with self.session.get(self.routes.assets) as response:
            bytes_result = await utility.to_bytes(response)

        await asyncio.gather(
            *[
                self._process_chain_data(chain.to_chain(), chain_data)
                for chain, chain_data in self._assets_validator.validate_json(
                    bytes_result
                ).items()
            ]
        )

    async def _get_asset_info(self, chain: Chain, address: str) -> Optional[AssetInfo]:
        mach_chain = MachChain.from_chain(chain)
        url = f"{self.routes.assets}/{mach_chain.value}/{address}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        if bytes_result == b"null":
            return None

        return AssetInfo.model_validate_json(bytes_result)

    # Call this if the token in question hasn't yet been registered
    # This gets the asset info and registers the token
    async def get_asset_info(
        self, chain: Chain, address: str
    ) -> Optional[tuple[Token, AssetInfo]]:
        if not (asset_info := await self._get_asset_info(chain, address)):
            return None

        # The refresh_assets method won't register every possible token that you could get info for (ie. it omits very obscure ones)
        # So it's possible we've never seen this token before, and thus should register it first so that it can be looked up
        token = await Token.register(
            client=await ChainClient.create(chain),
            address=address,
            symbol=asset_info.symbol.upper(),
            decimals=asset_info.decimals,
        )

        return (token, asset_info)

    # Call this if the token in question is already in the `Token.lookup_cache`
    async def get_token_info(self, token: Token) -> AssetInfo:
        # The logic is that if you were able to construct a Token object, then it must be in the lookup cache
        # If it was in the lookup cache (which was populated by the asset server), then it must have an asset info
        return await self._get_asset_info(token.chain, token.address)  # type: ignore

    async def get_pricing_data(self, token: Token) -> AssetPricingData:
        mach_chain = MachChain.from_chain(token.chain)
        url = f"{self.routes.prices}/{mach_chain.value}/{token.address}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return AssetPricingData.model_validate_json(bytes_result)

    async def get_price(self, token: Token) -> Decimal:
        pricing_data = await self.get_pricing_data(token)
        return Decimal(pricing_data.price)

    _asset_data_validator = TypeAdapter(dict[MachChain, list[UserAssetData]])

    async def get_raw_token_balances(
        self, account: AccountBase
    ) -> dict[MachChain, list[UserAssetData]]:
        url = f"{self.routes.users}/{account.address}/assets"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return self._asset_data_validator.validate_json(bytes_result)

    _chain_asset_data_validator = TypeAdapter(list[UserAssetData])

    async def get_raw_chain_token_balances(
        self, account: AccountBase
    ) -> list[UserAssetData]:
        mach_chain = MachChain.from_chain(account.chain)
        url = f"{self.routes.users}/{account.address}/assets/{mach_chain.value}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return self._chain_asset_data_validator.validate_json(bytes_result)

    async def _process_chain_balance_data(
        self, chain: Chain, balance_data: list[UserAssetData]
    ) -> dict[Token, int]:
        chain_client = await ChainClient.create(chain)

        tokens = await asyncio.gather(
            *[
                Token.register(
                    client=chain_client,
                    address=asset_data.address,
                    symbol=asset_data.symbol,
                    decimals=None,
                )
                for asset_data in balance_data
                if asset_data.address != "native"
            ]
        )

        balances = dict(zip(tokens, map(lambda data: data.balance, balance_data)))
        return balances

    async def get_token_balances(
        self, account: AccountBase
    ) -> dict[Chain, dict[Token, int]]:
        raw_balances = await self.get_raw_token_balances(account)

        account_chain = type(account.chain)

        filtered_balances = [
            (chain, balances)
            for chain, balances in map(
                lambda item: (item[0].to_chain(), item[1]),
                raw_balances.items(),
            )
            if isinstance(chain, account_chain)
        ]

        chains = map(lambda item: item[0], filtered_balances)

        result = await asyncio.gather(
            *[
                self._process_chain_balance_data(chain, balance_data)
                for chain, balance_data in filtered_balances
            ]
        )

        return dict(zip(chains, result))

    async def get_token_balances_in_coins(
        self, account_id: AccountBase
    ) -> dict[Chain, dict[Token, Decimal]]:
        raw_balances = await self.get_token_balances(account_id)
        return utility.balances_in_coins(raw_balances)

    async def get_chain_token_balances(self, account: AccountBase) -> dict[Token, int]:
        raw_balances = await self.get_raw_chain_token_balances(account)
        return await self._process_chain_balance_data(account.chain, raw_balances)

    async def get_chain_token_balances_in_coins(
        self, account: AccountBase
    ) -> dict[Token, Decimal]:
        raw_balances = await self.get_chain_token_balances(account)
        return utility.chain_balances_in_coins(raw_balances)

    async def get_all_raw_token_balances(
        self, accounts: AccountIDManager
    ) -> dict[Chain, list[UserAssetData]]:
        all_accounts = [
            accounts[chain]
            for chain in (
                SupportedChain.ETHEREUM.value,
                SupportedChain.SOLANA.value,
                SupportedChain.TRON.value,
            )
            if chain in accounts
        ]

        balances = await asyncio.gather(
            *[self.get_raw_token_balances(account) for account in all_accounts]
        )

        result: dict[Chain, list[UserAssetData]] = {}

        for account, balances in zip(all_accounts, balances):
            result.update(
                (
                    (chain.to_chain(), chain_balance)
                    for chain, chain_balance in balances.items()
                    if isinstance(chain.to_chain(), type(account.chain))
                )
            )

        return result

    async def get_all_token_balances(
        self, accounts: AccountIDManager
    ) -> dict[Chain, dict[Token, int]]:
        balances = await asyncio.gather(
            *[
                self.get_token_balances(accounts[chain])
                for chain in (
                    SupportedChain.ETHEREUM.value,
                    SupportedChain.SOLANA.value,
                    SupportedChain.TRON.value,
                )
                if chain in accounts
            ]
        )

        return dict(
            itertools.chain(*[chain_balances.items() for chain_balances in balances])
        )

    async def get_all_token_balances_in_coins(
        self, accounts: AccountIDManager
    ) -> dict[Chain, dict[Token, Decimal]]:
        balances = await self.get_all_token_balances(accounts)
        return utility.balances_in_coins(balances)


__all__ = ["AssetServer"]
