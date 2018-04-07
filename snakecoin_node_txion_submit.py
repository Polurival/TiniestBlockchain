import datetime as date
import json

from flask import Flask
from flask import request

from snakecoin_block import Block
from snakecoin_genesis import create_genesis_block
from snakecoin_pow import proof_of_work

node = Flask(__name__)

# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# This node's blockchain copy
blockchain = [create_genesis_block()]
# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []  # todo надо как-то добавлять юрлы остальных нод
# A variable to deciding if we're mining or not
mining = True


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        # On each new POST request,
        # we extract the transaction data
        new_txion = request.get_json()
        # Then we add the transaction to our list
        this_nodes_transactions.append(new_txion)
        # Because the transaction was successfully
        # submitted, we log it to our console
        print("New transaction")
        print("FROM: {}".format(new_txion['from']).encode('ascii', 'replace'))
        print("TO: {}".format(new_txion['to']).encode('ascii', 'replace'))
        print("AMOUNT: {}\n".format(new_txion['amount']))
        # Then we let the client know it worked out
        return "Transaction submission successful\n"


@node.route('/mine', methods=['GET'])
def mine():
    # Get the last proof of work
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    # Find the proof of work for
    # the current block being mined
    # Note: The program will hang here until a new
    #       proof of work is found
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
    # we know we can mine a block so
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # Empty transaction list
    this_nodes_transactions[:] = []
    # Now create the
    # new block!
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)
    # Let the client know we mined a block
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "previous_hash": last_block_hash
    }) + "\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    # Convert our blocks into dictionaries
    # so we can send them as json objects later
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        chain_to_send[i] = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            # "previous_hash": block.previous_hash,  - почему-то в примере нет этой строчки???
            "hash": block_hash
        }
    # Send our chain to whomever requested it
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


node.run()

"""
te a transaction.
curl "localhost:5000/txion" \
     -H "Content-Type: application/json" \
     -d '{"from": "akjflw", "to":"fjlakdj", "amount": 3}'
2. Mine a new block.

curl localhost:5000/mine
3. Check out the results. From the client window, we see this.
"""
