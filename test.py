from blockchain import *
from datetime import datetime

time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
blockchain = Blockchain()

blockA = Block([], time, 0)
blockchain.addBlock(blockA)

blockB = Block([], time, 1)
blockchain.addBlock(blockB)

blockC = Block([], time, 2)
blockchain.addBlock(blockC)

for block in blockchain.chain:
    print(block.index)
    print(block.hash)
    print(block.prev)
    print("=" * len(block.hash))
