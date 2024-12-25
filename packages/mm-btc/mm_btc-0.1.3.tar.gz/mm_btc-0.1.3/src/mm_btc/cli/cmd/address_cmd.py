from mm_std import print_json

from mm_btc.blockstream import BlockstreamClient
from mm_btc.wallet import is_testnet_address


def run(address: str) -> None:
    client = BlockstreamClient(testnet=is_testnet_address(address))
    res = client.get_address(address)
    print_json(res)
