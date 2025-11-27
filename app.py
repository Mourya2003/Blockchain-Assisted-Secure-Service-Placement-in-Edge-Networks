# app.py
import streamlit as st
import pandas as pd
import time
import random
from config import *

# IMPORT YOUR RESEARCH ARCHITECTURE
from components.blockchain import Blockchain
from components.edge_node import EdgeNode
from components.trust_manager import TrustManager
from components.placement_controller import PlacementController

# IMPORT PRODUCT MODULES
from product.traffic_monitor import TrafficCamera
from product.violation_detector import ViolationDetector
from product.evidence_validator import EvidenceValidator

# ==========================================
# SYSTEM INITIALIZATION
# ==========================================
st.set_page_config(page_title="TrafficGuard Ops", page_icon="🚦", layout="wide")

if 'initialized' not in st.session_state:
    # 1. Initialize Core Research Architecture
    blockchain = Blockchain()
    for validator in VALIDATORS:
        blockchain.add_validator(validator)
    
    trust_manager = TrustManager()
    placement_controller = PlacementController(blockchain)
    
    # 2. Initialize Product Layers
    violation_detector = ViolationDetector(blockchain, trust_manager)
    evidence_validator = EvidenceValidator(blockchain)
    
    # 3. Create Camera Nodes
    cameras = {}
    camera_nodes = []
    
    # We initialize nodes with realistic random history
    for cam_id, cam_info in CAMERA_LOCATIONS.items():
        cameras[cam_id] = TrafficCamera(cam_id, cam_info['location'], cam_info['type'])
        
        # Create Blockchain Node
        node = EdgeNode(cam_id, initial_trust=random.randint(65, 95))
        
        # Simulate History (CRITICAL FIX: Ensure math is consistent)
        node.total_tasks = random.randint(50, 150)
        node.success_count = int(node.total_tasks * random.uniform(0.8, 0.98))
        node.failure_count = node.total_tasks - node.success_count # <--- This prevents crashes
        
        camera_nodes.append(node)
    
    # Store in Session
    st.session_state.update({
        'initialized': True,
        'blockchain': blockchain,
        'trust_manager': trust_manager,
        'placement_controller': placement_controller,
        'violation_detector': violation_detector,
        'evidence_validator': evidence_validator,
        'cameras': cameras,
        'camera_nodes': camera_nodes,
        'violation_log': []
    })

# ==========================================
# DASHBOARD HEADER
# ==========================================
st.title("🚦 TrafficGuard: Decentralized Infrastructure Security")
st.markdown("**Product Engineering Lab Demo** | Powered by *Blockchain Trust Middleware*")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Active Traffic Units", len(st.session_state.camera_nodes))
with col2: st.metric("Court-Admissible Units", sum(1 for n in st.session_state.camera_nodes if n.trust_score >= 70))
with col3: st.metric("Blockchain Status", "✅ SECURE" if st.session_state.blockchain.is_chain_valid() else "❌ ERROR")
with col4: st.metric("Violations Processed", len(st.session_state.violation_log))

st.markdown("---")

