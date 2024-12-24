from ..account import AccountBase
from ..asset import Token
from ..chain import Chain
from ..transaction import SentTransaction
from .scanner import Scanner


def address(chain: Chain, address: str) -> str:
    return Scanner.create(chain).address(address)


def account(account: AccountBase) -> str:
    return address(account.chain, account.address)


def transaction(chain: Chain, transaction_id: str) -> str:
    return Scanner.create(chain).transaction(transaction_id)


def sent_transaction(sent_transaction: SentTransaction) -> str:
    return transaction(sent_transaction.chain, sent_transaction.id)


def token(token: Token) -> str:
    return Scanner.create(token.chain).token(token)
