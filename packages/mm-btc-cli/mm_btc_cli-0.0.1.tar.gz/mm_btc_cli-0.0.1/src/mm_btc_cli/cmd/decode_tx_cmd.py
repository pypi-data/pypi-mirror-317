from mm_btc.tx import decode_tx
from mm_std import print_json


def run(tx_hex: str, testnet: bool = False) -> None:
    res = decode_tx(tx_hex, testnet)
    print_json(res)
