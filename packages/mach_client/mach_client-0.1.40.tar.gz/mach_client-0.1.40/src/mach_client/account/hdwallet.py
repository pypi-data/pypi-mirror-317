from __future__ import annotations
import dataclasses

from hdwallet import HDWallet
from hdwallet.const import PUBLIC_KEY_TYPES
from hdwallet.cryptocurrencies import Bitcoin, Ethereum, ICryptocurrency, Solana, Tron
from hdwallet.derivations import BIP44Derivation
from hdwallet.entropies import BIP39_ENTROPY_STRENGTHS, BIP39Entropy
from hdwallet.hds import BIP44HD
from hdwallet.mnemonics import BIP39Mnemonic

from ..chain import Chain, EthereumChain, SolanaChain, TronChain
from .account import Account, AccountID


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Wallet:
    xprivate_key: str

    @staticmethod
    def create_base(cryptocurrency: type[ICryptocurrency] = Bitcoin) -> HDWallet:
        return HDWallet(
            cryptocurrency=cryptocurrency,
            hd=BIP44HD,
            network=cryptocurrency.NETWORKS.MAINNET,
            public_key_type=PUBLIC_KEY_TYPES.COMPRESSED,
        )

    @classmethod
    def create(cls) -> Wallet:
        hdwallet = cls.create_base().from_entropy(
            entropy=BIP39Entropy(
                entropy=BIP39Entropy.generate(
                    strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
                )
            )
        )

        return cls(xprivate_key=hdwallet.xprivate_key())  # type: ignore

    @classmethod
    def from_mnemonic(cls, mnemonic: str) -> Wallet:
        hdwallet = cls.create_base().from_mnemonic(mnemonic=BIP39Mnemonic(mnemonic))
        return cls(xprivate_key=hdwallet.xprivate_key())  # type: ignore

    @classmethod
    def from_xprivate_key(cls, xprivate_key: str) -> Wallet:
        return cls(xprivate_key=xprivate_key)

    # TODO: With `python-hdwallet`, if you don't create the HDWallet object using a mnemonic, it pretends it doesn't have one.
    @property
    def mnemonic(self) -> str:
        assert (
            mnemonic := self.create_base()
            .from_xprivate_key(self.xprivate_key)
            .mnemonic()
        )
        return mnemonic

    @property
    def xpublic_key(self) -> str:
        return (
            self.create_base().from_xprivate_key(self.xprivate_key).root_xpublic_key()
        )  # type: ignore

    # Derive the default address for the chain
    def derive_default(self, chain: Chain) -> HDWallet:
        match chain:
            case EthereumChain():
                cryptocurrency = Ethereum
            case SolanaChain():
                cryptocurrency = Solana
            case TronChain():
                cryptocurrency = Tron
            case _:
                assert False, f"Unsupported chain: {chain} with type {type(chain)}"

        return (
            self.create_base(cryptocurrency)
            .from_xprivate_key(self.xprivate_key)
            .from_derivation(
                # Notice that we use the base coin type instead of the chain's coin type
                # So ie. BSC will use the same derivation path as Ethereum
                # This is to ensure that as many chains use the same keypair as possible
                derivation=BIP44Derivation(coin_type=cryptocurrency.COIN_TYPE)
            )
        )

    def account[ChainType: Chain](self, chain: ChainType) -> Account[ChainType]:
        private_key = self.derive_default(chain).private_key()
        return Account.from_str(chain, private_key)  # type: ignore

    def account_id[ChainType: Chain](self, chain: ChainType) -> AccountID[ChainType]:
        address = self.derive_default(chain).address()
        return AccountID.from_str(chain, address)
