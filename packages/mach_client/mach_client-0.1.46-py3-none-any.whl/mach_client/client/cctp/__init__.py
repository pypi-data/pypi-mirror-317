from __future__ import annotations
import typing

from eth_typing import ChecksumAddress
from solders.keypair import Keypair
from solders.pubkey import Pubkey

from ... import config
from ...account import (
    Account,
    AccountID,
    EthereumAccount,
    EthereumAccountID,
    SolanaAccount,
    SolanaAccountID,
)
from ...asset import SolanaToken, Token
from ...chain import Chain
from ...chain_client import (
    ChainClient,
    EthereumClient,
    SolanaClient,
)
from ...transaction import (
    EthereumTransaction,
    SolanaTransaction,
    Transaction,
)
from ...utility import solana as solana_utility
from ..types import OrderData
from .solana import instructions
from .solana.instructions import (
    DepositForBurnAccounts,
    DepositForBurnArgs,
)
from .solana.types import DepositForBurnParams

if typing.TYPE_CHECKING:
    from ...client import MachClient


async def create_cctp_burn_transaction[SrcChainType: Chain, DestChainType: Chain](
    *,
    client: MachClient,
    src_client: ChainClient[SrcChainType],
    src_token: Token[SrcChainType],
    dest_token: Token[DestChainType],
    order_data: OrderData,
    signer: Account[SrcChainType],
    recipient: AccountID[DestChainType],
) -> Transaction[SrcChainType]:
    token_messenger_minter_address = client.cctp_token_messenger_minter_address(
        src_client.chain
    )
    destination_domain = client.cctp_domain(recipient.chain)

    match src_client:
        case EthereumClient():
            recipient_bytes = recipient.encode_address().rjust(32, b"\0")

            contract = src_client.w3.eth.contract(
                address=typing.cast(ChecksumAddress, token_messenger_minter_address),
                abi=config.ethereum_cctp_token_messenger_abi,
            )

            burn_function = contract.functions.depositForBurn(
                order_data.order_funding.src_amount_in,
                destination_domain,
                recipient_bytes,
                order_data.order_direction.src_token_address,
            )

            return await EthereumTransaction.from_contract_function(
                src_client, burn_function, typing.cast(EthereumAccount, signer)
            )

        case SolanaClient():
            recipient_pubkey = typing.cast(SolanaAccountID, recipient).pubkey
            recipient_token_account = typing.cast(
                SolanaToken, dest_token
            ).associated_token_account(recipient_pubkey)

            params = DepositForBurnParams(
                amount=order_data.order_funding.src_amount_in,
                destination_domain=destination_domain,
                mint_recipient=recipient_token_account,
            )

            args = DepositForBurnArgs(params=params)

            owner = typing.cast(SolanaAccountID, signer).pubkey
            burn_token_account = typing.cast(
                SolanaToken, src_token
            ).associated_token_account(owner)

            message_transmitter = Pubkey.from_string(
                client.cctp_message_transmitter_address(src_client.chain)
            )
            token_messenger_minter = Pubkey.from_string(token_messenger_minter_address)

            usdc_mint = typing.cast(SolanaToken, src_token).mint

            accounts = DepositForBurnAccounts(
                owner=owner,
                event_rent_payer=owner,
                sender_authority_pda=solana_utility.find_program_address(
                    "sender_authority", token_messenger_minter
                )[0],
                burn_token_account=burn_token_account,
                message_transmitter=solana_utility.find_program_address(
                    "message_transmitter", message_transmitter
                )[0],
                token_messenger=solana_utility.find_program_address(
                    "token_messenger", token_messenger_minter
                )[0],
                remote_token_messenger=solana_utility.find_program_address(
                    "remote_token_messenger",
                    token_messenger_minter,
                    (str(destination_domain),),
                )[0],
                token_minter=solana_utility.find_program_address(
                    "token_minter", token_messenger_minter
                )[0],
                local_token=solana_utility.find_program_address(
                    "local_token",
                    token_messenger_minter,
                    (usdc_mint,),
                )[0],
                burn_token_mint=usdc_mint,
                message_sent_event_data=Keypair().pubkey(),
                message_transmitter_program=message_transmitter,
                token_messenger_minter_program=token_messenger_minter,
                event_authority=solana_utility.find_program_address(
                    "__event_authority", token_messenger_minter
                )[0],
                program=token_messenger_minter,
            )

            instruction = instructions.deposit_for_burn(args=args, accounts=accounts)

            return await SolanaTransaction.create(
                src_client, (instruction,), (typing.cast(SolanaAccount, signer),)
            )

        case _:
            raise NotImplementedError(src_client.chain)


__all__ = ["create_cctp_burn_transaction"]
