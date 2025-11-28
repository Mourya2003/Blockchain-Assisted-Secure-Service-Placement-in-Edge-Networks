# config.py
"""
TrafficGuard Configuration
Includes Gas Fee Models for Priority Handling
"""

# Camera Network Configuration
CAMERA_LOCATIONS = {
    "CAM_001": {"location": "Main St & 5th Ave", "type": "Speed Camera"},
    "CAM_002": {"location": "Highway 101 Exit", "type": "Red Light Camera"},
    "CAM_003": {"location": "School Zone - Elm St", "type": "Speed Camera"},
    "CAM_004": {"location": "Downtown Intersection", "type": "Traffic Monitor"},
    "CAM_005": {"location": "Bridge Entrance", "type": "Speed Camera"},
    "CAM_006": {"location": "City Park West", "type": "Surveillance Unit"}
}

# Priority & Gas Fees (The New Economic Model)
PRIORITY_LEVELS = {
    "LOW (Routine Data)": 1,
    "MEDIUM (Violation)": 5,
    "HIGH (Accident Alert)": 20,
    "CRITICAL (Ambulance/Police)": 100
}

# Trust Thresholds
EVIDENCE_TRUST_THRESHOLD = 70.0
DEPLOYMENT_TRUST_THRESHOLD = 60.0

# Blockchain Validators
VALIDATORS = [
    "City_Traffic_Department",
    "Police_Department_Server", 
    "Court_Records_System"
]