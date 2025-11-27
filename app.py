# app.py - COMPLETE REWRITE
"""
TrafficGuard: Blockchain-Secured Evidence Management System
Real product that uses your research architecture
"""
import streamlit as st
import pandas as pd
import time
import random
from config import *
from product.traffic_monitor import TrafficCamera
from product.violation_detector import ViolationDetector
from product.evidence_validator import EvidenceValidator

# Import your RESEARCH components (unchanged)
from components.blockchain import Blockchain
from components.edge_node import EdgeNode
from components.trust_manager import TrustManager
from components.placement_controller import PlacementController

# ==========================================
# SYSTEM INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="TrafficGuard Evidence System",
    page_icon="🚦",
    layout="wide"
)

if 'initialized' not in st.session_state:
    # Core blockchain system (your research)
    blockchain = Blockchain()
    for validator in VALIDATORS:
        blockchain.add_validator(validator)
    
    trust_manager = TrustManager()
    placement_controller = PlacementController(blockchain)
    
    # Product layer (new)
    violation_detector = ViolationDetector(blockchain, trust_manager)
    evidence_validator = EvidenceValidator(blockchain)
    
    # Create camera network
    cameras = {}
    camera_nodes = []
    
    for cam_id, cam_info in CAMERA_LOCATIONS.items():
        # Create product camera
        cameras[cam_id] = TrafficCamera(
            cam_id, 
            cam_info['location'], 
            cam_info['type']
        )
        
        # Create blockchain node for this camera
        node = EdgeNode(cam_id, initial_trust=random.randint(60, 95))
        node.total_tasks = random.randint(50, 150)
        node.success_count = int(node.total_tasks * random.uniform(0.7, 0.95))
        camera_nodes.append(node)
    
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
# MAIN DASHBOARD
# ==========================================
st.title("🚦 TrafficGuard: Evidence Management System")
st.markdown("### Blockchain-Secured Traffic Violation Processing")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_cams = len(st.session_state.camera_nodes)
    st.metric("Active Cameras", total_cams)
with col2:
    trusted_cams = sum(1 for n in st.session_state.camera_nodes 
                       if n.trust_score >= EVIDENCE_TRUST_THRESHOLD)
    st.metric("Court-Admissible Cameras", trusted_cams)
with col3:
    st.metric("Blockchain Integrity", 
              "✅ Valid" if st.session_state.blockchain.is_chain_valid() else "❌ Compromised")
with col4:
    st.metric("Total Violations Processed", len(st.session_state.violation_log))

st.markdown("---")

