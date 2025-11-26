import streamlit as st
import time
import pandas as pd
from blockchain import Blockchain
from edge_node import EdgeNode

# ==========================================
# 1. SETUP & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="EdgeGuard Sentinel", layout="wide")

# We need to keep the Blockchain alive in memory when you click buttons
if 'blockchain' not in st.session_state:
    # Initialize the Real Backend
    bc = Blockchain()
    validators = ["Admin_Server", "ISP_Gateway", "City_Council"]
    for v in validators:
        bc.add_validator(v)
    
    st.session_state.blockchain = bc
    
    # Create the Virtual Nodes
    nodes = [
        EdgeNode("Node-1"), # High Trust
        EdgeNode("Node-2"), # Average
        EdgeNode("Node-3"), # Malicious (will act bad)
        EdgeNode("Node-4")  # Powerful but untrusted
    ]
    # Set initial trust scores for the demo
    nodes[0].trust_score = 80
    nodes[2].trust_score = 45 
    nodes[3].trust_score = 55
    st.session_state.nodes = nodes
    
    # Keep track of trust history for the chart
    st.session_state.trust_history = pd.DataFrame(columns=[n.node_id for n in nodes])

# ==========================================
# 2. SIDEBAR - THE "CONTROL CENTER"
# ==========================================
st.sidebar.header("🛠️ Node Control Panel")
st.sidebar.write("Manually simulate edge behavior:")

# Control 1: Pick a Node
selected_node_id = st.sidebar.selectbox("Select Target Node", [n.node_id for n in st.session_state.nodes])
target_node = next(n for n in st.session_state.nodes if n.node_id == selected_node_id)

# Control 2: Force Outcome
outcome = st.sidebar.radio("Force Task Outcome", ["SUCCESS (Good Behavior)", "FAILURE (Malicious/Error)"])

# Control 3: Trigger Button
if st.sidebar.button("⚡ Run Simulation Task"):
    # Determine success
    is_success = True if "SUCCESS" in outcome else False
    
    # 1. RUN TRUST LOGIC (Your Code)
    target_node.update_trust(is_success)
    
    # 2. ADD TO BLOCKCHAIN (Your Code)
    status_text = "Success" if is_success else "Failure"
    txn_data = f"Task: {status_text} | Node: {target_node.node_id}"
    new_block = st.session_state.blockchain.add_block(txn_data)
    
    # 3. Update History for Chart
    new_row = {n.node_id: n.trust_score for n in st.session_state.nodes}
    st.session_state.trust_history = pd.concat([st.session_state.trust_history, pd.DataFrame([new_row])], ignore_index=True)
    
    if is_success:
        st.sidebar.success(f"Task Verified! Trust increased to {target_node.trust_score:.1f}")
    else:
        st.sidebar.error(f"Failure Detected! Penalty applied. Trust dropped to {target_node.trust_score:.1f}")

st.sidebar.markdown("---")

# ==========================================
# 3. MAIN DASHBOARD - "THE PRODUCT VIEW"
# ==========================================
st.title("🛡️ EdgeGuard Sentinel")
st.markdown("**Decentralized Trust & Service Placement Orchestrator**")

# --- Top Metrics Row ---
col1, col2, col3 = st.columns(3)
col1.metric("Active Nodes", len(st.session_state.nodes))
col2.metric("Consensus Protocol", "Proof-of-Authority (PoA)")
col3.metric("Blockchain Height", len(st.session_state.blockchain.chain))

# --- Section A: Network Visualization ---
st.subheader("📡 Live Network Status")
cols = st.columns(len(st.session_state.nodes))

for i, node in enumerate(st.session_state.nodes):
    with cols[i]:
        # Dynamic Color Logic
        if node.trust_score >= 60:
            color = "green"
            icon = "✅"
            status = "SECURE"
        elif node.trust_score >= 40:
            color = "orange"
            icon = "⚠️"
            status = "SUSPICIOUS"
        else:
            color = "red"
            icon = "🚫"
            status = "BLOCKED"
        
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; border-left: 5px solid {color};">
            <h4>{icon} {node.node_id}</h4>
            <p><strong>Trust:</strong> {node.trust_score:.1f}</p>
            <p><strong>Tasks:</strong> {node.total_tasks}</p>
            <p style="color:{color}; font-weight:bold;">{status}</p>
        </div>
        """, unsafe_allow_html=True)

# --- Section B: Service Placement Controller ---
st.markdown("---")
st.subheader("🤖 Service Placement Controller")

if st.button("🚀 Deploy High-Priority Service"):
    with st.spinner('Analyzing Trust Scores & Resources...'):
        time.sleep(1) # Fake loading for effect
        
        # YOUR PLACEMENT LOGIC
        candidates = [n for n in st.session_state.nodes if n.trust_score >= 60]
        
        if not candidates:
            st.error("❌ CRITICAL SECURITY ALERT: No trusted nodes available! Deployment Aborted.")
        else:
            best_node = max(candidates, key=lambda x: x.trust_score)
            
            # Show the Winner
            st.success(f"✅ Deployment Successful! Service assigned to **{best_node.node_id}**")
            
            # Show the Why (Transparency)
            st.info(f"**Decision Logic:** Node {best_node.node_id} selected because Trust ({best_node.trust_score:.1f}) > 60 and reliability is optimal.")
            
            # Log to Blockchain
            st.session_state.blockchain.add_block(f"DEPLOYMENT: Assigned to {best_node.node_id}")

# --- Section C: Trust Evolution Chart ---
st.subheader("📈 Trust Score Evolution")
if not st.session_state.trust_history.empty:
    st.line_chart(st.session_state.trust_history)
else:
    st.write("Waiting for simulation data...")

# --- Section D: Immutable Ledger ---
with st.expander("🔍 View Blockchain Ledger (Audit Trail)", expanded=False):
    chain_data = []
    for block in st.session_state.blockchain.chain:
        chain_data.append({
            "Index": block.index,
            "Timestamp": block.timestamp,
            "Validator": block.validator_id,
            "Data": block.data,
            "Hash": block.hash
        })
    st.dataframe(pd.DataFrame(chain_data))