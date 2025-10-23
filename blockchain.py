from block import Block
import json

class Blockchain:
    """
    Represents the blockchain - a chain of linked blocks.
    Maintains integrity through cryptographic hashing.
    """
    
    def __init__(self):
        """Initialize blockchain with genesis block."""
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain."""
        genesis_block = Block(0, "Genesis Block", "0")
        self.chain.append(genesis_block)
        print(f"✓ Genesis block created: {genesis_block.hash[:16]}...")
    
    def add_block(self, data):
        """
        Add a new block to the chain.
        
        Args:
            data (str/dict): Data to store in the block
            
        Returns:
            Block: The newly created block
        """
        previous_block = self.chain[-1]
        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )
        self.chain.append(new_block)
        print(f"✓ Block #{new_block.index} added: {data}")
        return new_block
    
    def verify_chain(self):
        """
        Verify the integrity of the entire blockchain.
        
        Returns:
            bool: True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Check if current block's hash is correct
            if current.hash != current.calculate_hash():
                print(f"✗ Block #{current.index} has been tampered!")
                return False
            
            # Check if previous hash matches
            if current.previous_hash != previous.hash:
                print(f"✗ Chain broken between blocks #{previous.index} and #{current.index}")
                return False
        
        print("✓ Blockchain verification passed - chain is valid!")
        return True
    
    def display_chain(self):
        """Display all blocks in the chain."""
        print("\n" + "="*60)
        print("BLOCKCHAIN CONTENTS")
        print("="*60)
        for block in self.chain:
            print(block)
        print("="*60 + "\n")
    
    def get_block_count(self):
        """Return the number of blocks in the chain."""
        return len(self.chain)
    
    def save_to_file(self, filename="blockchain_data.json"):
        """Save blockchain to JSON file."""
        chain_data = []
        for block in self.chain:
            chain_data.append({
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            })
        
        with open(filename, 'w') as f:
            json.dump(chain_data, f, indent=4)
        print(f"✓ Blockchain saved to {filename}")