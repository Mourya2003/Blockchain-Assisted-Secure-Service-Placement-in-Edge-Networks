import hashlib
import json
import time

class Block:
    def __init__(self, index, data, previous_hash, validator_id):
        self.index = index
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.data = data
        self.previous_hash = previous_hash
        self.validator_id = validator_id
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "validator_id": self.validator_id
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
