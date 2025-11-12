from blockchain import Blockchain

print("\n===== Test 1: Blockchain Creation and Validator Rotation =====")
bc = Blockchain()
bc.add_validator("validator_1")
bc.add_validator("validator_2")
bc.add_validator("validator_3")

# Add 6 blocks
for i in range(6):
    block = bc.add_block(f"Transaction {i+1}")
    print(f"Block {block.index} added by {block.validator_id}")

print("\nVerifying blockchain integrity...")
print("Integrity Check:", "✅ Passed" if bc.verify_chain() else "❌ Failed")

# Simulate tampering
print("\n===== Test 2: Tampering Detection =====")
bc.chain[3].data = "Tampered Data"
print("After tampering → Integrity Check:", "✅ Passed" if bc.verify_chain() else "⚠️ Tampering Detected")
