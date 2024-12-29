import abc
from abc import ABC

from aiohttp import ClientSession
from pydantic import TypeAdapter

from ... import config
from ...account import AccountBase
from ...chain import EthereumChain
from .. import utility
from .types import WalletPoints


class MilesServerMixin(ABC):
    __slots__ = ("__routes",)

    def __init__(self, url: str) -> None:
        # The double underscore forces name mangling to occur
        # This allows subclasses to have a different `self.routes` attribute
        self.__routes = config.config.miles_server.endpoints.add_url(url)

    @property
    @abc.abstractmethod
    def session(self) -> ClientSession:
        pass

    async def get_points(self, account: AccountBase) -> float:
        assert isinstance(
            account.chain, EthereumChain
        ), "Points only supported on Ethereum"

        url = f"{self.__routes.points}/{account.address}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return WalletPoints.model_validate_json(bytes_result).points

    _wallet_points_validator = TypeAdapter(list[WalletPoints])

    async def get_all_points(self, limit: int = 10) -> list[WalletPoints]:
        params = {
            "limit": limit,
        }

        async with self.session.get(self.__routes.points, params=params) as response:
            bytes_result = await utility.to_bytes(response)

        return self._wallet_points_validator.validate_json(bytes_result)


__all__ = ["MilesServerMixin"]
