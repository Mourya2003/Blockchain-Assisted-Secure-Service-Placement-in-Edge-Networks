# product/traffic_monitor.py
"""
Simulates Traffic Camera Behavior
This is the "PRODUCT" part - generates realistic traffic data
"""
import random
import time
from config import VIOLATION_TYPES

class TrafficCamera:
    """Simulates a real traffic camera generating violation data"""
    
    def __init__(self, camera_id, location, camera_type):
        self.camera_id = camera_id
        self.location = location
        self.camera_type = camera_type
        self.is_online = True
        
    def capture_violation(self):
        """
        Simulates camera capturing a traffic violation
        Returns: (violation_data, is_valid_capture)
        """
        if not self.is_online:
            return None, False
            
        # Simulate realistic camera behavior
        violation = random.choice(VIOLATION_TYPES)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate violation data packet
        data = {
            "camera_id": self.camera_id,
            "location": self.location,
            "violation_type": violation,
            "timestamp": timestamp,
            "vehicle_plate": f"ABC{random.randint(100,999)}",
            "image_hash": f"img_{random.randint(10000,99999)}.jpg"
        }
        
        # Simulate camera reliability (cameras can malfunction)
        is_valid = random.random() > 0.15  # 85% reliability
        
        return data, is_valid
    
    def simulate_tampering(self):
        """Simulates hacking attempt on camera"""
        self.is_online = False
        return {
            "camera_id": self.camera_id,
            "status": "COMPROMISED",
            "alert": "Unauthorized access detected"
        }