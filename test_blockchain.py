"""
Test 1: Creating Blockchain and Adding Blocks
This test demonstrates blockchain creation and block linking.
"""

from blockchain import Blockchain

print("\n" + "="*60)
print("TEST 1: BLOCKCHAIN CREATION AND LINKING")
print("="*60 + "\n")

# Create blockchain
bc = Blockchain()

# Add blocks with node registration data
print("\nAdding blocks...")
bc.add_block("Node-1 registered")
bc.add_block("Node-2 registered")
bc.add_block("Node-1 trust updated: success")

# Display blockchain
bc.display_chain()

# Verify chain integrity
print("\nVerifying blockchain integrity...")
bc.verify_chain()

# Display statistics
print(f"\nTotal blocks in chain: {bc.get_block_count()}")

# Save blockchain
bc.save_to_file()

print("\n✓ Test 1 completed successfully!")