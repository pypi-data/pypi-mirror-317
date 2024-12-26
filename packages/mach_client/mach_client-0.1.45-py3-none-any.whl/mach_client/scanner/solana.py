from __future__ import annotations
import typing

from ..asset import Token
from .scanner import Scanner


class SolanaFM(Scanner):
    url = "https://solana.fm"

    @typing.override
    def address(self, address: str) -> str:
        return f"{self.url}/address/{address}"

    @typing.override
    def transaction(self, transaction_id: str) -> str:
        return f"{self.url}/tx/{transaction_id}"

    @typing.override
    def token(self, token: Token) -> str:
        return self.address(token.address)
