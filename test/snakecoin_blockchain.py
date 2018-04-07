from snakecoin_genesis import create_genesis_block
from test.snakecoin_new_block import next_block

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]


# For test:
# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    # Tell everyone about it!
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))

'''That’s about all that SnakeCoin has to offer. To make SnakeCoin scale
to the size of today’s production blockchains, we’d have to add more
features like a server layer to track changes to the chain on multiple
machines and a proof-of-work algorithm to limit the amount of blocks 
added in a given time period.'''
