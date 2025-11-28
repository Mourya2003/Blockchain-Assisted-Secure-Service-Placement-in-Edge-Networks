# app.py
import streamlit as st
import pandas as pd
import time
import random
from config import *

# IMPORT ARCHITECTURE
from components.blockchain import Blockchain
from components.edge_node import EdgeNode
from components.trust_manager import TrustManager
from components.placement_controller import PlacementController

# IMPORT PRODUCT LAYERS
from product.traffic_monitor import TrafficCamera
from product.violation_detector import ViolationDetector
from product.evidence_validator import EvidenceValidator

# ==========================================
# SYSTEM SETUP
# ==========================================
st.set_page_config(page_title="TrafficGuard Enterprise", page_icon="🚦", layout="wide")

if 'initialized' not in st.session_state:
    blockchain = Blockchain()
    for v in VALIDATORS: blockchain.add_validator(v)
    
    trust_manager = TrustManager()
    placement_controller = PlacementController(blockchain)
    violation_detector = ViolationDetector(blockchain, trust_manager)
    evidence_validator = EvidenceValidator(blockchain)
    
    # Create 6 Cameras
    cameras = {}
    camera_nodes = []
    for cam_id, cam_info in CAMERA_LOCATIONS.items():
        cameras[cam_id] = TrafficCamera(cam_id, cam_info['location'], cam_info['type'])
        node = EdgeNode(cam_id, initial_trust=random.randint(65, 95))
        node.total_tasks = random.randint(50, 150)
        node.success_count = int(node.total_tasks * random.uniform(0.85, 0.99))
        node.failure_count = node.total_tasks - node.success_count
        camera_nodes.append(node)
    
    st.session_state.update({
        'initialized': True,
        'blockchain': blockchain,
        'trust_manager': trust_manager,
        'placement_controller': placement_controller,
        'violation_detector': violation_detector,
        'cameras': cameras,
        'camera_nodes': camera_nodes,
        'violation_log': []
    })

# ==========================================
# HEADER
# ==========================================
st.title("🚦 TrafficGuard: Priority-Based Security")
st.markdown("**Enterprise Edition** | `Gas Fee Prioritization` | `Mempool Sorting`")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Active Cameras", len(st.session_state.camera_nodes))
with col2: 
    pending_count = len(st.session_state.blockchain.pending_transactions)
    st.metric("Mempool (Pending)", f"{pending_count} Txns", delta_color="inverse")
with col3: st.metric("Blockchain Height", len(st.session_state.blockchain.chain))

st.markdown("---")

# ==========================================
# 1. TRAFFIC INJECTOR (WITH ATTACK OPTION)
# ==========================================
col_left, col_mid, col_right = st.columns([1, 1.5, 1])

with col_left:
    st.subheader("1. Inject Traffic")
    st.info("Simulate data packets. Use 'Corrupt Data' to test security.")
    
    sel_id = st.selectbox("Source Camera", list(st.session_state.cameras.keys()))
    sel_node = next(n for n in st.session_state.camera_nodes if n.node_id == sel_id)
    
    # PRIORITY SELECTOR
    priority_label = st.select_slider(
        "Select Data Priority", 
        options=list(PRIORITY_LEVELS.keys())
    )
    gas_fee = PRIORITY_LEVELS[priority_label]
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📤 Send Valid Data", type="primary", use_container_width=True):
            # 1. Update Trust (Success)
            st.session_state.trust_manager.update_trust(sel_node, True)
            
            # 2. Add to Mempool
            data_packet = f"{sel_id}: Standard_Telemetry | Status: VERIFIED"
            st.session_state.blockchain.add_transaction(data_packet, gas_fee)
            st.success(f"Queued (Gas: {gas_fee})")

    with col_b:
        if st.button("⚠️ Send Corrupt Data", type="secondary", use_container_width=True):
            # 1. Update Trust (Failure - Penalty Applied)
            new_trust = st.session_state.trust_manager.update_trust(sel_node, False)
            
            # 2. Add 'Attack' packet to Mempool
            data_packet = f"🚨 {sel_id}: MALFORMED_PACKET | HACK_ATTEMPT"
            st.session_state.blockchain.add_transaction(data_packet, gas_fee)
            st.error(f"Attack Queued! Trust Dropped.")

    # Emergency Button
    if st.button("🚑 EMERGENCY OVERRIDE (100 GAS)", use_container_width=True):
        st.session_state.trust_manager.update_trust(sel_node, True)
        data_packet = f"🚨 {sel_id}: CRITICAL ACCIDENT DETECTED"
        st.session_state.blockchain.add_transaction(data_packet, 100)
        st.warning("CRITICAL ALERT JUMPED TO FRONT OF QUEUE")

