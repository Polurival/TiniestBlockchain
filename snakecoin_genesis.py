import datetime as date

from snakecoin_block import Block


def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), {
        "proof-of-work": 9,
        "transactions": None
    }, "0")
