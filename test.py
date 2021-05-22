from blockchain import *
from datetime import datetime

blockchain = Blockchain()

key = blockchain.generateKeys()

blockchain.addTransaction("A", "B", 100, key, key)
blockchain.addTransaction("A", "C", 100, key, key)
blockchain.addTransaction("A", "B", 200, key, key)
blockchain.addTransaction("C", "B", 100, key, key)
blockchain.addTransaction("B", "C", 250, key, key)

blockchain.mine(key)

for block in blockchain.chain:
    print(block.index)
    print(block.hash)
    print(block.prev)
    print("=" * len(block.hash))