with col_mid:
    st.subheader("2. Mempool (Priority Queue)")
    st.caption("Transactions are sorted by Gas Fee (Highest First) before Mining.")
    
    pending = st.session_state.blockchain.pending_transactions
    if pending:
        # VISUALIZE SORTING
        display_list = sorted(pending, key=lambda x: -x['gas'])
        
        for txn in display_list[:6]:
            if txn['gas'] >= 20: icon = "🔥"; color="red"
            elif txn['gas'] >= 5: icon = "⚡"; color="orange"
            else: icon = "📄"; color="grey"
            
            st.code(f"{icon} [Gas: {txn['gas']:03}] {txn['data']} ({txn['formatted_time']})")
            
        if len(pending) > 6: st.caption(f"...and {len(pending)-6} low-priority items waiting.")
        
        if st.button("⛏️ MINE BLOCK (Process High Priority)", type="primary", use_container_width=True):
            with st.spinner("Validator selecting highest fees..."):
                time.sleep(1)
                # UPDATED CALL
                new_block, leftovers = st.session_state.blockchain.mine_pending_block()
                
                st.success(f"Block #{new_block.index} Mined! (Capacity: 3 Txns)")
                if leftovers > 0:
                    st.warning(f"{leftovers} Low-Gas Transactions left in Mempool (Congestion).")
                else:
                    st.info("Mempool Cleared.")
                st.balloons()
    else:
        st.info("Mempool Empty.")

with col_right:
    st.subheader("3. Live Trust Scores")
    for node in st.session_state.camera_nodes:
        if node.trust_score >= 70: color = "green"
        elif node.trust_score >= 50: color = "orange"
        else: color = "red"
        st.markdown(f"**{node.node_id}**: <span style='color:{color}'>{node.trust_score:.1f}</span>", unsafe_allow_html=True)
        st.progress(min(int(node.trust_score), 100))

# ==========================================
# 2. AI DEPLOYMENT
# ==========================================
st.markdown("---")
st.subheader("🚀 Service Deployment (Research Core)")
if st.button("Run Placement Controller"):
    best, msg = st.session_state.placement_controller.request_placement(st.session_state.camera_nodes)
    if best: 
        st.success(f"Deployed to {best.node_id}")
        st.json({
            "Target Node": best.node_id,
            "Trust Score": f"{best.trust_score:.1f}",
            "Consensus": "Placement Logged on Chain"
        })
    else: 
        st.error(msg)

# ==========================================
# 3. LEDGER AUDIT (THE UPGRADE YOU ASKED FOR)
# ==========================================
with st.expander("🔍 View Immutable Blockchain Ledger", expanded=True):
    st.write("### Cryptographic Audit Trail")
    
    # Create a nice clean table for the ledger
    chain_data = []
    for b in st.session_state.blockchain.chain:
        chain_data.append({
            "Block #": b.index,
            "Timestamp": b.timestamp,
            "Validator Authority": b.validator_id,
            "SHA-256 Hash": b.hash,  # <--- HERE IS THE HASH
            "Data Payload": b.data
        })
    
    # Display as a rich interactive dataframe
    st.dataframe(
        pd.DataFrame(chain_data),
        column_config={
            "Block #": st.column_config.NumberColumn(format="%d"),
            "SHA-256 Hash": st.column_config.TextColumn(width="medium"),
            "Data Payload": st.column_config.TextColumn(width="large"),
        },
        use_container_width=True,
        hide_index=True
    )