import time
from components.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.validators = []
        self.current_validator = 0
        
        # MEMPOOL: Stores dicts {'data': str, 'gas': int, 'time': float}
        self.pending_transactions = [] 
        
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "Genesis Block - System Boot", "0", "System_Root")
        self.chain.append(genesis)

    def add_validator(self, validator_id):
        if validator_id not in self.validators:
            self.validators.append(validator_id)

    def get_next_validator(self):
        if not self.validators: return "Unknown"
        validator = self.validators[self.current_validator]
        self.current_validator = (self.current_validator + 1) % len(self.validators)
        return validator

    # --- CORE FEATURE: ADD WITH GAS FEE ---
    def add_transaction(self, data, gas_fee):
        """
        Adds a transaction to the Mempool with a specific Gas Fee.
        """
        txn = {
            "data": data,
            "gas": gas_fee,
            "timestamp": time.time(),
            "formatted_time": time.strftime("%H:%M:%S")
        }
        self.pending_transactions.append(txn)
        return len(self.pending_transactions)

    # --- CORE FEATURE: MINE HIGHEST PRIORITY FIRST ---
    def mine_pending_block(self):
        """
        Bundles transactions into a block, SORTED BY GAS FEE.
        High gas transactions get processed first.
        """
        if not self.pending_transactions:
            return None
            
        # 1. SORTING LOGIC (The "Real" Part)
        # Sort by Gas (Descending), then by Time (Ascending)
        sorted_txns = sorted(
            self.pending_transactions, 
            key=lambda x: (-x['gas'], x['timestamp'])
        )
        
        # 2. Bundle Data (Simulating Block Size Limit)
        # In real life, blocks have size limits. We take top 10.
        selected_txns = sorted_txns[:10] 
        
        # Create readable string for the block
        block_data = " | ".join([f"[Gas:{t['gas']}] {t['data']}" for t in selected_txns])
        
        # 3. Create Block
        validator = self.get_next_validator()
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), block_data, previous_hash, validator)
        self.chain.append(new_block)
        
        # 4. Remove mined transactions from buffer
        # (Keep the ones that didn't fit, if any)
        self.pending_transactions = sorted_txns[10:]
        
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash(): return False
            if current.previous_hash != prev.hash: return False
        return True