import time

class PlacementController:
    """
    Implements the Service Placement Logic.
    Process: Filter -> Rank -> Select -> Record
    """
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.trust_threshold = 60.0
        
        # Weights for the Placement Score Formula
        # w1 (Trust) + w2 (Reliability) + w3 (Resources) = 1.0
        self.w1 = 0.5 
        self.w2 = 0.3 
        self.w3 = 0.2 

    def request_placement(self, nodes):
        """
        Selects the best node for a high-priority service.
        Returns: (Selected_Node, Success_Message)
        """
        # 1. SECURITY FILTER: Reject malicious nodes immediately
        eligible_nodes = [n for n in nodes if n.trust_score >= self.trust_threshold]
        
        if not eligible_nodes:
            # Log failure to blockchain
            self.blockchain.add_block("PLACEMENT_FAILURE: No trusted nodes available.")
            return None, "CRITICAL FAILURE: All nodes are untrusted (<60)."

        # 2. RANKING ALGORITHM: Calculate Score for each eligible node
        ranked_nodes = []
        for node in eligible_nodes:
            # Calculate Reliability (R)
            reliability = node.success_count / node.total_tasks if node.total_tasks > 0 else 0
            
            # Resource Score (Simulated as 1.0 for this demo)
            resource_score = 1.0 
            
            # FINAL FORMULA: Score = w1*T + w2*R + w3*L
            score = (self.w1 * (node.trust_score/100.0)) + \
                    (self.w2 * reliability) + \
                    (self.w3 * resource_score)
            
            ranked_nodes.append((node, score))

        # 3. SELECTION: Pick the highest score
        ranked_nodes.sort(key=lambda x: x[1], reverse=True)
        best_node, final_score = ranked_nodes[0]

        # 4. AUDIT: Record the decision on the Blockchain
        txn_data = f"DEPLOY_SUCCESS: Assigned to {best_node.node_id} (Score: {final_score:.2f})"
        self.blockchain.add_block(txn_data)

        return best_node, f"Service Deployed to {best_node.node_id}"