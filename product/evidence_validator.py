# product/evidence_validator.py
"""
Evidence Validation System
Determines which camera footage is legally admissible
"""
from config import EVIDENCE_TRUST_THRESHOLD

class EvidenceValidator:
    """Validates if camera evidence meets legal standards"""
    
    def __init__(self, blockchain):
        self.blockchain = blockchain
        
    def validate_evidence_chain(self, camera_node, violation_data):
        """
        Validates complete chain of custody for evidence
        Returns: (is_valid, validation_report)
        """
        # Check 1: Camera Trust
        trust_check = camera_node.trust_score >= EVIDENCE_TRUST_THRESHOLD
        
        # Check 2: Blockchain Verification
        chain_valid = self.blockchain.is_chain_valid()
        
        # Check 3: Camera History (must have >80% success rate)
        reliability = (camera_node.success_count / camera_node.total_tasks 
                      if camera_node.total_tasks > 0 else 0)
        history_check = reliability >= 0.80
        
        # Generate Report
        report = {
            "camera_id": camera_node.node_id,
            "trust_score": camera_node.trust_score,
            "trust_check": "✅ PASS" if trust_check else "❌ FAIL",
            "blockchain_integrity": "✅ PASS" if chain_valid else "❌ FAIL",
            "reliability": f"{reliability*100:.1f}%",
            "history_check": "✅ PASS" if history_check else "❌ FAIL",
            "admissible": trust_check and chain_valid and history_check
        }
        
        # Log validation to blockchain
        result = "EVIDENCE_ACCEPTED" if report['admissible'] else "EVIDENCE_REJECTED"
        self.blockchain.add_block(
            f"{result} | Camera: {camera_node.node_id} | "
            f"Violation: {violation_data['violation_type']}"
        )
        
        return report['admissible'], report