# ==========================================
# 1. LIVE INFRASTRUCTURE GRID
# ==========================================
st.subheader("📡 Live Infrastructure Status")
cols = st.columns(3)
for idx, node in enumerate(st.session_state.camera_nodes):
    with cols[idx % 3]:
        # Visual Logic
        if node.trust_score >= EVIDENCE_TRUST_THRESHOLD:
            color = "#00ff00"; status = "🟢 SECURE"
        elif node.trust_score >= DEPLOYMENT_TRUST_THRESHOLD:
            color = "#ffaa00"; status = "🟡 WARNING"
        else:
            color = "#ff0000"; status = "🔴 COMPROMISED"
            
        cam = CAMERA_LOCATIONS[node.node_id]
        
        st.markdown(f"""
        <div style="border: 1px solid {color}; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #0E1117;">
            <div style="display:flex; justify-content:space-between;">
                <strong>{node.node_id}</strong>
                <span style="color:{color}">{status}</span>
            </div>
            <div style="font-size:0.8em; color:#aaa; margin-bottom:8px;">{cam['location']}</div>
            <div style="font-size:1.5em; font-weight:bold; color:{color}">{node.trust_score:.1f}%</div>
            <div style="font-size:0.8em;">Success Rate: {(node.success_count/node.total_tasks*100):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 2. PRODUCT FEATURES (The "Real World" Part)
# ==========================================
st.markdown("---")
tab1, tab2 = st.tabs(["🚨 Violation Detection", "🤖 AI Service Deployment"])

# --- TAB 1: TRAFFIC VIOLATIONS (The Product) ---
with tab1:
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.write("#### Simulator Controls")
        sel_id = st.selectbox("Select Unit", list(st.session_state.cameras.keys()))
        sel_cam = st.session_state.cameras[sel_id]
        sel_node = next(n for n in st.session_state.camera_nodes if n.node_id == sel_id)
        
        if st.button("📸 Trigger Traffic Event", type="primary"):
            # 1. Product Layer: Capture Data
            data, valid = sel_cam.capture_violation()
            
            # 2. Research Layer: Update Trust
            accepted, msg = st.session_state.violation_detector.process_violation(sel_node, data, valid)
            
            # 3. Product Layer: Validate Evidence
            admissible, report = st.session_state.evidence_validator.validate_evidence_chain(sel_node, data)
            
            # Log
            st.session_state.violation_log.append({
                "Time": data['timestamp'], "Unit": sel_id, "Type": data['violation_type'],
                "Evidence Status": "✅ Admissible" if admissible else "❌ Rejected"
            })
            
            if admissible:
                st.success("Violation Processed & Signed.")
            else:
                st.error(f"Evidence Rejected: {msg}")

        if st.button("💀 Simulate Cyber Attack"):
            st.session_state.trust_manager.update_trust(sel_node, False)
            st.session_state.blockchain.add_block(f"SECURITY_ALERT: {sel_id} Compromised")
            st.warning("Attack detected! Trust score penalized.")

    with col_right:
        st.write("#### Processed Violations Log")
        if st.session_state.violation_log:
            st.dataframe(pd.DataFrame(st.session_state.violation_log).tail(5), use_container_width=True)
        else:
            st.info("System Idle. Waiting for traffic events...")

# --- TAB 2: SERVICE PLACEMENT (The RP Logic Integration) ---
with tab2:
    st.write("#### 🚀 Autonomous Service Orchestrator")
    st.info("This module uses the **Placement Controller** (RP Logic) to move AI workloads to the safest nodes.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        service_type = st.selectbox("Select Service", ["Accident_Detection_AI", "Traffic_Flow_Optimizer", "Emergency_Vehicle_Green_Wave"])
        
        if st.button("Deploy Service"):
            with st.spinner("Auditing Network Trust..."):
                time.sleep(1)
                # CALLING YOUR PLACEMENT CONTROLLER
                best_node, msg = st.session_state.placement_controller.request_placement(st.session_state.camera_nodes)
                
                if best_node:
                    st.success(f"**Deployment Successful!**")
                    st.success(f"Target: **{best_node.node_id}**")
                    st.write(f"Security Score: **{best_node.trust_score:.2f}**")
                    st.write(f"Location: *{CAMERA_LOCATIONS[best_node.node_id]['location']}*")
                    st.caption("Decision Logic: Trust(50%) + Reliability(30%) + Resources(20%)")
                else:
                    st.error(msg)
    
    with col_b:
        with st.expander("🔍 View Blockchain Audit Trail", expanded=True):
            for b in st.session_state.blockchain.chain[-5:]:
                st.text(f"Block #{b.index} [{b.validator_id}]: {b.data[:60]}...")