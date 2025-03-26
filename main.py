import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):        # using SHA-256 for hashing
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def tamper_block(self, index, new_data):
        if index > 0 and index < len(self.chain):
            self.chain[index].transactions = new_data
            self.chain[index].hash = self.chain[index].calculate_hash()

# Example Usage of Blockchain

blockchain = Blockchain()
blockchain.add_block(["Aryan pays Rahul 5 BTC"])
blockchain.add_block(["Rahul pays Virat 2 BTC"])

# Print Blockchain

for block in blockchain.chain:
    print(vars(block))

# Here I validate blockchain before tampering

print("Is the blockchain valid:", blockchain.is_chain_valid())

# Trying to tamper with the blockchain

blockchain.tamper_block(1, ["Aryan pays Rahul 50 BTC"])

# Looking to validate the blockchain after tampering

print("Is the blockchain valid after tampering:", blockchain.is_chain_valid())