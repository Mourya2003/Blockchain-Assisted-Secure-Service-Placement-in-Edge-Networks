import time

class EdgeNode:
    """
    Represents a physical Edge Node in the network.
    This class holds the STATE (Data), but not the LOGIC.
    """
    def __init__(self, node_id, initial_trust=50):
        self.node_id = node_id
        
        # Trust State
        self.trust_score = float(initial_trust)
        
        # Performance Metrics (S, F, Total)
        # --- FIXED VARIABLES BELOW ---
        self.success_count = 0 
        self.failure_count = 0
        self.total_tasks = 0
        
        # For Recency Calculation (A)
        self.last_activity_time = time.time()