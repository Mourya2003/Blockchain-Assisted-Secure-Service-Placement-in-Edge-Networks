import streamlit as st
import pandas as pd
import random
import time

# IMPORT YOUR RESEARCH ARCHITECTURE
from components.blockchain import Blockchain
from components.edge_node import EdgeNode
from components.trust_manager import TrustManager
from components.placement_controller import PlacementController

# ==========================================
# 1. SYSTEM INITIALIZATION (The Backend)
# ==========================================
st.set_page_config(page_title="EdgeGuard Research Demo", layout="wide")

if 'system_initialized' not in st.session_state:
    # A. Initialize Blockchain (The Ledger)
    blockchain = Blockchain()
    validators = ["Admin_Server", "ISP_Gateway", "City_Council"]
    for v in validators: blockchain.add_validator(v)
    
    # B. Initialize Logic Engines
    trust_manager = TrustManager()
    placement_controller = PlacementController(blockchain)
    
    # C. Create EXACTLY 6 Nodes (The Physical Layer)
    nodes = []
    # Nodes 1-3: High Performance, Good History
    for i in range(1, 4):
        n = EdgeNode(f"Node-{i}", initial_trust=random.randint(75, 95))
        n.total_tasks = random.randint(20, 50)
        n.success_count = n.total_tasks # 100% reliability start
        nodes.append(n)
        
    # Node 4: Average/Neutral
    n4 = EdgeNode("Node-4", initial_trust=65); n4.total_tasks=10; n4.success_count=8
    nodes.append(n4)
    
    # Node 5: The "Sleeper" (High resources, but barely trusted)
    n5 = EdgeNode("Node-5", initial_trust=55); n5.total_tasks=5; n5.success_count=3
    nodes.append(n5)
    
    # Node 6: The Malicious Node
    n6 = EdgeNode("Node-6", initial_trust=45); n6.total_tasks=50; n6.success_count=20
    nodes.append(n6)

    # Save to Session State (Memory)
    st.session_state.blockchain = blockchain
    st.session_state.trust_manager = trust_manager
    st.session_state.placement_controller = placement_controller
    st.session_state.nodes = nodes
    st.session_state.system_initialized = True
    
    # Chart Data
    st.session_state.chart_data = pd.DataFrame(columns=[n.node_id for n in nodes])

# ==========================================
# 2. SIDEBAR - THE "REALITY" CONTROLLER
# ==========================================
st.sidebar.header("⚡ Simulation Controls")
st.sidebar.write("Manually trigger edge events:")

# Select Node
target_id = st.sidebar.selectbox("Target Node", [n.node_id for n in st.session_state.nodes])
target_node = next(n for n in st.session_state.nodes if n.node_id == target_id)

# Select Outcome
outcome = st.sidebar.radio("Event Outcome", ["SUCCESS (Verify)", "FAILURE (Attack)"])

if st.sidebar.button("Run Transaction"):
    is_success = (outcome == "SUCCESS (Verify)")
    
    # 1. CALL TRUST MANAGER (Real Math)
    old_score = target_node.trust_score
    new_score = st.session_state.trust_manager.update_trust(target_node, is_success)
    
    # 2. LOG TO BLOCKCHAIN (Real Crypto)
    status_str = "SUCCESS" if is_success else "FAILURE"
    txn = f"TASK: {target_node.node_id} | Result: {status_str}"
    block = st.session_state.blockchain.add_block(txn)
    
    # 3. FEEDBACK
    if is_success:
        st.sidebar.success(f"Trust Increased: {old_score:.1f} -> {new_score:.1f}")
    else:
        st.sidebar.error(f"Penalty Applied: {old_score:.1f} -> {new_score:.1f}")
    
    # 4. UPDATE CHART
    new_row = {n.node_id: n.trust_score for n in st.session_state.nodes}
    st.session_state.chart_data = pd.concat([st.session_state.chart_data, pd.DataFrame([new_row])], ignore_index=True)

st.sidebar.markdown("---")
st.sidebar.info(f"**Blockchain Height:** {len(st.session_state.blockchain.chain)} Blocks")

# ==========================================
# 3. MAIN DASHBOARD
# ==========================================
st.title("🛡️ EdgeGuard: Secure Service Placement")
st.markdown("### Live Network Status (6 Nodes)")

# A. NODE GRID
cols = st.columns(3) # 2 Rows of 3
for i, node in enumerate(st.session_state.nodes):
    with cols[i % 3]:
        # Determine Color based on Trust Threshold (60)
        if node.trust_score >= 60:
            color = "green"
            icon = "✅ SECURE"
            border = "2px solid #28a745"
        elif node.trust_score >= 40:
            color = "orange"
            icon = "⚠️ RISKY"
            border = "2px solid #ffc107"
        else:
            color = "red"
            icon = "🚫 BANNED"
            border = "2px solid #dc3545"
            
        st.markdown(f"""
        <div style="border: {border}; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: #1e1e1e;">
            <h3 style="margin:0; color:white;">{node.node_id}</h3>
            <p style="margin:0; font-size: 1.2em; color: {color};"><strong>{node.trust_score:.1f}</strong></p>
            <p style="margin:0; font-size: 0.9em; color: #aaa;">Tasks: {node.total_tasks} | {icon}</p>
        </div>
        """, unsafe_allow_html=True)

# B. PLACEMENT CONTROLLER SECTION
st.markdown("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🤖 Placement Controller")
    st.write("Algorithm: `Filter(>60) -> Rank -> Select`")
    
    if st.button("🚀 Deploy Critical Service"):
        with st.spinner("Analyzing Trust Scores & Blockchain History..."):
            time.sleep(1) # UI Effect
            
            # CALL PLACEMENT CONTROLLER (Real Logic)
            selected, msg = st.session_state.placement_controller.request_placement(st.session_state.nodes)
            
            if selected:
                st.success(f"**DEPLOYED TO: {selected.node_id}**")
                st.info(f"Trust Score: {selected.trust_score:.1f}")
                st.caption(f"Transaction logged to Blockchain.")
            else:
                st.error(msg)

with col2:
    st.subheader("📈 Trust Evolution")
    if not st.session_state.chart_data.empty:
        st.line_chart(st.session_state.chart_data)
    else:
        st.info("Run simulations in the sidebar to see live data.")

# C. BLOCKCHAIN LEDGER
with st.expander("🔍 View Immutable Ledger (SHA-256 Hashes)"):
    chain_data = []
    for b in st.session_state.blockchain.chain:
        chain_data.append({
            "Block": b.index,
            "Validator": b.validator_id,
            "Data": b.data,
            "Hash": b.hash
        })
    st.dataframe(pd.DataFrame(chain_data))