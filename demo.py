from blockchain import Blockchain
from edge_node import EdgeNode
import random

print("\n===== Demo: Blockchain + Trust + Placement =====")

# Setup blockchain
bc = Blockchain()
for v in ["validator_1", "validator_2", "validator_3"]:
    bc.add_validator(v)

for i in range(6):
    bc.add_block(f"Transaction {i+1}")
print("✅ Blockchain created successfully with", len(bc.chain), "blocks")

# Create nodes
nodes = [
    {"id": "Node-1", "trust": 75, "reliability": 0.85, "cpu": 80, "mem": 12},
    {"id": "Node-2", "trust": 68, "reliability": 0.75, "cpu": 90, "mem": 10},
    {"id": "Node-3", "trust": 55, "reliability": 0.60, "cpu": 70, "mem": 10},
    {"id": "Node-4", "trust": 72, "reliability": 0.78, "cpu": 60, "mem": 8},
    {"id": "Node-5", "trust": 45, "reliability": 0.55, "cpu": 95, "mem": 16}
]

TRUST_THRESHOLD = 60
print("\nEligible nodes (Trust ≥ 60):")
eligible = [n for n in nodes if n["trust"] >= TRUST_THRESHOLD]
for n in eligible:
    print(f"{n['id']} - Trust: {n['trust']}")

# Compute placement score
def calc_score(n):
    w1, w2, w3 = 0.5, 0.3, 0.2
    L = ((n["cpu"]/100 + n["mem"]/16)/2)
    return w1*(n["trust"]/100) + w2*n["reliability"] + w3*L

scored = [(n["id"], round(calc_score(n)*100, 1)) for n in eligible]
scored.sort(key=lambda x: x[1], reverse=True)

print("\nPlacement Decision:")
for s in scored:
    print(f"{s[0]} → Score: {s[1]}")
print(f"\n✅ Node selected for placement: {scored[0][0]} (Score={scored[0][1]})")
