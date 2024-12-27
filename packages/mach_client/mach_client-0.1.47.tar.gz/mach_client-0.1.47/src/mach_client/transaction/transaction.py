import abc
from abc import ABC
import dataclasses
from typing import Any


from ..chain import Chain


# Proxy for a chain-specific sent transaction
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SentTransaction[ChainType: Chain](ABC):
    # TODO: This currently doesn't follow the convention in the rest of the codebase that the `.id` property should produce a CAIP identifier that is unique across chains. Instead we return the transaction hash or equivalent, which is not necessarily unique across chains.
    @property
    @abc.abstractmethod
    def id(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass

    # Confirms the transaction if necessary and returns the receipt/response
    @abc.abstractmethod
    async def wait_for_receipt(self, **kwargs) -> Any:
        pass


# Proxy for a chain-specific transaction
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Transaction[
    ChainType: Chain,
](ABC):
    @abc.abstractmethod
    async def broadcast(self) -> SentTransaction[ChainType]:
        pass

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass
