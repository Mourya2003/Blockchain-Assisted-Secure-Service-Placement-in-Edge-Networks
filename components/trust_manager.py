import time

class TrustManager:
    """
    Implements the Recency-Weighted Trust Formula.
    Formula: Ti = alpha*S + beta*A - gamma*F + delta*R
    """
    def __init__(self):
        # Hyperparameters (Tuned via Heuristic Analysis)
        self.alpha = 5.0   # Reward for Success
        self.beta = 3.0    # Weight for Recency (Activity)
        self.gamma = 10.0  # Penalty for Failure (Security First)
        self.delta = 2.0   # Reward for Consistency (Reliability)

    def calculate_recency(self, last_active_time):
        """Calculates the Activity Factor (A)"""
        current_time = time.time()
        time_diff = current_time - last_active_time
        # Decay logic: Trust fades if inactive for > 1 hour (3600s)
        # Result is between 0.5 and 1.0
        return max(0.5, 1.0 - (time_diff / 3600))

    def update_trust(self, node, is_success):
        """
        Updates the node's trust score.
        Returns: The new trust score.
        """
        # 1. Update Metrics
        node.total_tasks += 1
        if is_success:
            node.success_count += 1
        else:
            node.failure_count += 1
            
        # 2. Calculate Terms
        recency_factor = self.calculate_recency(node.last_activity_time)
        reliability = node.success_count / node.total_tasks
        
        # 3. Apply The Linear Formula
        if is_success:
            # Reward: Alpha * Recency + Delta * Reliability
            change = (self.alpha * recency_factor) + (self.delta * reliability)
            node.trust_score = min(100.0, node.trust_score + change)
        else:
            # Penalty: Gamma (Immediate drop)
            node.trust_score = max(0.0, node.trust_score - self.gamma)
            
        # Update timestamp
        node.last_activity_time = time.time()
        
        return node.trust_score