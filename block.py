import hashlib
import json
from time import time

class Block:
    """
    Represents a single block in the blockchain.
    Each block contains an index, timestamp, data, previous hash, and its own hash.
    """
    
    def __init__(self, index, data, previous_hash):
        """
        Initialize a new block.
        
        Args:
            index (int): Position of the block in the chain
            data (str/dict): Transaction data or information to store
            previous_hash (str): Hash of the previous block
        """
        self.index = index
        self.timestamp = time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block.
        
        Returns:
            str: Hexadecimal hash string
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __str__(self):
        """String representation of the block."""
        return f"Block #{self.index} | Hash: {self.hash[:16]}... | Prev: {self.previous_hash[:16]}..."