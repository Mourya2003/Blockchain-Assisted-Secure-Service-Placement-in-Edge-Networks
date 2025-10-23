class EdgeNode:
    """
    Represents an edge node in the network.
    Each node has resources, trust score, and task history.
    """
    
    def __init__(self, node_id, cpu_cores=4, memory_gb=8):
        """
        Initialize an edge node.
        
        Args:
            node_id (str): Unique identifier for the node
            cpu_cores (int): Available CPU cores
            memory_gb (int): Available memory in GB
        """
        self.node_id = node_id
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.trust_score = 50  # Initial trust (neutral)
        self.task_history = []
        self.status = "Active"
    
    def update_trust(self, success, event_description=""):
        """
        Update trust score based on task outcome.
        
        Args:
            success (bool): True if task succeeded, False if failed
            event_description (str): Description of the event
        """
        old_trust = self.trust_score
        
        if success:
            self.trust_score = min(self.trust_score + 5, 100)
            result = "SUCCESS"
        else:
            self.trust_score = max(self.trust_score - 10, 0)
            result = "FAILURE"
        
        # Record in history
        self.task_history.append({
            "result": result,
            "description": event_description,
            "old_trust": old_trust,
            "new_trust": self.trust_score
        })
        
        change = self.trust_score - old_trust
        sign = "+" if change > 0 else ""
        print(f"  {self.node_id}: {old_trust} → {self.trust_score} ({sign}{change}) [{result}]")
    
    def get_trust_level(self):
        """Return trust level category."""
        if self.trust_score >= 80:
            return "HIGH"
        elif self.trust_score >= 60:
            return "MEDIUM"
        elif self.trust_score >= 40:
            return "LOW"
        else:
            return "UNTRUSTED"
    
    def is_trustworthy(self, threshold=60):
        """Check if node meets trust threshold."""
        return self.trust_score >= threshold
    
    def __str__(self):
        """String representation of the node."""
        return (f"{self.node_id} | Trust: {self.trust_score} ({self.get_trust_level()}) | "
                f"Resources: {self.cpu_cores} cores, {self.memory_gb}GB RAM | "
                f"Status: {self.status}")