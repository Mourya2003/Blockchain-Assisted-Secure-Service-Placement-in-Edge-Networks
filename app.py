import streamlit as st
import pandas as pd
import random
import time

# IMPORT YOUR RESEARCH ARCHITECTURE (Same Backend!)
from components.blockchain import Blockchain
from components.edge_node import EdgeNode
from components.trust_manager import TrustManager
from components.placement_controller import PlacementController

# ==========================================
# 1. SYSTEM INITIALIZATION (The Backend)
# ==========================================
st.set_page_config(page_title="CityGuard Traffic Ops", layout="wide")

if 'system_initialized' not in st.session_state:
    # A. Initialize Blockchain
    blockchain = Blockchain()
    validators = ["City_Hall_Server", "Traffic_Control_HQ", "Police_Dept_Node"]
    for v in validators: blockchain.add_validator(v)
    
    # B. Initialize Logic
    trust_manager = TrustManager()
    placement_controller = PlacementController(blockchain)
    
    # C. Create SMART CITY NODES (Rebranded)
    nodes = []
    
    # High Trust Cameras
    n1 = EdgeNode("Cam-Main-St", initial_trust=95); n1.total_tasks=100; n1.success_count=98; nodes.append(n1)
    n2 = EdgeNode("Signal-5th-Ave", initial_trust=88); n2.total_tasks=80; n2.success_count=75; nodes.append(n2)
    n3 = EdgeNode("Sensor-Hwy-101", initial_trust=92); n3.total_tasks=120; n3.success_count=118; nodes.append(n3)
    
    # The "Glitchy" Camera
    n4 = EdgeNode("Cam-River-Rd", initial_trust=65); n4.total_tasks=40; n4.success_count=30; nodes.append(n4)
    
    # The "Compromised" Unit (Sleeper)
    n5 = EdgeNode("Signal-West-End", initial_trust=55); n5.total_tasks=20; n5.success_count=12; nodes.append(n5)
    
    # The "Hacked" Unit
    n6 = EdgeNode("Cam-Market-Sq", initial_trust=45); n6.total_tasks=60; n6.success_count=25; nodes.append(n6)

    st.session_state.blockchain = blockchain
    st.session_state.trust_manager = trust_manager
    st.session_state.placement_controller = placement_controller
    st.session_state.nodes = nodes
    st.session_state.system_initialized = True
    
    # Chart Data
    st.session_state.chart_data = pd.DataFrame(columns=[n.node_id for n in nodes])

# ==========================================
# 2. SIDEBAR - TRAFFIC SIMULATOR
# ==========================================
st.sidebar.header("🚦 Traffic Simulation")
st.sidebar.write("Inject Event Stream:")

# Select Unit
target_id = st.sidebar.selectbox("Select Traffic Unit", [n.node_id for n in st.session_state.nodes])
target_node = next(n for n in st.session_state.nodes if n.node_id == target_id)

# Select Scenario
scenario = st.sidebar.radio("Data Stream Integrity", ["VALID DATA (Normal)", "CORRUPTED (Hack Attempt)"])

if st.sidebar.button("📡 Transmit Data Packet"):
    is_success = (scenario == "VALID DATA (Normal)")
    
    # 1. REAL LOGIC (Same Code!)
    old_score = target_node.trust_score
    new_score = st.session_state.trust_manager.update_trust(target_node, is_success)
    
    # 2. BLOCKCHAIN LOG
    status_str = "VERIFIED" if is_success else "TAMPERED"
    txn = f"UNIT: {target_node.node_id} | DATA: {status_str} | TIMESTAMP: {time.time()}"
    block = st.session_state.blockchain.add_block(txn)
    
    # 3. FEEDBACK
    if is_success:
        st.sidebar.success(f"Packet Verified. Integrity Score: {new_score:.1f}")
    else:
        st.sidebar.error(f"🚨 ANOMALY DETECTED! Integrity Score Dropped: {new_score:.1f}")
    
    # 4. UPDATE CHART
    new_row = {n.node_id: n.trust_score for n in st.session_state.nodes}
    st.session_state.chart_data = pd.concat([st.session_state.chart_data, pd.DataFrame([new_row])], ignore_index=True)

st.sidebar.markdown("---")
st.sidebar.info(f"**Ledger Height:** {len(st.session_state.blockchain.chain)} Blocks")

# ==========================================
# 3. MAIN DASHBOARD - SMART CITY OPS
# ==========================================
st.title("🏙️ CityGuard: Traffic Infrastructure Security")
st.markdown("### 🟢 Live Infrastructure Status")

# A. NODE GRID
cols = st.columns(3)
for i, node in enumerate(st.session_state.nodes):
    with cols[i % 3]:
        # Determine Color based on Trust
        if node.trust_score >= 60:
            color = "#00ff00"; bg="#113311"; icon = "✅ ONLINE"
        elif node.trust_score >= 40:
            color = "orange"; bg="#332200"; icon = "⚠️ UNSTABLE"
        else:
            color = "red"; bg="#330000"; icon = "🚫 COMPROMISED"
            
        st.markdown(f"""
        <div style="border: 1px solid {color}; padding: 15px; border-radius: 5px; margin-bottom: 10px; background-color: {bg};">
            <h4 style="margin:0; color:white;">📷 {node.node_id}</h4>
            <p style="margin:0; font-size: 1.1em; color: {color};"><strong>Integrity: {node.trust_score:.1f}%</strong></p>
            <p style="margin:0; font-size: 0.8em; color: #ccc;">Uptime: {node.total_tasks} hrs | {icon}</p>
        </div>
        """, unsafe_allow_html=True)

# B. CRITICAL SERVICE DEPLOYMENT
st.markdown("---")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚑 Emergency AI Deployment")
    st.write("Deploy **'Ambulance_Green_Wave_AI'** to the most secure intersection controller.")
    
    if st.button("🚀 Deploy Critical Traffic Model"):
        with st.spinner("Auditing Infrastructure Security..."):
            time.sleep(1.5)
            
            # CALL PLACEMENT CONTROLLER
            selected, msg = st.session_state.placement_controller.request_placement(st.session_state.nodes)
            
            if selected:
                st.success(f"**DEPLOYMENT SUCCESSFUL**")
                st.write(f"Target: **{selected.node_id}**")
                st.write(f"Security Rating: **{selected.trust_score:.1f}** (Highest Available)")
                st.info("The system automatically bypassed compromised units (Red/Orange).")
            else:
                st.error(msg)

with col2:
    st.subheader("📉 Integrity Evolution")
    if not st.session_state.chart_data.empty:
        st.line_chart(st.session_state.chart_data)
    else:
        st.info("Waiting for telemetry data...")

# C. AUDIT LOG
with st.expander("👮 View Forensic Ledger (Blockchain Audit Trail)"):
    chain_data = []
    for b in st.session_state.blockchain.chain:
        chain_data.append({
            "Block ID": b.index,
            "Validator Authority": b.validator_id,
            "Event Log": b.data,
            "Cryptographic Hash": b.hash
        })
    st.dataframe(pd.DataFrame(chain_data))