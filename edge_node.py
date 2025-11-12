import time

class EdgeNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.trust_score = 50
        self.successful_tasks = 0
        self.total_tasks = 0
        self.last_activity = time.time()

    def update_trust(self, success, recency_weight=0.9):
        current_time = time.time()
        time_diff = current_time - self.last_activity
        recency_factor = max(0.5, 1 - (time_diff / 3600))  # decay if inactive

        if success:
            self.trust_score = min(self.trust_score + 5 * recency_factor, 100)
            self.successful_tasks += 1
        else:
            self.trust_score = max(self.trust_score - 10, 0)

        self.total_tasks += 1
        self.last_activity = current_time

    def apply_decay(self, decay_rate=0.1):
        if time.time() - self.last_activity > 1800:  # 30 mins
            self.trust_score = max(self.trust_score - decay_rate * 10, 0)
