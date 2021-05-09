from blockchain import *
from datetime import datetime

blockchain = Blockchain()

key = blockchain.generateKeys()

blockchain.addTransaction("A", "B", 100, key, key)

for block in blockchain.chain:
    print(block.index)
    print(block.hash)
    print(block.prev)
    print("=" * len(block.hash))

