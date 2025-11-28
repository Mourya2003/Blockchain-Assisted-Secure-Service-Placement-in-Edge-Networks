import time
from components.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.validators = []
        self.current_validator = 0
        self.pending_transactions = [] 
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "Genesis Block", "0", "System_Root")
        self.chain.append(genesis)

    def add_validator(self, validator_id):
        if validator_id not in self.validators:
            self.validators.append(validator_id)

    def get_next_validator(self):
        if not self.validators: return "Unknown"
        validator = self.validators[self.current_validator]
        self.current_validator = (self.current_validator + 1) % len(self.validators)
        return validator

    def add_block(self, data):
        validator = self.get_next_validator()
        previous_hash = self.chain[-1].hash if self.chain else "0"
        new_block = Block(len(self.chain), data, previous_hash, validator)
        self.chain.append(new_block)
        return new_block

    def add_transaction(self, data, gas_fee):
        txn = {
            "data": data,
            "gas": gas_fee,
            "timestamp": time.time(),
            "formatted_time": time.strftime("%H:%M:%S")
        }
        self.pending_transactions.append(txn)
        return len(self.pending_transactions)

    def mine_pending_block(self):
        if not self.pending_transactions:
            return None
            
        # 1. SORT BY GAS (Highest Fee First)
        # This is the "Priority" logic
        sorted_txns = sorted(
            self.pending_transactions, 
            key=lambda x: (-x['gas'], x['timestamp'])
        )
        
        # 2. CAP THE BLOCK (The "Realism" Upgrade)
        # We limit the block to only 3 transactions.
        # This forces "Congestion" so you can see low-fee items get left behind.
        BLOCK_CAPACITY = 3 
        
        accepted_txns = sorted_txns[:BLOCK_CAPACITY]
        leftover_txns = sorted_txns[BLOCK_CAPACITY:]
        
        # 3. Create the Block
        block_data = " | ".join([f"[Gas:{t['gas']}] {t['data']}" for t in accepted_txns])
        new_block = self.add_block(block_data)
        
        # 4. Update Mempool (Keep the leftovers waiting)
        self.pending_transactions = leftover_txns
        
        return new_block, len(leftover_txns) # Return count of leftovers

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash(): return False
            if current.previous_hash != prev.hash: return False
        return True