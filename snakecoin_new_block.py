import datetime as date

from snakecoin_block import Block


def next_block(last_block):
    index = last_block.index + 1
    timestamp = date.datetime.now()
    data = "Hey! I'm block " + str(index)
    previous_hash = last_block.hash
    return Block(index, timestamp, data, previous_hash)
