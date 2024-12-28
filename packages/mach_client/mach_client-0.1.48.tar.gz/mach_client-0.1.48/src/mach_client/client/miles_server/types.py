from typing import Annotated

from eth_typing import ChecksumAddress
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from web3 import Web3

# TODO: This is only for Ethereum, might change if this endpoint starts supporting more chains
Wallet = Annotated[ChecksumAddress, AfterValidator(Web3.to_checksum_address)]


class WalletPoints(BaseModel):
    wallet: Wallet
    points: float
