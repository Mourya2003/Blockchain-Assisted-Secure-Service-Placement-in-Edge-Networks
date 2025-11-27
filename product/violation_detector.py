# product/violation_detector.py
"""
Violation Detection System
Uses blockchain trust to validate evidence
"""
from components.trust_manager import TrustManager

class ViolationDetector:
    """Processes violations and validates camera trustworthiness"""
    
    def __init__(self, blockchain, trust_manager):
        self.blockchain = blockchain
        self.trust_manager = trust_manager
        
    def process_violation(self, camera_node, violation_data, is_valid_capture):
        """
        Process a traffic violation capture
        Returns: (accepted, reason)
        """
        # Update camera trust based on capture quality
        new_trust = self.trust_manager.update_trust(camera_node, is_valid_capture)
        
        # Log to blockchain (immutable audit trail)
        log_entry = (f"VIOLATION_CAPTURE | Camera: {camera_node.node_id} | "
                    f"Type: {violation_data['violation_type']} | "
                    f"Valid: {is_valid_capture} | Trust: {new_trust:.1f}")
        
        self.blockchain.add_block(log_entry)
        
        # Decision logic
        if is_valid_capture:
            return True, "Evidence Accepted"
        else:
            return False, "Camera malfunction detected"
    
    def can_use_as_evidence(self, camera_node, threshold=70.0):
        """
        Determines if camera feed can be used as court evidence
        This is the KEY PRODUCT FEATURE
        """
        if camera_node.trust_score >= threshold:
            return True, "COURT-ADMISSIBLE"
        elif camera_node.trust_score >= 60:
            return False, "MONITORING ONLY - Trust too low for evidence"
        else:
            return False, "COMPROMISED - Camera disabled"