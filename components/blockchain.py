import time
# Import the Block class you just made
from components.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.validators = []
        self.current_validator = 0
        self.create_genesis_block()

    def create_genesis_block(self):
        # The first block in the chain (Hardcoded)
        genesis = Block(0, "Genesis Block - System Boot", "0", "System_Root")
        self.chain.append(genesis)

    def add_validator(self, validator_id):
        """Registers a node as a PoA Validator"""
        if validator_id not in self.validators:
            self.validators.append(validator_id)

    def get_next_validator(self):
        """Round-Robin Validator Rotation (Proof-of-Authority)"""
        if not self.validators:
            return "Unknown_Validator"
        
        validator = self.validators[self.current_validator]
        # Rotate to next
        self.current_validator = (self.current_validator + 1) % len(self.validators)
        return validator

    def add_block(self, data):
        """
        1. Get Validator
        2. Link to Previous Hash
        3. Create & Seal Block
        """
        validator = self.get_next_validator()
        previous_hash = self.chain[-1].hash
        
        # Create the Block using your block.py class
        new_block = Block(len(self.chain), data, previous_hash, validator)
        
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """Verifies integrity (Tamper Detection)"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True