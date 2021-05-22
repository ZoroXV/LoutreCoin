from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import *
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
        if (pendingSize < self.blockSize):
            print("Not enough pending transactions to mine a new block. Must be >=", self.blockSize)
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

            rewardMiner = Transaction("LoutreCoin", miner, self.mineReward)
            self.pendingTransactions = [rewardMiner]

        return True

    def generateKeys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open("rsa_pub.key", "wb")
        file_out.write(private_key)

        public_key = key.publickey().export_key()
        file_out = open("rsa.key", "wb")
        file_out.write(public_key)

        return key.publickey().export_key().decode('ASCII')

    def addTransaction(self, sender, reciever, amt, keyString, senderKey):
        keyByte = keyString.encode("ASCII");
        senderKeyByte = senderKey.encode("ASCII");

        key = RSA.import_key(keyByte);
        senderKey = RSA.import_key(senderKeyByte);

        if not sender or not reciever or not amt:
            print("Invalid Transaction parameters");
            return False;

        transaction = Transaction(sender, reciever, amt);
        transaction.signTransaction(key, senderKey);

        if not transaction.isValidTransaction():
            print("");
            return False;
        self.pendingTransactions.append(transaction);
        return len(self.chain) + 1;

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

    def isValidTransaction(self):

        if(self.hash != self.calculateHash()):
            return False;
        if(self.sender == self.receiver):
            return False;
        if(self.sender == "LoutreCoin"):
            #security : unfinished
            return True;
        if not self.signature or len(self.signature) == 0:
            print("No Signature!")
            return False;
        return True;

    def signTransaction(self, key, senderKey):
        if(self.hash != self.calculateHash()):
            print("transaction tampered error")
            return False

        if(str(key.publickey().export_key()) != str(senderKey.publickey().export_key())):
            print("Transaction attempt to be signed from another wallet")
            return False

        pkcs1_15.new(key)

        self.signature = "made"
        print("made signature!")
        return True
