# config.py
"""
TrafficGuard Configuration
Separates product settings from core blockchain logic
"""

# Camera Network Configuration
CAMERA_LOCATIONS = {
    "CAM_001": {"location": "Main St & 5th Ave", "type": "Speed Camera"},
    "CAM_002": {"location": "Highway 101 Exit", "type": "Red Light Camera"},
    "CAM_003": {"location": "School Zone - Elm St", "type": "Speed Camera"},
    "CAM_004": {"location": "Downtown Intersection", "type": "Traffic Monitor"},
    "CAM_005": {"location": "Bridge Entrance", "type": "Speed Camera"},
}

# Violation Types (Real Traffic Data)
VIOLATION_TYPES = [
    "Speed: 65mph in 45mph zone",
    "Red Light Violation",
    "Stop Sign Run",
    "Illegal U-Turn",
    "Speed: 35mph in School Zone (15mph)"
]

# Trust Thresholds for Evidence
EVIDENCE_TRUST_THRESHOLD = 70.0  # Camera must have 70+ trust for court evidence
DEPLOYMENT_TRUST_THRESHOLD = 60.0  # Can operate, but evidence not court-valid

# Blockchain Authorities (Realistic)
VALIDATORS = [
    "City_Traffic_Department",
    "Police_Department_Server", 
    "Court_Records_System"
]