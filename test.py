from blockchain import *
from datetime import datetime

blockchain = Blockchain()

tr1 = Transaction("Monsieur A", "Madame B", 100)

blockchain.pendingTransactions.append(tr1)

blockchain.mine("Steve")

for block in blockchain.chain:
    print(block.index)
    print(block.hash)
    print(block.prev)
    print("=" * len(block.hash))
