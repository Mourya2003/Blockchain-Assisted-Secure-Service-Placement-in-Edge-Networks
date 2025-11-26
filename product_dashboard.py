import time
import random
import os
from blockchain import Blockchain
from edge_node import EdgeNode

# --- Helper to clear screen for that "Dashboard" look ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("="*60)
    print("      EDGETRUST SENTINEL v1.0 - SECURE ORCHESTRATOR      ")
    print("="*60)
    print(f" System Status: \033[92mONLINE\033[0m")
    print(f" Consensus:     \033[96mPROOF-OF-AUTHORITY (PoA)\033[0m")
    print(f" Validators:    3 Active")
    print("-" * 60)

# --- Setup System ---
bc = Blockchain()
for v in ["NetAdmin_01", "CityCouncil_Node", "ISP_Gateway"]:
    bc.add_validator(v)

# Initialize Nodes with your specific scenarios
nodes = [
    EdgeNode("Node-1"), # Good node
    EdgeNode("Node-2"), # Average node
    EdgeNode("Node-3"), # Bad node
    EdgeNode("Node-4")  # High resource, low trust node
]
# Pre-set some values to make the demo interesting immediately
nodes[0].trust_score = 80  # Trusted
nodes[2].trust_score = 45  # Malicious
nodes[3].trust_score = 55  # Suspicious

# --- Simulation Functions ---
def show_nodes():
    print("\n[LIVE NETWORK STATUS]")
    print(f"{'Node ID':<10} | {'Trust':<10} | {'Status':<15} | {'Recent Act'}")
    print("-" * 55)
    for n in nodes:
        status = "\033[92mSECURE\033[0m" if n.trust_score >= 60 else "\033[91mBLOCKED\033[0m"
        print(f"{n.node_id:<10} | {n.trust_score:<10.1f} | {status:<24} | {time.strftime('%H:%M:%S')}")
    print("-" * 55)

def simulate_activity():
    print("\n[...] Simulating Network Traffic...")
    time.sleep(1)
    
    # Randomly pick a node to do a task
    target = random.choice(nodes)
    is_success = True
    
    # If it's Node-3 (Bad), make it fail often
    if target.node_id == "Node-3":
        is_success = random.choice([True, False, False]) # Mostly fails
    elif target.node_id == "Node-4":
        is_success = random.choice([True, False]) # Unstable
        
    # Update Trust Logic (Your Core Feature)
    target.update_trust(is_success)
    
    # Add to Blockchain
    txn_data = f"{target.node_id} Task {'Success' if is_success else 'Failure'}"
    new_block = bc.add_block(txn_data)
    
    status_color = "\033[92mSUCCESS\033[0m" if is_success else "\033[91mFAILURE\033[0m"
    print(f" > Event: {target.node_id} processed task -> {status_color}")
    print(f" > Blockchain: Block #{new_block.index} minted by {new_block.validator_id}")
    print(f" > Trust Score Updated: {target.trust_score:.1f}")
    input("\nPress Enter to continue...")

def deploy_service():
    print("\n[SERVICE DEPLOYMENT REQUEST]")
    print("Request: Deploy 'Traffic_Analysis_AI' (Req: High CPU)")
    time.sleep(1)
    
    # Your Service Placement Logic
    eligible = [n for n in nodes if n.trust_score >= 60]
    
    if not eligible:
        print("\033[91m[ALERT] Deployment Aborted: No trusted nodes available!\033[0m")
        return

    # Simple ranking simulation
    print(f"\n> Found {len(eligible)} trusted candidates.")
    best_node = max(eligible, key=lambda n: n.trust_score)
    
    print(f"> Analyzing Resources... Done.")
    print(f"> Selected Node: \033[92m{best_node.node_id}\033[0m (Trust: {best_node.trust_score:.1f})")
    
    # Log to blockchain
    bc.add_block(f"DEPLOYMENT: Service assigned to {best_node.node_id}")
    print("> Deployment recorded on Ledger.")
    input("\nPress Enter to continue...")

def view_ledger():
    print("\n[IMMUTABLE LEDGER AUDIT]")
    for block in bc.chain:
        print(f"[{block.index}] Hash: {block.hash[:10]}... | Data: {block.data}")
    input("\nPress Enter to continue...")

# --- Main Loop ---
while True:
    clear_screen()
    print_header()
    show_nodes()
    print("\nCOMMAND MENU:")
    print("1. Simulate Live Transaction (Update Trust)")
    print("2. Request Service Deployment (Placement Controller)")
    print("3. Audit Blockchain Ledger")
    print("4. Exit")
    
    choice = input("\nSelect Action [1-4]: ")
    
    if choice == '1':
        simulate_activity()
    elif choice == '2':
        deploy_service()
    elif choice == '3':
        view_ledger()
    elif choice == '4':
        print("Shutting down EdgeTrust Sentinel...")
        break