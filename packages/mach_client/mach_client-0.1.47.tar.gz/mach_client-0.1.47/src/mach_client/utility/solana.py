# Reference:
# https://github.com/circlefin/solana-cctp-contracts/blob/master/examples/utils.ts
# https://github.com/tristeroresearch/cache-half-full/blob/dev-solana-add-bond/backend/solutils.py

import functools
import typing

from solders.pubkey import Pubkey


@functools.cache
def find_program_address(
    label: str,
    program_id: Pubkey,
    extra_seeds: tuple[str | bytes | bytearray | Pubkey] = tuple(),
) -> tuple[Pubkey, int]:
    seeds = [label.encode()]

    for seed in extra_seeds:
        match seed:
            case str():
                seeds.append(seed.encode())
            case bytes() | bytearray():
                seeds.append(seed)
            case Pubkey() | memoryview():
                seeds.append(bytes(seed))
            case _ as arg:
                typing.assert_never(arg)

        if isinstance(seed, str):
            seeds.append(seed.encode())
        elif isinstance(seed, (bytes, bytearray)):
            seeds.append(seed)
        elif isinstance(seed, Pubkey):
            seeds.append(bytes(seed))

    return Pubkey.find_program_address(seeds, program_id)
