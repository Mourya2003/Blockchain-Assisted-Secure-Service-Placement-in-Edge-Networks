"""
COMPLETE DEMO - For Mid-Semester Presentation
Shows all implemented features in sequence.
"""

from blockchain import Blockchain
from edge_node import EdgeNode
import time

def print_header(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def demo_pause(seconds=1):
    """Pause for dramatic effect during demo."""
    time.sleep(seconds)

# ============================================================================
# DEMO START
# ============================================================================

print_header("BLOCKCHAIN-BASED TRUST MANAGEMENT SYSTEM - DEMO")

# Step 1: Create Blockchain
print_header("STEP 1: Initialize Blockchain")
bc = Blockchain()
demo_pause()

# Step 2: Register Nodes
print_header("STEP 2: Register Edge Nodes")
nodes = {
    "Node-1": EdgeNode("Node-1", cpu_cores=8, memory_gb=16),
    "Node-2": EdgeNode("Node-2", cpu_cores=4, memory_gb=8),
    "Node-3": EdgeNode("Node-3", cpu_cores=2, memory_gb=4),
    "Node-4": EdgeNode("Node-4", cpu_cores=4, memory_gb=8),
    "Node-5": EdgeNode("Node-5", cpu_cores=8, memory_gb=16)
}

for node_id, node in nodes.items():
    bc.add_block(f"{node_id} registered")
    print(f"  {node}")
demo_pause()

# Step 3: Simulate Task Execution
print_header("STEP 3: Simulate Task Executions")

tasks = [
    ("Node-1", True, "Image processing completed"),
    ("Node-2", True, "Data analysis completed"),
    ("Node-3", False, "Timeout - task failed"),
    ("Node-1", True, "ML inference completed"),
    ("Node-4", False, "Connection lost"),
    ("Node-2", False, "Resource exhaustion"),
    ("Node-5", True, "Video transcoding completed"),
    ("Node-1", True, "Encryption task completed"),
    ("Node-3", True, "Data sync completed"),
    ("Node-4", True, "Monitoring task completed")
]

print("\nExecuting 10 tasks across nodes...\n")
for node_id, success, description in tasks:
    nodes[node_id].update_trust(success, description)
    bc.add_block(f"{node_id} - {'Success' if success else 'Failure'} - Trust: {nodes[node_id].trust_score}")
    demo_pause(0.3)

# Step 4: Display Trust Scores
print_header("STEP 4: Final Trust Scores")
print(f"{'Node ID':<15} {'Trust Score':<15} {'Level':<15} {'Trustworthy?':<15}")
print("-"*60)
for node_id, node in nodes.items():
    trustworthy = "✓ YES" if node.is_trustworthy() else "✗ NO"
    print(f"{node_id:<15} {node.trust_score:<15} {node.get_trust_level():<15} {trustworthy:<15}")

# Step 5: Service Placement Decision
print_header("STEP 5: Service Placement Decision")
print("New service requires: Trust >= 60, 4+ CPU cores\n")

eligible_nodes = []
for node_id, node in nodes.items():
    if node.is_trustworthy() and node.cpu_cores >= 4:
        eligible_nodes.append((node_id, node.trust_score))

if eligible_nodes:
    eligible_nodes.sort(key=lambda x: x[1], reverse=True)
    selected = eligible_nodes[0]
    print(f"✓ Service placed on: {selected[0]} (Trust: {selected[1]})")
    print(f"\nEligible nodes: {[n[0] for n in eligible_nodes]}")
else:
    print("✗ No eligible nodes found!")

# Step 6: Blockchain Verification
print_header("STEP 6: Verify Blockchain Integrity")
bc.verify_chain()

# Step 7: Display Statistics
print_header("STEP 7: System Statistics")
print(f"Total blocks in chain: {bc.get_block_count()}")
print(f"Total nodes registered: {len(nodes)}")
print(f"Trusted nodes (≥60): {sum(1 for n in nodes.values() if n.is_trustworthy())}")
print(f"Tasks executed: {len(tasks)}")
print(f"Success rate: {sum(1 for t in tasks if t[1]) / len(tasks) * 100:.1f}%")

# Save blockchain
print("\nSaving blockchain data...")
bc.save_to_file("demo_blockchain.json")

print_header("DEMO COMPLETED SUCCESSFULLY!")
print("All features demonstrated:")
print("  ✓ Blockchain creation and block linking")
print("  ✓ Node registration")
print("  ✓ Trust score calculation")
print("  ✓ Service placement decision")
print("  ✓ Chain integrity verification")
print("="*70 + "\n")