from __future__ import annotations
from decimal import Decimal
from importlib import resources
from importlib.resources.abc import Traversable
import json
import os
from pathlib import Path
from typing import Any, Annotated, Optional

from pydantic import BaseModel, PlainValidator
import yaml

from .account import AccountManager, SimpleAccountManager
from .chain import Chain, constants


class AddURLMixin(BaseModel):
    def add_url[Self: AddURLMixin](self: Self, url: str) -> Self:
        return type(self)(
            **{key: f"{url}{value}" for key, value in self.model_dump().items()}
        )


class BackendAPIRoutes(AddURLMixin):
    orders: str = "/v1/orders"
    cctp_orders: str = "/v1/orders/cctp"
    order_status: str = "/v1/orders/status"
    gas: str = "/v1/orders/gas"
    quotes: str = "/v1/quotes"
    points: str = "/v1/points"
    token_balances: str = "/tokenBalances"
    get_config: str = "/get_config"
    get_all_tokens_from_db: str = "/v1/tokens/get_all_tokens_from_db"


class BackendConfig(BaseModel):
    url: str
    endpoints: BackendAPIRoutes = BackendAPIRoutes()


class MilesServerAPIRoutes(AddURLMixin):
    points: str = "/v1/points"
    twitter: str = "/v1/twitter"
    profile: str = "/v1/profile"


class MilesServerConfig(BaseModel):
    url: str
    endpoints: MilesServerAPIRoutes = MilesServerAPIRoutes()


class TokenServerAPIRoutes(AddURLMixin):
    assets: str = "/v1/assets"
    prices: str = "/v1/prices"
    users: str = "/v1/users"


class TokenServerConfig(BaseModel):
    url: str
    endpoints: TokenServerAPIRoutes = TokenServerAPIRoutes()


class TradingConfig(BaseModel):
    slippage_tolerance: Decimal


def parse_endpoint_uris(data: dict[str, str]) -> dict[Chain, str]:
    return {
        Chain.from_id(*chain_id.split(":")): endpoint_uri
        for chain_id, endpoint_uri in data.items()
        if chain_id in constants.CHAIN_ID_TO_CHAIN
    }


class Config(BaseModel):
    backend: BackendConfig
    miles_server: MilesServerConfig
    token_server: TokenServerConfig
    trading: TradingConfig
    endpoint_uris: Annotated[dict[Chain, str], PlainValidator(parse_endpoint_uris)]


def load_abi(path: Traversable) -> Any:
    with path.open("r") as abi:
        return json.load(abi)


config_path = Path(os.environ.get("CONFIG_PATH", "config.yaml"))
with open(config_path) as config_file:
    full_config = yaml.safe_load(config_file)

config = Config.model_validate(full_config["mach_client"])

accounts: Optional[AccountManager] = (
    None
    if "accounts" not in full_config
    else SimpleAccountManager.from_key_values(**full_config["accounts"])
)

abi_path = resources.files("abi")

ethereum_order_book_abi = load_abi(abi_path / "ethereum" / "order_book.json")
tron_order_book_abi = load_abi(abi_path / "tron" / "order_book.json")

ethereum_cctp_token_messenger_abi = load_abi(abi_path / "ethereum" / "cctp_token_messenger.json")

erc20_abi = load_abi(abi_path / "ethereum" / "erc20.json")
trc20_abi = load_abi(abi_path / "tron" / "trc20.json")
