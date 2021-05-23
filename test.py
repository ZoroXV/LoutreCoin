from blockchain import *
from datetime import datetime

blockchain = Blockchain()

key = blockchain.generateKeys()

blockchain.addTransaction("A", "B", 100, key, key)
blockchain.addTransaction("A", "C", 100, key, key)
blockchain.addTransaction("A", "B", 200, key, key)
blockchain.addTransaction("C", "B", 100, key, key)
blockchain.addTransaction("B", "C", 250, key, key)

blockchain.addTransaction("C", "B", 10, key, key)
blockchain.addTransaction("B", "C", 25, key, key)
blockchain.addTransaction("A", "B", 10, key, key)
blockchain.addTransaction("B", "A", 25, key, key)

blockchain.mine("Steve")
blockchain.mine("Steve")
blockchain.mine("Steve")

for block in blockchain.chain:
    print(block.index)
    print(block.hash)
    print(block.prev)
    print("Block's transactions")
    for transaction in block.transactions:
        print('\t', transaction.sender, "give", transaction.amount, "LC to", transaction.receiver)
    print("=" * len(block.hash))
