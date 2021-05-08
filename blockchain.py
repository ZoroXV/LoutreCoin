from datetime import datetime
import hashlib

class Blockchain:
    def __init__(self):
        self.chain = []

class Block:
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions
        self.time = time
        self.prev = ''
        self.hash = self.calculateHash()

    def calculateHash(self):
        transactionsHash = ""
        for transaction in self.transactions:
            transactionsHash += transaction.hash

        clearStr = str(self.time) + transactionsHash + self.prev
        return hashlib.sha256(str.encode(clearStr)).hexdigest()

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
