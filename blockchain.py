from datetime import datetime
import hashlib

class Blockchain:
    def __init__(self):
        self.chain = [self.addLeadingBlock()]
        self.pendingTransactions = []
        self.header = 4 # Leading Zero wanted for block's hashes
        self.mineReward = 1
        self.blockSize = 5 # Maximum aount of transactions inside one block

    def addLeadingBlock(self):
        currentTime = datetime.now().strftime("%d%m%Y-%H:%M:%S")
        block = Block([], currentTime, 0)
        block.prev = "None"
        return block

    def addBlock(self, block):
        if (len(self.chain) > 0):
            block.prev = self.chain[-1].hash
        else:
            block.prev = "None"

        self.chain.append(block)

    def mine(self, miner):
        pendingSize = len(self.pendingTransactions)
        if (pendingSize <= 0):
            print("Not enough pending transactions to mine a new block. Must be > 1")
            return False
        else:
            for i in range(0, pendingSize, self.blockSize):
                end = i + self.blockSize
                if i >= pendingSize:
                    end = pendingSize

                nextTransactions = self.pendingTransactions[i:end]
                currentTime = datetime.now().strftime("%d%m%Y-%H:%M:%S")

                newBlock = Block(nextTransactions, currentTime, len(self.chain))

                newBlock.prev = self.chain[-1].hash
                newBlock.mine(self.header)

                self.chain.append(newBlock)

            print("Mining pending transactions success!")

            rewardMiner = Transaction("LoutreCoin mining reward", miner, self.mineReward)
            self.pendingTransactions = [rewardMiner]

        return True


class Block:
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions
        self.time = time
        self.proof = 0 # Proof of Work 'x' Value
        self.prev = ''
        self.hash = self.calculateHash()

    def calculateHash(self):
        transactionsHash = ""
        for transaction in self.transactions:
            transactionsHash += transaction.hash

        clearStr = str(self.index) + str(self.time) + transactionsHash + self.prev + str(self.proof)
        return hashlib.sha256(str.encode(clearStr)).hexdigest()

    def mine(self, header):
        pattern = "0" * header
        while self.hash[0:header] != pattern:
            self.proof += 1
            self.hash = self.calculateHash()
            print("X:", self.proof)
            print("Hash attempt:", self.hash)
            print("Pattern wanted:", pattern, "...")

        print("\nBlock Mined! Proof of Work value: ", self.proof)

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        self.hash = self.calculateHash()

    def calculateHash(self):
        clearStr = str(self.time) + self.sender + str(self.amount) + self.receiver
        return hashlib.sha256(str.encode(clearStr)).hexdigest()
