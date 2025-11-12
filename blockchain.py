from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.validators = []
        self.current_validator = 0
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "Genesis Block", "0", "validator_0")
        self.chain.append(genesis)

    def add_validator(self, validator_id):
        if validator_id not in self.validators:
            self.validators.append(validator_id)

    def get_next_validator(self):
        validator = self.validators[self.current_validator]
        self.current_validator = (self.current_validator + 1) % len(self.validators)
        return validator

    def add_block(self, data):
        validator = self.get_next_validator()
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), data, previous_hash, validator)
        self.chain.append(new_block)
        return new_block

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.previous_hash != prev.hash:
                return False
            if current.hash != current.calculate_hash():
                return False
        return True