# Camera Network Status
st.subheader("📷 Camera Network Status")
cols = st.columns(3)
for idx, node in enumerate(st.session_state.camera_nodes):
    with cols[idx % 3]:
        # Determine status
        if node.trust_score >= EVIDENCE_TRUST_THRESHOLD:
            status = "🟢 EVIDENCE-GRADE"
            color = "#00ff00"
            bg = "#113311"
        elif node.trust_score >= DEPLOYMENT_TRUST_THRESHOLD:
            status = "🟡 MONITORING ONLY"
            color = "#ffaa00"
            bg = "#332200"
        else:
            status = "🔴 COMPROMISED"
            color = "#ff0000"
            bg = "#330000"
        
        cam_info = CAMERA_LOCATIONS[node.node_id]
        reliability = (node.success_count / node.total_tasks * 100 
                      if node.total_tasks > 0 else 0)
        
        st.markdown(f"""
        <div style="border: 2px solid {color}; padding: 15px; border-radius: 8px; 
                    background-color: {bg}; margin-bottom: 15px;">
            <h4 style="margin:0; color:white;">{node.node_id}</h4>
            <p style="margin:5px 0; font-size:0.9em; color:#ccc;">{cam_info['location']}</p>
            <p style="margin:5px 0; font-size:0.85em; color:#ccc;">{cam_info['type']}</p>
            <hr style="border-color:#555; margin:10px 0;">
            <p style="margin:0; font-size:1.2em; color:{color};"><strong>Trust: {node.trust_score:.1f}%</strong></p>
            <p style="margin:5px 0; font-size:0.9em; color:#ccc;">Reliability: {reliability:.1f}%</p>
            <p style="margin:5px 0; font-size:0.9em; color:{color};"><strong>{status}</strong></p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Violation Processing Simulator
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🚨 Live Violation Detection")
    
    selected_cam_id = st.selectbox(
        "Select Camera", 
        list(st.session_state.cameras.keys()),
        format_func=lambda x: f"{x} - {CAMERA_LOCATIONS[x]['location']}"
    )
    
    selected_camera = st.session_state.cameras[selected_cam_id]
    selected_node = next(n for n in st.session_state.camera_nodes 
                        if n.node_id == selected_cam_id)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📸 Capture Violation", use_container_width=True):
            # Simulate real camera capture
            violation_data, is_valid = selected_camera.capture_violation()
            
            if violation_data:
                # Process through your research system
                accepted, reason = st.session_state.violation_detector.process_violation(
                    selected_node, violation_data, is_valid
                )
                
                # Validate for court evidence
                is_admissible, report = st.session_state.evidence_validator.validate_evidence_chain(
                    selected_node, violation_data
                )
                
                # Store result
                st.session_state.violation_log.append({
                    'timestamp': violation_data['timestamp'],
                    'camera': selected_cam_id,
                    'violation': violation_data['violation_type'],
                    'plate': violation_data['vehicle_plate'],
                    'valid_capture': is_valid,
                    'admissible': is_admissible,
                    'trust_after': selected_node.trust_score
                })
                
                # Display result
                if is_admissible:
                    st.success(f"✅ EVIDENCE ACCEPTED")
                    st.info(f"**Violation:** {violation_data['violation_type']}\n\n"
                           f"**Vehicle:** {violation_data['plate']}\n\n"
                           f"**Status:** Court-admissible evidence")
                else:
                    st.warning(f"⚠️ EVIDENCE REJECTED")
                    st.error(f"**Reason:** {report['trust_check']} Trust Check\n\n"
                            f"**Current Trust:** {report['trust_score']:.1f}%")
    
    with col_b:
        if st.button("🔨 Simulate Camera Hack", use_container_width=True):
            # Simulate malicious activity
            tamper_data = selected_camera.simulate_tampering()
            
            # Process as failure
            st.session_state.trust_manager.update_trust(selected_node, False)
            st.session_state.blockchain.add_block(
                f"SECURITY_ALERT | {selected_cam_id} | Unauthorized access detected"
            )
            
            st.error(f"🚨 SECURITY BREACH DETECTED\n\n"
                    f"Camera {selected_cam_id} has been compromised!\n\n"
                    f"Trust Score: {selected_node.trust_score:.1f}% (Dropped)")

with col_right:
    st.subheader("📊 Recent Activity")
    if st.session_state.violation_log:
        df = pd.DataFrame(st.session_state.violation_log)
        st.dataframe(df[['timestamp', 'camera', 'violation', 'admissible', 'trust_after']], 
                    use_container_width=True)
    else:
        st.info("No violations processed yet")

# Evidence Validation Report
st.markdown("---")
st.subheader("⚖️ Evidence Validation Report")
if st.button("Generate Court Report"):
    with st.spinner("Validating camera network..."):
        time.sleep(1)
        
        report_data = []
        for node in st.session_state.camera_nodes:
            is_valid, report = st.session_state.evidence_validator.validate_evidence_chain(
                node, {'violation_type': 'System Check'}
            )
            report_data.append(report)
        
        st.dataframe(pd.DataFrame(report_data), use_container_width=True)

# Blockchain Audit Trail
with st.expander("🔍 View Blockchain Audit Trail"):
    st.write("**Immutable Evidence Chain**")
    for block in st.session_state.blockchain.chain:
        st.text(f"Block #{block.index} | Validator: {block.validator_id}\n"
               f"Data: {block.data}\n"
               f"Hash: {block.hash[:32]}...\n")