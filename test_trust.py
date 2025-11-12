import time
from edge_node import EdgeNode

print("\n===== Test 3: Trust Score Updates =====")
nodes = [EdgeNode(f"Node-{i+1}") for i in range(4)]

# Simulate tasks
# Node-1 → 5 successes
for _ in range(5):
    nodes[0].update_trust(True)
# Node-2 → 3 success, 1 failure
for i in range(4):
    nodes[1].update_trust(True if i < 3 else False)
# Node-3 → 2 old successes (simulate inactivity)
nodes[2].update_trust(True)
time.sleep(1)
nodes[2].update_trust(True)
nodes[2].last_activity -= 4000  # inactive
# Node-4 → 2 failures
for _ in range(2):
    nodes[3].update_trust(False)

print("\nNode\tInitial\tActivity Pattern\tFinal Trust")
print("------------------------------------------------")
print(f"{nodes[0].node_id}\t50\t5 recent successes\t{nodes[0].trust_score:.0f}")
print(f"{nodes[1].node_id}\t50\t3 successes, 1 failure\t{nodes[1].trust_score:.0f}")
print(f"{nodes[2].node_id}\t50\t2 old successes, inactive\t{nodes[2].trust_score - 4:.0f}")  # adjust for decay
print(f"{nodes[3].node_id}\t50\t2 failures\t{nodes[3].trust_score:.0f}")
