"""
Test 3: Trust Score Update
This test demonstrates trust score calculation and updates.
"""

from edge_node import EdgeNode
from blockchain import Blockchain

print("\n" + "="*60)
print("TEST 3: TRUST SCORE UPDATES")
print("="*60 + "\n")

# Create blockchain
bc = Blockchain()

# Create edge nodes
print("Creating edge nodes...\n")
node1 = EdgeNode("Node-1", cpu_cores=8, memory_gb=16)
node2 = EdgeNode("Node-2", cpu_cores=4, memory_gb=8)

print(node1)
print(node2)

# Simulate task executions
print("\n" + "-"*60)
print("Simulating task executions...")
print("-"*60 + "\n")

print("Task 1: Node-1 executes task")
node1.update_trust(True, "Image processing task completed")
bc.add_block(f"{node1.node_id} - Success - Trust: {node1.trust_score}")

print("\nTask 2: Node-2 executes task")
node2.update_trust(True, "Data analysis task completed")
bc.add_block(f"{node2.node_id} - Success - Trust: {node2.trust_score}")

print("\nTask 3: Node-1 executes another task")
node1.update_trust(True, "ML inference completed")
bc.add_block(f"{node1.node_id} - Success - Trust: {node1.trust_score}")

print("\nTask 4: Node-2 fails a task")
node2.update_trust(False, "Timeout - task failed")
bc.add_block(f"{node2.node_id} - Failure - Trust: {node2.trust_score}")

# Display final status
print("\n" + "="*60)
print("FINAL NODE STATUS")
print("="*60 + "\n")
print(node1)
print(node2)

# Check trustworthiness (threshold = 60)
print("\n" + "-"*60)
print("Trust Evaluation (Threshold: 60)")
print("-"*60)
print(f"{node1.node_id}: {'✓ TRUSTED' if node1.is_trustworthy() else '✗ UNTRUSTED'}")
print(f"{node2.node_id}: {'✓ TRUSTED' if node2.is_trustworthy() else '✗ UNTRUSTED'}")

# Display blockchain
bc.display_chain()

print("\n✓ Test 3 completed successfully!")