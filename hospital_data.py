"""
Hospital Layout & Directory Data (Architectural Floor Blueprint)
Clean orthogonal floor plan with realistic rooms, hallways, lifts, and stairs
strictly segregated across Ground Floor, 1st Floor, and 2nd Floor.
"""

FLOORS = {
    0: {
        "name": "Ground Floor",
        "short": "G",
        "description": "Reception, Emergency Trauma 24/7, Pharmacy, Radiology & Blood Bank",
        "rooms_count": 9
    },
    1: {
        "name": "1st Floor (OPD Wings)",
        "short": "1F",
        "description": "Cardiology, Orthology, Surgery, Pediatrics, Ultrasound & Physiotherapy",
        "rooms_count": 8
    },
    2: {
        "name": "2nd Floor (Specialist & ICU)",
        "short": "2F",
        "description": "Neurology, Nephrology, Oncology, ENT, ICU, OT & Dialysis Suite",
        "rooms_count": 8
    }
}

DOCTORS = [
    {
        "id": "DOC_ORTHO_01",
        "name": "Dr. Priya Sundaram",
        "specialty": "Orthology / Orthopedics",
        "department": "Orthology",
        "room_id": "ROOM_102",
        "room_name": "Room 102 - Orthopedic OPD",
        "floor": 1,
        "qualification": "MS (Ortho), Joint Replacement",
        "opd_timings": "09:00 AM - 01:00 PM",
        "status": "Available",
        "token_current": 14,
        "avg_consultation_mins": 4,
        "availability_tag": "🟢 Available (Token #14)",
        "keywords": ["ortho", "bone", "joint", "fracture", "orthology", "knee"]
    },
    {
        "id": "DOC_NEURO_01",
        "name": "Dr. Ramesh Natarajan",
        "specialty": "Neurology",
        "department": "Neurology",
        "room_id": "ROOM_201",
        "room_name": "Room 201 - Neurology OPD",
        "floor": 2,
        "qualification": "DM (Neurology), Brain & Spine Specialist",
        "opd_timings": "10:00 AM - 02:00 PM",
        "status": "Available",
        "token_current": 8,
        "avg_consultation_mins": 5,
        "availability_tag": "🟢 Available (Token #8)",
        "keywords": ["neuro", "nuerology", "brain", "nerve", "stroke", "neurology"]
    },
    {
        "id": "DOC_CARDIO_01",
        "name": "Dr. Kumar Velayutham",
        "specialty": "Cardiology",
        "department": "Cardiology",
        "room_id": "ROOM_101",
        "room_name": "Room 101 - Cardiology Clinic",
        "floor": 1,
        "qualification": "MD, DM (Cardiology), Cardiologist",
        "opd_timings": "09:30 AM - 01:30 PM",
        "status": "In Consultation",
        "token_current": 19,
        "avg_consultation_mins": 4,
        "availability_tag": "🟡 In Consultation (Token #19)",
        "keywords": ["cardio", "heart", "chest pain", "ecg", "cardiology"]
    },
    {
        "id": "DOC_PEDI_01",
        "name": "Dr. Anitha Balakrishnan",
        "specialty": "Pediatrics (Child Specialist)",
        "department": "Pediatrics",
        "room_id": "ROOM_104",
        "room_name": "Room 104 - Pediatric Clinic",
        "floor": 1,
        "qualification": "MD (Pediatrics), DCH",
        "opd_timings": "08:30 AM - 12:30 PM",
        "status": "Available",
        "token_current": 22,
        "avg_consultation_mins": 3,
        "availability_tag": "🟢 Available (Token #22)",
        "keywords": ["pediatric", "child", "baby", "infant", "vaccine"]
    },
    {
        "id": "DOC_SURG_01",
        "name": "Dr. Selvam Murugesan",
        "specialty": "General & Laparoscopic Surgery",
        "department": "General Surgery",
        "room_id": "ROOM_103",
        "room_name": "Room 103 - Surgical Consult",
        "floor": 1,
        "qualification": "MS (General Surgery)",
        "opd_timings": "11:00 AM - 03:00 PM",
        "status": "In Minor OT",
        "token_current": 5,
        "avg_consultation_mins": 5,
        "availability_tag": "🔴 In Minor OT (Next at 1:00 PM)",
        "keywords": ["surgery", "laparoscopy", "appendix", "hernia", "surgeon"]
    },
    {
        "id": "DOC_NEPHRO_01",
        "name": "Dr. Deepa Chandran",
        "specialty": "Nephrology (Kidney Specialist)",
        "department": "Nephrology",
        "room_id": "ROOM_202",
        "room_name": "Room 202 - Nephrology Clinic",
        "floor": 2,
        "qualification": "DM (Nephrology)",
        "opd_timings": "10:00 AM - 01:00 PM",
        "status": "Available",
        "token_current": 11,
        "avg_consultation_mins": 4,
        "availability_tag": "🟢 Available (Token #11)",
        "keywords": ["kidney", "nephro", "dialysis", "renal"]
    },
    {
        "id": "DOC_ONCO_01",
        "name": "Dr. Vignesh Narayanan",
        "specialty": "Medical Oncology (Cancer Care)",
        "department": "Oncology",
        "room_id": "ROOM_203",
        "room_name": "Room 203 - Oncology Care",
        "floor": 2,
        "qualification": "DM (Medical Oncology)",
        "opd_timings": "02:00 PM - 05:00 PM",
        "status": "On Round",
        "token_current": 7,
        "avg_consultation_mins": 6,
        "availability_tag": "🟡 On Round (Returns 2:00 PM)",
        "keywords": ["cancer", "onco", "tumor", "chemo"]
    },
    {
        "id": "DOC_ENT_01",
        "name": "Dr. Gayathri Raman",
        "specialty": "ENT & Eye Specialist",
        "department": "ENT / Ophthalmology",
        "room_id": "ROOM_204",
        "room_name": "Room 204 - ENT & Eye Clinic",
        "floor": 2,
        "qualification": "MS (ENT), DLO",
        "opd_timings": "09:00 AM - 01:00 PM",
        "status": "Available",
        "token_current": 16,
        "avg_consultation_mins": 4,
        "availability_tag": "🟢 Available (Token #16)",
        "keywords": ["ent", "ear", "nose", "throat", "eye", "vision"]
    }
]

EMERGENCY_LOCATIONS = [
    {"id": "ROOM_EMERGENCY", "name": "Emergency Ward / Casualty", "floor": 0, "icon": "🚨", "badge": "Critical 24/7"},
    {"id": "ROOM_ICU", "name": "Intensive Care Unit (ICU)", "floor": 2, "icon": "🏥", "badge": "Critical Care"},
    {"id": "ROOM_PHARMACY", "name": "Main 24/7 Pharmacy", "floor": 0, "icon": "💊", "badge": "Medicines"},
    {"id": "ROOM_BLOOD_BANK", "name": "Blood Bank", "floor": 0, "icon": "🩸", "badge": "Blood Supply"},
    {"id": "ROOM_RADIOLOGY", "name": "Radiology & CT / X-Ray", "floor": 0, "icon": "🩻", "badge": "Scans & Imaging"}
]

# Architectural Floor Blueprint Nodes
# Canvas coordinate space: 880 width x 560 height
# Corridors are orthogonal:
# North Corridor: Y = 160
# Central Main Corridor: Y = 280
# South Corridor: Y = 420
# Vertical Hallways: West X = 180, Center X = 440, East X = 700
NODES = {
    # ==================== FLOOR 0 (GROUND FLOOR) ====================
    # Entrance & Central Arrival
    "ENTRANCE_MAIN": {
        "id": "ENTRANCE_MAIN",
        "name": "Main Hospital Entrance",
        "room_code": "ENTRY",
        "type": "entrance",
        "floor": 0,
        "x": 440, "y": 500,
        "w": 120, "h": 40,
        "door_x": 440, "door_y": 480,
        "qr_code": "QR_GROUND_ENTRANCE",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🟢 24/7 Main Arrival Portico",
        "description": "Ambulance drop-off and hospital main entry gate."
    },
    "RECEPTION": {
        "id": "RECEPTION",
        "name": "Reception & Patient Token Desk",
        "room_code": "G-01",
        "type": "reception",
        "floor": 0,
        "x": 440, "y": 350,
        "w": 140, "h": 50,
        "door_x": 440, "door_y": 325,
        "qr_code": "QR_GROUND_RECEPTION",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🟢 4 Counters Active (Queue: 2 mins)",
        "description": "Outpatient registration, token issuance, and information desk."
    },

    # North Wing Rooms (Ground)
    "ROOM_EMERGENCY": {
        "id": "ROOM_EMERGENCY",
        "name": "Emergency Ward / Casualty",
        "room_code": "G-EMERGENCY",
        "type": "room",
        "floor": 0,
        "x": 130, "y": 90,
        "w": 140, "h": 80,
        "door_x": 130, "door_y": 130,
        "qr_code": "QR_GROUND_EMERGENCY",
        "status": "Emergency",
        "availability_status": "emergency",
        "availability_text": "🔴 24/7 Critical Trauma Active",
        "description": "Immediate trauma resuscitation, emergency doctors on standby."
    },
    "ROOM_TRIAGE": {
        "id": "ROOM_TRIAGE",
        "name": "Triage & Vitals Assessment",
        "room_code": "G-02",
        "type": "room",
        "floor": 0,
        "x": 280, "y": 90,
        "w": 120, "h": 80,
        "door_x": 280, "door_y": 130,
        "qr_code": "QR_GROUND_TRIAGE",
        "status": "Available",
        "availability_status": "open",
        "availability_text": "🟢 Duty Nurse Available (No Wait)",
        "description": "Blood pressure, oxygen vitals, and emergency triage prioritization."
    },
    "ROOM_RADIOLOGY": {
        "id": "ROOM_RADIOLOGY",
        "name": "Radiology, CT & X-Ray",
        "room_code": "G-03",
        "type": "room",
        "floor": 0,
        "x": 600, "y": 90,
        "w": 130, "h": 80,
        "door_x": 600, "door_y": 130,
        "qr_code": "QR_GROUND_RADIOLOGY",
        "status": "Available",
        "availability_status": "diagnostics",
        "availability_text": "🔵 Digital X-Ray & CT Scanner Active",
        "description": "Digital scans, chest X-rays, multi-slice computed tomography."
    },
    "ROOM_BLOOD_BANK": {
        "id": "ROOM_BLOOD_BANK",
        "name": "Blood Bank & Pathology",
        "room_code": "G-04",
        "type": "room",
        "floor": 0,
        "x": 750, "y": 90,
        "w": 130, "h": 80,
        "door_x": 750, "door_y": 130,
        "qr_code": "QR_GROUND_BLOOD_BANK",
        "status": "Available",
        "availability_status": "open",
        "availability_text": "🟢 All Blood Units Ready (A+, B+, O+)",
        "description": "Blood cross-matching, donor suites, diagnostic blood collection."
    },

    # Mid & South Rooms (Ground)
    "ROOM_PHARMACY": {
        "id": "ROOM_PHARMACY",
        "name": "Main 24/7 Pharmacy",
        "room_code": "G-PHARMA",
        "type": "room",
        "floor": 0,
        "x": 750, "y": 280,
        "w": 130, "h": 80,
        "door_x": 685, "door_y": 280,
        "qr_code": "QR_GROUND_PHARMACY",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🟢 24/7 Medicines Counter Stocked",
        "description": "Outpatient medicine dispensary and medical surgical supplies."
    },
    # Fire Exits & Safe Assembly Point (Ground Floor)
    "FIRE_EXIT_WEST": {
        "id": "FIRE_EXIT_WEST",
        "name": "West Fire Exit & Assembly Ground",
        "room_code": "FIRE-EXIT-W",
        "type": "fire_exit",
        "floor": 0,
        "x": 50, "y": 280,
        "w": 50, "h": 50,
        "door_x": 75, "door_y": 280,
        "status": "Emergency Exit",
        "availability_status": "emergency",
        "availability_text": "🚪🏃 Emergency Fire Exit Door (Pushes Open)",
        "description": "Direct outdoor escape route to West Garden Safe Assembly Area."
    },
    "FIRE_EXIT_EAST": {
        "id": "FIRE_EXIT_EAST",
        "name": "East Fire Exit & Parking Assembly",
        "room_code": "FIRE-EXIT-E",
        "type": "fire_exit",
        "floor": 0,
        "x": 830, "y": 280,
        "w": 50, "h": 50,
        "door_x": 805, "door_y": 280,
        "status": "Emergency Exit",
        "availability_status": "emergency",
        "availability_text": "🚪🏃 Emergency Fire Exit Door (Pushes Open)",
        "description": "Direct outdoor escape route to East Parking Safe Assembly Area."
    },
    "RESTROOM_G": {
        "id": "RESTROOM_G",
        "name": "Restrooms (Ground)",
        "room_code": "G-REST",
        "type": "amenity",
        "floor": 0,
        "x": 130, "y": 450,
        "w": 120, "h": 70,
        "door_x": 180, "door_y": 420,
        "qr_code": "QR_GROUND_RESTROOM",
        "status": "Clean",
        "availability_status": "open",
        "availability_text": "🟢 Wheelchair Accessible Washroom",
        "description": "Universal sanitized restrooms with support bars."
    },
    "ROOM_CAFETERIA": {
        "id": "ROOM_CAFETERIA",
        "name": "Cafeteria & Snacks",
        "room_code": "G-CAFE",
        "type": "amenity",
        "floor": 0,
        "x": 750, "y": 450,
        "w": 140, "h": 70,
        "door_x": 700, "door_y": 420,
        "qr_code": "QR_GROUND_CAFETERIA",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🟢 Open (Fresh Meals & Drinks)",
        "description": "Healthy refreshments, tea, coffee, and attendant dining."
    },

    # Central Core: Elevators & Stairs (Consistent across all floors)
    "LIFT_A_F0": {
        "id": "LIFT_A_F0",
        "name": "Elevator / Lift A (Ground)",
        "room_code": "LIFT-A",
        "type": "lift",
        "floor": 0,
        "x": 390, "y": 210,
        "w": 60, "h": 50,
        "door_x": 390, "door_y": 235,
        "qr_code": "QR_LIFT_A_F0",
        "status": "Operational",
        "availability_status": "open",
        "availability_text": "🛗 High-Speed Bed Lift (Wheelchair Ready)",
        "description": "Elevator connecting Ground, 1st, and 2nd Floors."
    },
    "LIFT_B_F0": {
        "id": "LIFT_B_F0",
        "name": "Elevator / Lift B (Ground)",
        "room_code": "LIFT-B",
        "type": "lift",
        "floor": 0,
        "x": 490, "y": 210,
        "w": 60, "h": 50,
        "door_x": 490, "door_y": 235,
        "qr_code": "QR_LIFT_B_F0",
        "status": "Operational",
        "availability_status": "open",
        "availability_text": "🛗 Passenger Lift (Connects 1F, 2F)",
        "description": "Passenger elevator."
    },
    "STAIRS_1_F0": {
        "id": "STAIRS_1_F0",
        "name": "Staircase 1 (West - Ground)",
        "room_code": "STAIRS-1",
        "type": "stairs",
        "floor": 0,
        "x": 310, "y": 210,
        "w": 60, "h": 50,
        "door_x": 310, "door_y": 235,
        "qr_code": "QR_STAIRS_1_F0",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🪜 Staircase to 1st & 2nd Floor",
        "description": "West wing staircase."
    },
    "STAIRS_2_F0": {
        "id": "STAIRS_2_F0",
        "name": "Staircase 2 (East - Ground)",
        "room_code": "STAIRS-2",
        "type": "stairs",
        "floor": 0,
        "x": 570, "y": 210,
        "w": 60, "h": 50,
        "door_x": 570, "door_y": 235,
        "qr_code": "QR_STAIRS_2_F0",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🪜 Staircase to 1st & 2nd Floor",
        "description": "East wing staircase."
    },

    # Ground Corridors Waypoints
    "HW_G_N_WEST": {"id": "HW_G_N_WEST", "name": "North-West Hallway", "type": "waypoint", "floor": 0, "x": 180, "y": 160},
    "HW_G_N_MID": {"id": "HW_G_N_MID", "name": "North-Central Hallway", "type": "waypoint", "floor": 0, "x": 440, "y": 160},
    "HW_G_N_EAST": {"id": "HW_G_N_EAST", "name": "North-East Hallway", "type": "waypoint", "floor": 0, "x": 700, "y": 160},
    "HW_G_MAIN_WEST": {"id": "HW_G_MAIN_WEST", "name": "Main West Hallway", "type": "waypoint", "floor": 0, "x": 180, "y": 280},
    "HW_G_MAIN_CENTER": {"id": "HW_G_MAIN_CENTER", "name": "Central Main Hallway", "type": "waypoint", "floor": 0, "x": 440, "y": 280},
    "HW_G_MAIN_EAST": {"id": "HW_G_MAIN_EAST", "name": "Main East Hallway", "type": "waypoint", "floor": 0, "x": 700, "y": 280},
    "HW_G_S_WEST": {"id": "HW_G_S_WEST", "name": "South West Hallway", "type": "waypoint", "floor": 0, "x": 180, "y": 420},
    "HW_G_S_CENTER": {"id": "HW_G_S_CENTER", "name": "South Central Hallway", "type": "waypoint", "floor": 0, "x": 440, "y": 420},
    "HW_G_S_EAST": {"id": "HW_G_S_EAST", "name": "South East Hallway", "type": "waypoint", "floor": 0, "x": 700, "y": 420},


    # ==================== FLOOR 1 (FIRST FLOOR - OPD WINGS) ====================
    # Specialist Consultation Clinics (North Wing)
    "ROOM_101": {
        "id": "ROOM_101",
        "name": "Room 101 - Cardiology Clinic",
        "room_code": "101",
        "type": "room",
        "floor": 1,
        "x": 130, "y": 90,
        "w": 140, "h": 80,
        "door_x": 130, "door_y": 130,
        "qr_code": "QR_ROOM_101",
        "doctor_id": "DOC_CARDIO_01",
        "status": "In Consultation",
        "availability_status": "consultation",
        "availability_text": "🟡 Dr. Kumar Velayutham (In Consultation, Token #19)",
        "description": "Cardiology clinic, resting ECG, rhythm analysis & consult."
    },
    "ROOM_102": {
        "id": "ROOM_102",
        "name": "Room 102 - Orthology / Orthopedic OPD",
        "room_code": "102",
        "type": "room",
        "floor": 1,
        "x": 280, "y": 90,
        "w": 130, "h": 80,
        "door_x": 280, "door_y": 130,
        "qr_code": "QR_ROOM_102",
        "doctor_id": "DOC_ORTHO_01",
        "status": "Available",
        "availability_status": "available",
        "availability_text": "🟢 Dr. Priya Sundaram (Available, Token #14)",
        "description": "Bone & joint clinic, fracture care, orthopedic consult."
    },
    "ROOM_103": {
        "id": "ROOM_103",
        "name": "Room 103 - General Surgery Consult",
        "room_code": "103",
        "type": "room",
        "floor": 1,
        "x": 600, "y": 90,
        "w": 130, "h": 80,
        "door_x": 600, "door_y": 130,
        "qr_code": "QR_ROOM_103",
        "doctor_id": "DOC_SURG_01",
        "status": "In Minor OT",
        "availability_status": "busy",
        "availability_text": "🔴 Dr. Selvam (In Minor OT, Next at 1:00 PM)",
        "description": "Pre-operative surgical evaluations and consults."
    },
    "ROOM_104": {
        "id": "ROOM_104",
        "name": "Room 104 - Pediatric & Child Health",
        "room_code": "104",
        "type": "room",
        "floor": 1,
        "x": 750, "y": 90,
        "w": 130, "h": 80,
        "door_x": 750, "door_y": 130,
        "qr_code": "QR_ROOM_104",
        "doctor_id": "DOC_PEDI_01",
        "status": "Available",
        "availability_status": "available",
        "availability_text": "🟢 Dr. Anitha Balakrishnan (Available, Token #22)",
        "description": "Child outpatient care, baby vaccinations & health checkup."
    },

    # Mid & South Facilities (Floor 1)
    "ROOM_ULTRASOUND": {
        "id": "ROOM_ULTRASOUND",
        "name": "Ultrasound & 2D Echo Lab",
        "room_code": "105-USG",
        "type": "room",
        "floor": 1,
        "x": 130, "y": 280,
        "w": 130, "h": 80,
        "door_x": 195, "door_y": 280,
        "qr_code": "QR_FLOOR1_USG",
        "status": "Available",
        "availability_status": "diagnostics",
        "availability_text": "🔵 Sonologist on Duty (Wait time ~15 mins)",
        "description": "Color Doppler, abdominal sonography & cardiac echo."
    },
    "ROOM_PHYSIO": {
        "id": "ROOM_PHYSIO",
        "name": "Physiotherapy & Rehab Center",
        "room_code": "106-REHAB",
        "type": "room",
        "floor": 1,
        "x": 750, "y": 280,
        "w": 130, "h": 80,
        "door_x": 685, "door_y": 280,
        "qr_code": "QR_FLOOR1_PHYSIO",
        "status": "Available",
        "availability_status": "available",
        "availability_text": "🟢 Open (2 Therapists Available)",
        "description": "Physical rehabilitation, exercise therapy, heat treatments."
    },
    "WAITING_LOUNGE_F1": {
        "id": "WAITING_LOUNGE_F1",
        "name": "OPD Waiting Lounge",
        "room_code": "1F-LOUNGE",
        "type": "amenity",
        "floor": 1,
        "x": 440, "y": 380,
        "w": 180, "h": 60,
        "door_x": 440, "door_y": 350,
        "qr_code": "QR_FLOOR1_WAITING",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🟢 35 Free Seats (Digital Token Screens)",
        "description": "Comfortable seating lounge with live token announcement."
    },
    "RESTROOM_F1": {
        "id": "RESTROOM_F1",
        "name": "Restrooms (1st Floor)",
        "room_code": "1F-REST",
        "type": "amenity",
        "floor": 1,
        "x": 130, "y": 450,
        "w": 120, "h": 70,
        "door_x": 180, "door_y": 420,
        "qr_code": "QR_FLOOR1_RESTROOM",
        "status": "Clean",
        "availability_status": "open",
        "availability_text": "🟢 Clean & Sanitized",
        "description": "Restrooms for patients & attendants."
    },

    # Central Core (Floor 1 - Same vertical coordinates as Ground)
    "LIFT_A_F1": {
        "id": "LIFT_A_F1",
        "name": "Elevator / Lift A (Floor 1)",
        "room_code": "LIFT-A",
        "type": "lift",
        "floor": 1,
        "x": 390, "y": 210,
        "w": 60, "h": 50,
        "door_x": 390, "door_y": 235,
        "qr_code": "QR_LIFT_A_F1",
        "status": "Operational",
        "availability_status": "open",
        "availability_text": "🛗 Operational (Connects G, 1F, 2F)",
        "description": "Elevator foyer connecting all floors."
    },
    "LIFT_B_F1": {
        "id": "LIFT_B_F1",
        "name": "Elevator / Lift B (Floor 1)",
        "room_code": "LIFT-B",
        "type": "lift",
        "floor": 1,
        "x": 490, "y": 210,
        "w": 60, "h": 50,
        "door_x": 490, "door_y": 235,
        "qr_code": "QR_LIFT_B_F1",
        "status": "Operational",
        "availability_status": "open",
        "availability_text": "🛗 Passenger Lift",
        "description": "Passenger elevator."
    },
    "STAIRS_1_F1": {
        "id": "STAIRS_1_F1",
        "name": "Staircase 1 (West - 1F)",
        "room_code": "STAIRS-1",
        "type": "stairs",
        "floor": 1,
        "x": 310, "y": 210,
        "w": 60, "h": 50,
        "door_x": 310, "door_y": 235,
        "qr_code": "QR_STAIRS_1_F1",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🪜 Staircase Landing (Down to G, Up to 2F)",
        "description": "West staircase."
    },
    "STAIRS_2_F1": {
        "id": "STAIRS_2_F1",
        "name": "Staircase 2 (East - 1F)",
        "room_code": "STAIRS-2",
        "type": "stairs",
        "floor": 1,
        "x": 570, "y": 210,
        "w": 60, "h": 50,
        "door_x": 570, "door_y": 235,
        "qr_code": "QR_STAIRS_2_F1",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🪜 Staircase Landing",
        "description": "East staircase."
    },

    # Floor 1 Corridors Waypoints
    "HW_1_N_WEST": {"id": "HW_1_N_WEST", "name": "1F North-West Hallway", "type": "waypoint", "floor": 1, "x": 180, "y": 160},
    "HW_1_N_MID": {"id": "HW_1_N_MID", "name": "1F North-Central Hallway", "type": "waypoint", "floor": 1, "x": 440, "y": 160},
    "HW_1_N_EAST": {"id": "HW_1_N_EAST", "name": "1F North-East Hallway", "type": "waypoint", "floor": 1, "x": 700, "y": 160},
    "HW_1_MAIN_WEST": {"id": "HW_1_MAIN_WEST", "name": "1F Main West Hallway", "type": "waypoint", "floor": 1, "x": 180, "y": 280},
    "HW_1_MAIN_CENTER": {"id": "HW_1_MAIN_CENTER", "name": "1F Central Main Hallway", "type": "waypoint", "floor": 1, "x": 440, "y": 280},
    "HW_1_MAIN_EAST": {"id": "HW_1_MAIN_EAST", "name": "1F Main East Hallway", "type": "waypoint", "floor": 1, "x": 700, "y": 280},
    "HW_1_S_WEST": {"id": "HW_1_S_WEST", "name": "1F South West Hallway", "type": "waypoint", "floor": 1, "x": 180, "y": 420},
    "HW_1_S_CENTER": {"id": "HW_1_S_CENTER", "name": "1F South Central Hallway", "type": "waypoint", "floor": 1, "x": 440, "y": 420},
    "HW_1_S_EAST": {"id": "HW_1_S_EAST", "name": "1F South East Hallway", "type": "waypoint", "floor": 1, "x": 700, "y": 420},


    # ==================== FLOOR 2 (SECOND FLOOR - SPECIALTY & ICU) ====================
    # Critical Care & Super Specialty (North Wing)
    "ROOM_ICU": {
        "id": "ROOM_ICU",
        "name": "Intensive Care Unit (ICU / CCU)",
        "room_code": "2F-ICU",
        "type": "room",
        "floor": 2,
        "x": 130, "y": 90,
        "w": 140, "h": 80,
        "door_x": 130, "door_y": 130,
        "qr_code": "QR_FLOOR2_ICU",
        "status": "Critical",
        "availability_status": "emergency",
        "availability_text": "🔴 Restricted Life-Support Zone (3 Beds Ready)",
        "description": "Advanced multi-para monitors, ventilators & 24/7 intensivist."
    },
    "ROOM_OT": {
        "id": "ROOM_OT",
        "name": "Operation Theatre Complex (OT 1 & 2)",
        "room_code": "2F-OT",
        "type": "room",
        "floor": 2,
        "x": 280, "y": 90,
        "w": 130, "h": 80,
        "door_x": 280, "door_y": 130,
        "qr_code": "QR_FLOOR2_OT",
        "status": "Sterile",
        "availability_status": "busy",
        "availability_text": "🔴 Surgery in Progress (OT-1 Active)",
        "description": "Laminar airflow sterile modular surgical suites."
    },
    "ROOM_201": {
        "id": "ROOM_201",
        "name": "Room 201 - Neurology OPD",
        "room_code": "201",
        "type": "room",
        "floor": 2,
        "x": 600, "y": 90,
        "w": 130, "h": 80,
        "door_x": 600, "door_y": 130,
        "qr_code": "QR_ROOM_201",
        "doctor_id": "DOC_NEURO_01",
        "status": "Available",
        "availability_status": "available",
        "availability_text": "🟢 Dr. Ramesh Natarajan (Available, Token #8)",
        "description": "Brain, nerve & spine consultation clinic."
    },
    "ROOM_202": {
        "id": "ROOM_202",
        "name": "Room 202 - Nephrology Clinic",
        "room_code": "202",
        "type": "room",
        "floor": 2,
        "x": 750, "y": 90,
        "w": 130, "h": 80,
        "door_x": 750, "door_y": 130,
        "qr_code": "QR_ROOM_202",
        "doctor_id": "DOC_NEPHRO_01",
        "status": "Available",
        "availability_status": "available",
        "availability_text": "🟢 Dr. Deepa Chandran (Available, Token #11)",
        "description": "Kidney care, hypertension & renal physician consult."
    },

    # Mid & South Facilities (Floor 2)
    "ROOM_203": {
        "id": "ROOM_203",
        "name": "Room 203 - Oncology Care",
        "room_code": "203",
        "type": "room",
        "floor": 2,
        "x": 130, "y": 280,
        "w": 130, "h": 80,
        "door_x": 195, "door_y": 280,
        "qr_code": "QR_ROOM_203",
        "doctor_id": "DOC_ONCO_01",
        "status": "On Round",
        "availability_status": "busy",
        "availability_text": "🟡 Dr. Vignesh Narayanan (On Round, Returns 2:00 PM)",
        "description": "Cancer care, chemotherapy planning & consultation."
    },
    "ROOM_204": {
        "id": "ROOM_204",
        "name": "Room 204 - ENT & Eye Clinic",
        "room_code": "204",
        "type": "room",
        "floor": 2,
        "x": 750, "y": 280,
        "w": 130, "h": 80,
        "door_x": 685, "door_y": 280,
        "qr_code": "QR_ROOM_204",
        "doctor_id": "DOC_ENT_01",
        "status": "Available",
        "availability_status": "available",
        "availability_text": "🟢 Dr. Gayathri Raman (Available, Token #16)",
        "description": "Ear, Nose, Throat endoscopy & vision checkups."
    },
    "ROOM_DIALYSIS": {
        "id": "ROOM_DIALYSIS",
        "name": "Dialysis Suite",
        "room_code": "2F-DIALYSIS",
        "type": "room",
        "floor": 2,
        "x": 130, "y": 450,
        "w": 130, "h": 70,
        "door_x": 180, "door_y": 420,
        "qr_code": "QR_FLOOR2_DIALYSIS",
        "status": "Available",
        "availability_status": "diagnostics",
        "availability_text": "🔵 6 Stations Active (2 Beds Vacant)",
        "description": "Hemodialysis stations with purified dialysis water."
    },
    "RESTROOM_F2": {
        "id": "RESTROOM_F2",
        "name": "Restrooms (2nd Floor)",
        "room_code": "2F-REST",
        "type": "amenity",
        "floor": 2,
        "x": 750, "y": 450,
        "w": 120, "h": 70,
        "door_x": 700, "door_y": 420,
        "qr_code": "QR_FLOOR2_RESTROOM",
        "status": "Clean",
        "availability_status": "open",
        "availability_text": "🟢 Clean & Sanitized",
        "description": "Patient & staff restrooms."
    },

    # Central Core (Floor 2 - Exact vertical match)
    "LIFT_A_F2": {
        "id": "LIFT_A_F2",
        "name": "Elevator / Lift A (Floor 2)",
        "room_code": "LIFT-A",
        "type": "lift",
        "floor": 2,
        "x": 390, "y": 210,
        "w": 60, "h": 50,
        "door_x": 390, "door_y": 235,
        "qr_code": "QR_LIFT_A_F2",
        "status": "Operational",
        "availability_status": "open",
        "availability_text": "🛗 Operational (Connects down to 1F, G)",
        "description": "Elevator foyer."
    },
    "LIFT_B_F2": {
        "id": "LIFT_B_F2",
        "name": "Elevator / Lift B (Floor 2)",
        "room_code": "LIFT-B",
        "type": "lift",
        "floor": 2,
        "x": 490, "y": 210,
        "w": 60, "h": 50,
        "door_x": 490, "door_y": 235,
        "qr_code": "QR_LIFT_B_F2",
        "status": "Operational",
        "availability_status": "open",
        "availability_text": "🛗 Passenger Lift",
        "description": "Passenger elevator."
    },
    "STAIRS_1_F2": {
        "id": "STAIRS_1_F2",
        "name": "Staircase 1 (West - 2F)",
        "room_code": "STAIRS-1",
        "type": "stairs",
        "floor": 2,
        "x": 310, "y": 210,
        "w": 60, "h": 50,
        "door_x": 310, "door_y": 235,
        "qr_code": "QR_STAIRS_1_F2",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🪜 Staircase Landing (Down to 1F & G)",
        "description": "West staircase."
    },
    "STAIRS_2_F2": {
        "id": "STAIRS_2_F2",
        "name": "Staircase 2 (East - 2F)",
        "room_code": "STAIRS-2",
        "type": "stairs",
        "floor": 2,
        "x": 570, "y": 210,
        "w": 60, "h": 50,
        "door_x": 570, "door_y": 235,
        "qr_code": "QR_STAIRS_2_F2",
        "status": "Open",
        "availability_status": "open",
        "availability_text": "🪜 Staircase Landing",
        "description": "East staircase."
    },

    # Floor 2 Corridors Waypoints
    "HW_2_N_WEST": {"id": "HW_2_N_WEST", "name": "2F North-West Hallway", "type": "waypoint", "floor": 2, "x": 180, "y": 160},
    "HW_2_N_MID": {"id": "HW_2_N_MID", "name": "2F North-Central Hallway", "type": "waypoint", "floor": 2, "x": 440, "y": 160},
    "HW_2_N_EAST": {"id": "HW_2_N_EAST", "name": "2F North-East Hallway", "type": "waypoint", "floor": 2, "x": 700, "y": 160},
    "HW_2_MAIN_WEST": {"id": "HW_2_MAIN_WEST", "name": "2F Main West Hallway", "type": "waypoint", "floor": 2, "x": 180, "y": 280},
    "HW_2_MAIN_CENTER": {"id": "HW_2_MAIN_CENTER", "name": "2F Central Main Hallway", "type": "waypoint", "floor": 2, "x": 440, "y": 280},
    "HW_2_MAIN_EAST": {"id": "HW_2_MAIN_EAST", "name": "2F Main East Hallway", "type": "waypoint", "floor": 2, "x": 700, "y": 280},
    "HW_2_S_WEST": {"id": "HW_2_S_WEST", "name": "2F South West Hallway", "type": "waypoint", "floor": 2, "x": 180, "y": 420},
    "HW_2_S_CENTER": {"id": "HW_2_S_CENTER", "name": "2F South Central Hallway", "type": "waypoint", "floor": 2, "x": 440, "y": 420},
    "HW_2_S_EAST": {"id": "HW_2_S_EAST", "name": "2F South East Hallway", "type": "waypoint", "floor": 2, "x": 700, "y": 420}
}

# Orthogonal Walking Corridors & Connecting Edges
EDGES = [
    # ==================== GROUND FLOOR EDGES ====================
    # Entrance & Reception to Hallways
    {"from": "ENTRANCE_MAIN", "to": "HW_G_S_CENTER", "distance": 8, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_S_CENTER", "to": "RECEPTION", "distance": 10, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "RECEPTION", "to": "HW_G_MAIN_CENTER", "distance": 10, "type": "corridor", "floor": 0, "accessible": True},

    # Main Grid (East-West corridors)
    {"from": "HW_G_N_WEST", "to": "HW_G_N_MID", "distance": 26, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_N_MID", "to": "HW_G_N_EAST", "distance": 26, "type": "corridor", "floor": 0, "accessible": True},
    
    {"from": "HW_G_MAIN_WEST", "to": "HW_G_MAIN_CENTER", "distance": 26, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_MAIN_CENTER", "to": "HW_G_MAIN_EAST", "distance": 26, "type": "corridor", "floor": 0, "accessible": True},

    {"from": "HW_G_S_WEST", "to": "HW_G_S_CENTER", "distance": 26, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_S_CENTER", "to": "HW_G_S_EAST", "distance": 26, "type": "corridor", "floor": 0, "accessible": True},

    # Main Grid (North-South hallways)
    {"from": "HW_G_N_WEST", "to": "HW_G_MAIN_WEST", "distance": 16, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_MAIN_WEST", "to": "HW_G_S_WEST", "distance": 18, "type": "corridor", "floor": 0, "accessible": True},

    {"from": "HW_G_N_MID", "to": "HW_G_MAIN_CENTER", "distance": 16, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_MAIN_CENTER", "to": "HW_G_S_CENTER", "distance": 18, "type": "corridor", "floor": 0, "accessible": True},

    {"from": "HW_G_N_EAST", "to": "HW_G_MAIN_EAST", "distance": 16, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "HW_G_MAIN_EAST", "to": "HW_G_S_EAST", "distance": 18, "type": "corridor", "floor": 0, "accessible": True},

    # Room Door Connections (Ground)
    {"from": "ROOM_EMERGENCY", "to": "HW_G_N_WEST", "distance": 8, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "ROOM_TRIAGE", "to": "HW_G_N_WEST", "distance": 10, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "ROOM_RADIOLOGY", "to": "HW_G_N_EAST", "distance": 10, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "ROOM_BLOOD_BANK", "to": "HW_G_N_EAST", "distance": 8, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "ROOM_PHARMACY", "to": "HW_G_MAIN_EAST", "distance": 6, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "RESTROOM_G", "to": "HW_G_S_WEST", "distance": 6, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "ROOM_CAFETERIA", "to": "HW_G_S_EAST", "distance": 6, "type": "corridor", "floor": 0, "accessible": True},
    # Fire Exit Escape Connections
    {"from": "FIRE_EXIT_WEST", "to": "HW_G_MAIN_WEST", "distance": 10, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "FIRE_EXIT_EAST", "to": "HW_G_MAIN_EAST", "distance": 10, "type": "corridor", "floor": 0, "accessible": True},

    # Central Core to Hallways (Ground)
    {"from": "LIFT_A_F0", "to": "HW_G_MAIN_CENTER", "distance": 8, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "LIFT_B_F0", "to": "HW_G_MAIN_CENTER", "distance": 8, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "STAIRS_1_F0", "to": "HW_G_MAIN_CENTER", "distance": 12, "type": "corridor", "floor": 0, "accessible": True},
    {"from": "STAIRS_2_F0", "to": "HW_G_MAIN_CENTER", "distance": 12, "type": "corridor", "floor": 0, "accessible": True},


    # ==================== FLOOR 1 (FIRST FLOOR) EDGES ====================
    # Main Grid (East-West)
    {"from": "HW_1_N_WEST", "to": "HW_1_N_MID", "distance": 26, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "HW_1_N_MID", "to": "HW_1_N_EAST", "distance": 26, "type": "corridor", "floor": 1, "accessible": True},

    {"from": "HW_1_MAIN_WEST", "to": "HW_1_MAIN_CENTER", "distance": 26, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "HW_1_MAIN_CENTER", "to": "HW_1_MAIN_EAST", "distance": 26, "type": "corridor", "floor": 1, "accessible": True},

    {"from": "HW_1_S_WEST", "to": "HW_1_S_CENTER", "distance": 26, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "HW_1_S_CENTER", "to": "HW_1_S_EAST", "distance": 26, "type": "corridor", "floor": 1, "accessible": True},

    # Main Grid (North-South)
    {"from": "HW_1_N_WEST", "to": "HW_1_MAIN_WEST", "distance": 16, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "HW_1_MAIN_WEST", "to": "HW_1_S_WEST", "distance": 18, "type": "corridor", "floor": 1, "accessible": True},

    {"from": "HW_1_N_MID", "to": "HW_1_MAIN_CENTER", "distance": 16, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "HW_1_MAIN_CENTER", "to": "HW_1_S_CENTER", "distance": 18, "type": "corridor", "floor": 1, "accessible": True},

    {"from": "HW_1_N_EAST", "to": "HW_1_MAIN_EAST", "distance": 16, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "HW_1_MAIN_EAST", "to": "HW_1_S_EAST", "distance": 18, "type": "corridor", "floor": 1, "accessible": True},

    # Room Door Connections (Floor 1)
    {"from": "ROOM_101", "to": "HW_1_N_WEST", "distance": 8, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "ROOM_102", "to": "HW_1_N_WEST", "distance": 10, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "ROOM_103", "to": "HW_1_N_EAST", "distance": 10, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "ROOM_104", "to": "HW_1_N_EAST", "distance": 8, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "ROOM_ULTRASOUND", "to": "HW_1_MAIN_WEST", "distance": 6, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "ROOM_PHYSIO", "to": "HW_1_MAIN_EAST", "distance": 6, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "WAITING_LOUNGE_F1", "to": "HW_1_MAIN_CENTER", "distance": 10, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "RESTROOM_F1", "to": "HW_1_S_WEST", "distance": 6, "type": "corridor", "floor": 1, "accessible": True},

    # Central Core to Hallways (Floor 1)
    {"from": "LIFT_A_F1", "to": "HW_1_MAIN_CENTER", "distance": 8, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "LIFT_B_F1", "to": "HW_1_MAIN_CENTER", "distance": 8, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "STAIRS_1_F1", "to": "HW_1_MAIN_CENTER", "distance": 12, "type": "corridor", "floor": 1, "accessible": True},
    {"from": "STAIRS_2_F1", "to": "HW_1_MAIN_CENTER", "distance": 12, "type": "corridor", "floor": 1, "accessible": True},


    # ==================== FLOOR 2 (SECOND FLOOR) EDGES ====================
    # Main Grid (East-West)
    {"from": "HW_2_N_WEST", "to": "HW_2_N_MID", "distance": 26, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "HW_2_N_MID", "to": "HW_2_N_EAST", "distance": 26, "type": "corridor", "floor": 2, "accessible": True},

    {"from": "HW_2_MAIN_WEST", "to": "HW_2_MAIN_CENTER", "distance": 26, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "HW_2_MAIN_CENTER", "to": "HW_2_MAIN_EAST", "distance": 26, "type": "corridor", "floor": 2, "accessible": True},

    {"from": "HW_2_S_WEST", "to": "HW_2_S_CENTER", "distance": 26, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "HW_2_S_CENTER", "to": "HW_2_S_EAST", "distance": 26, "type": "corridor", "floor": 2, "accessible": True},

    # Main Grid (North-South)
    {"from": "HW_2_N_WEST", "to": "HW_2_MAIN_WEST", "distance": 16, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "HW_2_MAIN_WEST", "to": "HW_2_S_WEST", "distance": 18, "type": "corridor", "floor": 2, "accessible": True},

    {"from": "HW_2_N_MID", "to": "HW_2_MAIN_CENTER", "distance": 16, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "HW_2_MAIN_CENTER", "to": "HW_2_S_CENTER", "distance": 18, "type": "corridor", "floor": 2, "accessible": True},

    {"from": "HW_2_N_EAST", "to": "HW_2_MAIN_EAST", "distance": 16, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "HW_2_MAIN_EAST", "to": "HW_2_S_EAST", "distance": 18, "type": "corridor", "floor": 2, "accessible": True},

    # Room Door Connections (Floor 2)
    {"from": "ROOM_ICU", "to": "HW_2_N_WEST", "distance": 8, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "ROOM_OT", "to": "HW_2_N_WEST", "distance": 10, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "ROOM_201", "to": "HW_2_N_EAST", "distance": 10, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "ROOM_202", "to": "HW_2_N_EAST", "distance": 8, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "ROOM_203", "to": "HW_2_MAIN_WEST", "distance": 6, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "ROOM_204", "to": "HW_2_MAIN_EAST", "distance": 6, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "ROOM_DIALYSIS", "to": "HW_2_S_WEST", "distance": 6, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "RESTROOM_F2", "to": "HW_2_S_EAST", "distance": 6, "type": "corridor", "floor": 2, "accessible": True},

    # Central Core to Hallways (Floor 2)
    {"from": "LIFT_A_F2", "to": "HW_2_MAIN_CENTER", "distance": 8, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "LIFT_B_F2", "to": "HW_2_MAIN_CENTER", "distance": 8, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "STAIRS_1_F2", "to": "HW_2_MAIN_CENTER", "distance": 12, "type": "corridor", "floor": 2, "accessible": True},
    {"from": "STAIRS_2_F2", "to": "HW_2_MAIN_CENTER", "distance": 12, "type": "corridor", "floor": 2, "accessible": True},


    # ==================== MULTI-FLOOR VERTICAL TRANSITIONS ====================
    {"from": "LIFT_A_F0", "to": "LIFT_A_F1", "distance": 10, "type": "lift", "accessible": True},
    {"from": "LIFT_A_F1", "to": "LIFT_A_F2", "distance": 10, "type": "lift", "accessible": True},

    {"from": "LIFT_B_F0", "to": "LIFT_B_F1", "distance": 10, "type": "lift", "accessible": True},
    {"from": "LIFT_B_F1", "to": "LIFT_B_F2", "distance": 10, "type": "lift", "accessible": True},

    {"from": "STAIRS_1_F0", "to": "STAIRS_1_F1", "distance": 15, "type": "stairs", "accessible": False},
    {"from": "STAIRS_1_F1", "to": "STAIRS_1_F2", "distance": 15, "type": "stairs", "accessible": False},

    {"from": "STAIRS_2_F0", "to": "STAIRS_2_F1", "distance": 15, "type": "stairs", "accessible": False},
    {"from": "STAIRS_2_F1", "to": "STAIRS_2_F2", "distance": 15, "type": "stairs", "accessible": False}
]

# ==============================================================================
# BILINGUAL SYMPTOM DICTIONARY & SMART DOCTOR MAPPING
# ==============================================================================
SYMPTOMS_CATALOG = [
    {
        "id": "SYM_CHEST_PAIN",
        "title_en": "Chest Pain & Heart Issues",
        "title_ta": "நெஞ்சு வலி / இதய பிரச்சனை",
        "keywords_en": ["chest pain", "heart", "heart attack", "angina", "palpitation", "high bp", "blood pressure", "ecg", "cardiac"],
        "keywords_ta": ["நெஞ்சு வலி", "இதயம்", "மாரடைப்பு", "மூச்சுத்திணறல்", "இரத்த அழுத்தம்", "ஈசிஜி"],
        "doctor_id": "DOC_CARDIO_01",
        "room_id": "ROOM_101",
        "department": "Cardiology",
        "floor": 1,
        "urgency": "emergency",
        "badge": "❤️ Cardiology",
        "advice_en": "Urgent: Consult Dr. Kumar Velayutham (Cardiology, Room 101) or visit Casualty immediately if severe.",
        "advice_ta": "அவசரம்: டாக்டர் குமார் (அறை 101)-ஐ அணுகவும். வலி தீவிரமாக இருப்பின் எமர்ஜென்சி வார்டுக்கு செல்லவும்."
    },
    {
        "id": "SYM_HEADACHE_BRAIN",
        "title_en": "Headache, Dizziness & Brain / Nerve",
        "title_ta": "தலைவலி, மயக்கம் & மூளை / நரம்பு",
        "keywords_en": ["headache", "migraine", "brain", "stroke", "paralysis", "dizziness", "seizure", "fits", "nerve", "spine", "numbness"],
        "keywords_ta": ["தலைவலி", "மைக்ரேன்", "மூளை", "பக்கவாதம்", "மயக்கம்", "வலிப்பு", "நரம்பு", "முதுகு தண்டு"],
        "doctor_id": "DOC_NEURO_01",
        "room_id": "ROOM_201",
        "department": "Neurology",
        "floor": 2,
        "urgency": "priority",
        "badge": "🧠 Neurology",
        "advice_en": "Consult Dr. Ramesh Natarajan (Neurology OPD, Room 201 - 2nd Floor).",
        "advice_ta": "டாக்டர் ரமேஷ் நடராஜன் (நியூராலஜி, அறை 201 - 2-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_BONE_JOINT",
        "title_en": "Bone Fracture, Knee & Joint Pain",
        "title_ta": "எலும்பு முறிவு, மூட்டு & எலும்பு வலி",
        "keywords_en": ["bone", "fracture", "joint pain", "knee", "arthritis", "back pain", "sprain", "ortho", "leg fracture", "shoulder"],
        "keywords_ta": ["எலும்பு முறிவு", "மூட்டு வலி", "முதுகு வலி", "எலும்பு தேய்மானம்", "தசை பிடிப்பு", "கால் வலி", "கை முறிவு"],
        "doctor_id": "DOC_ORTHO_01",
        "room_id": "ROOM_102",
        "department": "Orthology / Orthopedics",
        "floor": 1,
        "urgency": "routine",
        "badge": "🦴 Orthology",
        "advice_en": "Consult Dr. Priya Sundaram (Orthopedics OPD, Room 102 - 1st Floor).",
        "advice_ta": "டாக்டர் பிரியா சுந்தரம் (ஆர்த்தோபீடிக்ஸ், அறை 102 - 1-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_CHILD_FEVER",
        "title_en": "Child Fever, Cold & Vaccination",
        "title_ta": "குழந்தை காய்ச்சல், சளி & தடுப்பூசி",
        "keywords_en": ["child", "baby", "pediatric", "fever", "cold", "cough", "infant", "vaccine", "vaccination", "vomiting"],
        "keywords_ta": ["குழந்தை காய்ச்சல்", "சளி", "இருமல்", "குழந்தை", "தடுப்பூசி", "வாந்தி"],
        "doctor_id": "DOC_PEDI_01",
        "room_id": "ROOM_104",
        "department": "Pediatrics",
        "floor": 1,
        "urgency": "routine",
        "badge": "👶 Pediatrics",
        "advice_en": "Consult Dr. Anitha Balakrishnan (Pediatric Clinic, Room 104 - 1st Floor).",
        "advice_ta": "டாக்டர் அனிதா பாலகிருஷ்ணன் (குழந்தைகள் நலம், அறை 104 - 1-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_KIDNEY_URINE",
        "title_en": "Kidney Stone, Urine Infection & Dialysis",
        "title_ta": "சிறுநீரக கல், சிறுநீர் எரிச்சல் & டயாலிசிஸ்",
        "keywords_en": ["kidney", "kidney stone", "urine", "burning urine", "creatinine", "dialysis", "renal", "nephro"],
        "keywords_ta": ["சிறுநீரகம்", "கிட்னி கல்", "சிறுநீர் எரிச்சல்", "டயாலிசிஸ்", "சிறுநீர் பிரச்சனை"],
        "doctor_id": "DOC_NEPHRO_01",
        "room_id": "ROOM_202",
        "department": "Nephrology",
        "floor": 2,
        "urgency": "priority",
        "badge": "🩺 Nephrology",
        "advice_en": "Consult Dr. Deepa Chandran (Nephrology, Room 202 - 2nd Floor).",
        "advice_ta": "டாக்டர் தீபா சந்திரன் (நெப்ராலஜி, அறை 202 - 2-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_STOMACH_SURGERY",
        "title_en": "Stomach Pain, Appendix & Hernia",
        "title_ta": "வயிற்று வலி, குடல்வால் & ஹெர்னியா",
        "keywords_en": ["stomach pain", "abdominal pain", "appendix", "hernia", "gallbladder", "piles", "surgery", "laparoscopy"],
        "keywords_ta": ["வயிற்று வலி", "குடல்வால்", "ஹெர்னியா", "பித்தப்பை கல்", "மூலம்", "அறுவை சிகிச்சை"],
        "doctor_id": "DOC_SURG_01",
        "room_id": "ROOM_103",
        "department": "General Surgery",
        "floor": 1,
        "urgency": "priority",
        "badge": "🔬 General Surgery",
        "advice_en": "Consult Dr. Selvam Murugesan (Surgical Consult, Room 103 - 1st Floor).",
        "advice_ta": "டாக்டர் செல்வம் முருகேசன் (சர்ஜரி கன்சல்ட், அறை 103 - 1-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_ENT_EYE",
        "title_en": "Ear, Nose, Throat & Eye Issues",
        "title_ta": "காது, மூக்கு, தொண்டை & கண் பிரச்சனைகள்",
        "keywords_en": ["ear pain", "hearing", "sinus", "throat infection", "tonsil", "eye", "vision", "cataract", "ent"],
        "keywords_ta": ["காது வலி", "கேட்கும் திறன்", "சைனஸ்", "தொண்டை வலி", "கண் பார்வை", "கண்புரை"],
        "doctor_id": "DOC_ENT_01",
        "room_id": "ROOM_204",
        "department": "ENT & Eye Clinic",
        "floor": 2,
        "urgency": "routine",
        "badge": "👂 ENT & Eye",
        "advice_en": "Consult Dr. Gayathri Raman (ENT & Eye Clinic, Room 204 - 2nd Floor).",
        "advice_ta": "டாக்டர் காயத்ரி ராமன் (இ.என்.டி & கண், அறை 204 - 2-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_CANCER_ONCO",
        "title_en": "Cancer Care & Tumor Evaluation",
        "title_ta": "புற்றுநோய் பரிசோதனை & கட்டி சிகிச்சை",
        "keywords_en": ["cancer", "tumor", "lump", "chemo", "chemotherapy", "biopsy", "oncology"],
        "keywords_ta": ["புற்றுநோய்", "கட்டி", "கீமோதெரபி", "பயாப்சி"],
        "doctor_id": "DOC_ONCO_01",
        "room_id": "ROOM_203",
        "department": "Medical Oncology",
        "floor": 2,
        "urgency": "priority",
        "badge": "🎗️ Oncology",
        "advice_en": "Consult Dr. Vignesh Narayanan (Oncology Care, Room 203 - 2nd Floor).",
        "advice_ta": "டாக்டர் விக்னேஷ் நாராயணன் (ஆன்காலஜி, அறை 203 - 2-வது தளம்)-ஐ அணுகவும்."
    },
    {
        "id": "SYM_SCANS_XRAY",
        "title_en": "X-Ray, CT Scan & Imaging Lab",
        "title_ta": "எக்ஸ்-ரே, சிடி ஸ்கேன் & இமேஜிங்",
        "keywords_en": ["x-ray", "xray", "ct scan", "scan", "imaging", "mri", "radiology"],
        "keywords_ta": ["எக்ஸ்-ரே", "சிடி ஸ்கேன்", "ஸ்கேன்", "இமேஜிங்", "ரேடியாலஜி"],
        "doctor_id": None,
        "room_id": "ROOM_RADIOLOGY",
        "department": "Radiology & Imaging",
        "floor": 0,
        "urgency": "routine",
        "badge": "🩻 Radiology",
        "advice_en": "Proceed to Ground Floor Radiology & CT Scan Lab (West Wing).",
        "advice_ta": "தரைத்தளம் ரேடியாலஜி & சிடி ஸ்கேன் லேப்-க்கு (மேற்கு பிரிவு) செல்லவும்."
    },
    {
        "id": "SYM_PHARMACY",
        "title_en": "Medicines & Prescription Dispensing",
        "title_ta": "மருந்துகள் & மாத்திரைகள்",
        "keywords_en": ["medicine", "tablet", "pharmacy", "drug", "prescription", "syrup"],
        "keywords_ta": ["மருந்து", "மாத்திரை", "மருந்தகம்", "பார்மசி"],
        "doctor_id": None,
        "room_id": "ROOM_PHARMACY",
        "department": "Main Pharmacy",
        "floor": 0,
        "urgency": "routine",
        "badge": "💊 Pharmacy",
        "advice_en": "Proceed to 24/7 Main Pharmacy (Ground Floor East Wing).",
        "advice_ta": "தரைத்தளம் கிழக்கு பிரிவில் உள்ள 24/7 மெயின் பார்மசிக்கு செல்லவும்."
    },
    {
        "id": "SYM_BLOOD_BANK",
        "title_en": "Blood Test & Blood Grouping",
        "title_ta": "இரத்த பரிசோதனை & இரத்த வங்கி",
        "keywords_en": ["blood test", "blood bank", "blood donation", "platelets", "hemoglobin", "blood group"],
        "keywords_ta": ["இரத்த பரிசோதனை", "இரத்த வங்கி", "ரத்த தானம்", "ஹீமோகுளோபின்"],
        "doctor_id": None,
        "room_id": "ROOM_BLOOD_BANK",
        "department": "Blood Bank",
        "floor": 0,
        "urgency": "routine",
        "badge": "🩸 Blood Bank",
        "advice_en": "Proceed to Ground Floor Blood Bank (East Wing).",
        "advice_ta": "தரைத்தளம் கிழக்கு பிரிவில் உள்ள ரத்த வங்கிக்கு செல்லவும்."
    },
    {
        "id": "SYM_EMERGENCY_TRAUMA",
        "title_en": "Accident, Trauma & Critical Emergency",
        "title_ta": "விபத்து & அவசர சிகிச்சை (Casualty)",
        "keywords_en": ["accident", "trauma", "emergency", "casualty", "heavy bleeding", "unconscious", "poison", "burns"],
        "keywords_ta": ["விபத்து", "அவசர சிகிச்சை", "அதிக ரத்தப்போக்கு", "சுயநினைவின்மை", "விஷம்", "தீக்காயம்"],
        "doctor_id": None,
        "room_id": "ROOM_EMERGENCY",
        "department": "Emergency Casualty",
        "floor": 0,
        "urgency": "emergency",
        "badge": "🚨 Emergency",
        "advice_en": "Critical: Rush immediately to Emergency Trauma Ward (Ground Floor West).",
        "advice_ta": "மிக அவசரம்: தரைத்தளத்தில் உள்ள எமர்ஜென்சி ட்ராமா வார்டுக்கு உடனடியாக செல்லவும்."
    }
]


def search_symptoms_and_doctors(query, limit=6):
    """
    Smart Symptom Search Engine.
    Matches queries in English and Tamil across symptoms, doctors, specialties, and rooms.
    """
    if not query:
        return []

    q = query.strip().lower()
    if len(q) < 2:
        return []

    results = []
    seen_ids = set()

    # 1. Match against Symptoms Catalog
    for sym in SYMPTOMS_CATALOG:
        score = 0
        matched_kw = None

        # Check English keywords
        for kw in sym["keywords_en"]:
            if q == kw:
                score = max(score, 60)
                matched_kw = kw
                break
            elif q in kw or kw in q:
                score = max(score, 40)
                matched_kw = kw

        # Check Tamil keywords
        for kw in sym["keywords_ta"]:
            if q == kw:
                score = max(score, 60)
                matched_kw = kw
                break
            elif q in kw or kw in q:
                score = max(score, 40)
                matched_kw = kw

        # Check titles
        if q in sym["title_en"].lower() or q in sym["title_ta"].lower():
            score = max(score, 35)

        if score > 0:
            doc_info = None
            if sym.get("doctor_id"):
                for d in DOCTORS:
                    if d["id"] == sym["doctor_id"]:
                        doc_info = d
                        break

            room_info = NODES.get(sym["room_id"], {})
            entry_id = f"sym_{sym['id']}"
            if entry_id not in seen_ids:
                seen_ids.add(entry_id)
                results.append({
                    "score": score,
                    "type": "symptom",
                    "id": sym["id"],
                    "matched_keyword": matched_kw or q,
                    "title_en": sym["title_en"],
                    "title_ta": sym["title_ta"],
                    "department": sym["department"],
                    "urgency": sym["urgency"],
                    "badge": sym["badge"],
                    "advice_en": sym["advice_en"],
                    "advice_ta": sym["advice_ta"],
                    "doctor": doc_info,
                    "target_node_id": sym["room_id"],
                    "target_node_name": room_info.get("name", sym["room_id"]),
                    "floor": sym["floor"]
                })

    # 2. Match against Doctors directly
    for doc in DOCTORS:
        score = 0
        doc_q = doc["name"].lower()
        spec_q = doc["specialty"].lower()

        if q in doc_q:
            score = 50
        elif q in spec_q:
            score = 45
        else:
            for kw in doc.get("keywords", []):
                if q in kw.lower() or kw.lower() in q:
                    score = 35
                    break

        if score > 0:
            entry_id = f"doc_{doc['id']}"
            if entry_id not in seen_ids:
                seen_ids.add(entry_id)
                results.append({
                    "score": score,
                    "type": "doctor",
                    "id": doc["id"],
                    "matched_keyword": doc["name"],
                    "title_en": f"{doc['name']} ({doc['specialty']})",
                    "title_ta": f"{doc['name']} ({doc['specialty']})",
                    "department": doc["department"],
                    "urgency": "routine",
                    "badge": "👨‍⚕️ Specialist Doctor",
                    "advice_en": f"Consult {doc['name']} at {doc['room_name']}.",
                    "advice_ta": f"{doc['name']} - அறை {doc['room_name']}-ல் சந்திக்கலாம்.",
                    "doctor": doc,
                    "target_node_id": doc["room_id"],
                    "target_node_name": doc["room_name"],
                    "floor": doc["floor"]
                })

    # 3. Sort by score descending and return top matches
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def get_doctor_queue_info(doctor_id, patient_token=None):
    """
    Calculates live queue analytics and estimated waiting time for a doctor.
    """
    doctor = None
    for d in DOCTORS:
        if d["id"] == doctor_id or d["room_id"] == doctor_id:
            doctor = d
            break

    if not doctor:
        return {"success": False, "error": f"Doctor '{doctor_id}' not found"}

    current_token = doctor["token_current"]
    avg_mins = doctor.get("avg_consultation_mins", 4)

    # If patient has not entered token, generate a default appointment token (current + 9)
    if patient_token is None or patient_token <= 0:
        patient_token = current_token + 9

    patients_ahead = max(0, patient_token - current_token)
    estimated_wait_minutes = patients_ahead * avg_mins

    if patients_ahead <= 2:
        urgency_level = "now"
        status_text_en = "Almost Your Turn! Head to OPD immediately."
        status_text_ta = "உங்கள் முறை நெருங்கிவிட்டது! உடனே செல்லவும்."
        status_badge = "🟢 Next in Line"
    elif patients_ahead <= 6:
        urgency_level = "moderate"
        status_text_en = f"{patients_ahead} patients ahead (~{estimated_wait_minutes} mins wait). Wait in OPD lounge."
        status_text_ta = f"{patients_ahead} நோயாளிகள் முன்னால் உள்ளனர் (~{estimated_wait_minutes} நிமிடம் காத்திருப்பு)."
        status_badge = "🟡 Moderate Wait"
    else:
        urgency_level = "long"
        status_text_en = f"Long Queue: {patients_ahead} patients ahead (~{estimated_wait_minutes} mins wait). Complete scans first to save time!"
        status_text_ta = f"நீண்ட வரிசை: {patients_ahead} பேர் முன்னால் உள்ளனர் (~{estimated_wait_minutes} நிமி). ஸ்கேன்/பார்மசியை முதலில் முடிக்கலாம்!"
        status_badge = "🔴 Long Wait"

    return {
        "success": True,
        "doctor_id": doctor["id"],
        "doctor_name": doctor["name"],
        "specialty": doctor["specialty"],
        "room_id": doctor["room_id"],
        "room_name": doctor["room_name"],
        "floor": doctor["floor"],
        "current_token": current_token,
        "patient_token": patient_token,
        "patients_ahead": patients_ahead,
        "avg_consultation_mins": avg_mins,
        "estimated_wait_minutes": estimated_wait_minutes,
        "urgency_level": urgency_level,
        "status_badge": status_badge,
        "status_text_en": status_text_en,
        "status_text_ta": status_text_ta,
        "can_do_scans_first": bool(patients_ahead >= 5)
    }


def optimize_multistop_order_by_queue(start_id, stops, patient_token=None):
    """
    Smart Queue Optimizer:
    If a Doctor has a long wait time and a Scan lab is in the stops,
    intelligently reorders the journey to do Scans first, saving 25-40 mins of idle waiting!
    """
    if not stops or len(stops) < 2:
        return {"can_optimize": False, "stops": stops}

    # Find if any stop is a Doctor room
    doctor_room_idx = -1
    matched_doc = None
    for idx, s in enumerate(stops):
        for d in DOCTORS:
            if d["room_id"] == s:
                doctor_room_idx = idx
                matched_doc = d
                break
        if doctor_room_idx != -1:
            break

    # Find if any stop is a Scan lab or Pharmacy
    scan_rooms = ["ROOM_RADIOLOGY", "ROOM_105", "ROOM_BLOOD_BANK", "ROOM_PHARMACY"]
    scan_room_idx = -1
    matched_scan = None
    for idx, s in enumerate(stops):
        if s in scan_rooms:
            scan_room_idx = idx
            matched_scan = s
            break

    if doctor_room_idx == -1 or scan_room_idx == -1:
        return {"can_optimize": False, "stops": stops}

    # If Doctor is already scheduled after the scan, no reordering needed
    if doctor_room_idx > scan_room_idx:
        return {"can_optimize": False, "stops": stops}

    # Evaluate Doctor Queue
    queue_info = get_doctor_queue_info(matched_doc["id"], patient_token)
    patients_ahead = queue_info["patients_ahead"]
    wait_mins = queue_info["estimated_wait_minutes"]

    # Only recommend reordering if Doctor wait time is >= 15 minutes!
    if wait_mins < 15:
        return {"can_optimize": False, "stops": stops}

    # Create optimized stop order: move scan before doctor
    optimized_stops = list(stops)
    scan_item = optimized_stops.pop(scan_room_idx)
    optimized_stops.insert(doctor_room_idx, scan_item)

    scan_names = {
        "ROOM_RADIOLOGY": "Radiology & X-Ray (Ground Floor, 5 min wait)",
        "ROOM_105": "Ultrasound & 2D Echo Lab (Floor 1, 5 min wait)",
        "ROOM_BLOOD_BANK": "Blood Bank (Ground Floor, 4 min wait)",
        "ROOM_PHARMACY": "Main Pharmacy (Ground Floor, 3 min wait)"
    }
    scan_name = scan_names.get(matched_scan, "Diagnostic Scan")

    time_saved = max(15, wait_mins - 10)

    advisory_en = (
        f"{matched_doc['name']} has {patients_ahead} patients ahead (~{wait_mins} mins wait). "
        f"We recommend visiting {scan_name} first! You can save ~{time_saved} minutes of idle waiting."
    )
    advisory_ta = (
        f"{matched_doc['name']}-விடம் {patients_ahead} பேர் முன்னால் உள்ளனர் (~{wait_mins} நிமி காத்திருப்பு). "
        f"முதலில் {scan_name}-ஐ முடித்துவிட்டால் சுமார் {time_saved} நிமிடம் மிச்சமாகும்!"
    )

    return {
        "can_optimize": True,
        "original_stops": stops,
        "optimized_stops": optimized_stops,
        "doctor_name": matched_doc["name"],
        "doctor_room": matched_doc["room_id"],
        "scan_room": matched_scan,
        "patients_ahead": patients_ahead,
        "wait_minutes": wait_mins,
        "time_saved_mins": time_saved,
        "advisory_en": advisory_en,
        "advisory_ta": advisory_ta
    }


# ==============================================================================
# LIVE CROWD DENSITY & RUSH METRICS
# ==============================================================================
CROWD_DENSITY = {
    # Floor 0 (Ground Floor)
    "RECEPTION": {"level": "high", "percentage": 88, "people_count": 28, "status_en": "High Rush (Token Queue)", "status_ta": "அதிக நெரிசல் (டோக்கன் வரிசை)"},
    "ROOM_PHARMACY": {"level": "high", "percentage": 92, "people_count": 34, "status_en": "High Rush (Prescription Counter)", "status_ta": "அதிக நெரிசல் (மருந்து கவுண்டர்)"},
    "ROOM_EMERGENCY": {"level": "high", "percentage": 78, "people_count": 18, "status_en": "Priority Emergency Rush", "status_ta": "அவசர பிரிவு நெரிசல்"},
    "HW_G_MAIN_CENTER": {"level": "high", "percentage": 80, "people_count": 24, "status_en": "Heavy Foot Traffic", "status_ta": "அதிக மக்கள் நடமாட்டம்"},
    "ROOM_RADIOLOGY": {"level": "moderate", "percentage": 48, "people_count": 12, "status_en": "Moderate Waiting (Scans)", "status_ta": "மிதமான காத்திருப்பு"},
    "ROOM_BLOOD_BANK": {"level": "low", "percentage": 22, "people_count": 5, "status_en": "Low Traffic (Smooth)", "status_ta": "குறைந்த நெரிசல்"},
    "ROOM_REST_G": {"level": "low", "percentage": 15, "people_count": 2, "status_en": "Low Traffic (Restrooms)", "status_ta": "குறைந்த கூட்டம்"},
    "HW_G_MAIN_WEST": {"level": "moderate", "percentage": 42, "people_count": 9, "status_en": "Moderate Walkway", "status_ta": "மிதமான நடமாட்டம்"},
    "HW_G_MAIN_EAST": {"level": "moderate", "percentage": 52, "people_count": 14, "status_en": "Moderate Walkway", "status_ta": "மிதமான நடமாட்டம்"},
    "ENTRANCE_MAIN": {"level": "moderate", "percentage": 60, "people_count": 16, "status_en": "Steady Inflow", "status_ta": "தொடர் வருகை"},
    "LIFT_A_F0": {"level": "high", "percentage": 75, "people_count": 14, "status_en": "Busy Elevator", "status_ta": "அதிக லிஃப்ட் கூட்டம்"},
    "LIFT_B_F0": {"level": "moderate", "percentage": 50, "people_count": 8, "status_en": "Moderate Lift", "status_ta": "மிதமான லிஃப்ட் கூட்டம்"},
    "STAIRS_1_F0": {"level": "moderate", "percentage": 45, "people_count": 7, "status_en": "Normal Stairway", "status_ta": "மிதமான படிக்கட்டு"},
    "STAIRS_2_F0": {"level": "low", "percentage": 25, "people_count": 3, "status_en": "Free Stairway", "status_ta": "சுலப படிக்கட்டு"},

    # Floor 1 (OPD Wings)
    "ROOM_101": {"level": "moderate", "percentage": 68, "people_count": 19, "status_en": "Moderate-High (Cardiology OPD)", "status_ta": "கார்டியாலஜி காத்திருப்பு"},
    "ROOM_102": {"level": "moderate", "percentage": 62, "people_count": 15, "status_en": "Moderate (Orthology OPD)", "status_ta": "ஆர்த்தோ காத்திருப்பு"},
    "ROOM_103": {"level": "moderate", "percentage": 45, "people_count": 8, "status_en": "Moderate (Surgical Consult)", "status_ta": "சர்ஜரி காத்திருப்பு"},
    "ROOM_104": {"level": "moderate", "percentage": 58, "people_count": 14, "status_en": "Moderate (Pediatric Lounge)", "status_ta": "குழந்தைகள் பிரிவு"},
    "ROOM_105": {"level": "low", "percentage": 30, "people_count": 6, "status_en": "Low Wait (Ultrasound)", "status_ta": "குறைந்த காத்திருப்பு"},
    "ROOM_106": {"level": "low", "percentage": 20, "people_count": 4, "status_en": "Smooth (Physiotherapy)", "status_ta": "குறைந்த கூட்டம்"},
    "ROOM_REST_1": {"level": "low", "percentage": 18, "people_count": 2, "status_en": "Low Traffic (Restrooms)", "status_ta": "குறைந்த கூட்டம்"},
    "HW_1_MAIN_CENTER": {"level": "moderate", "percentage": 50, "people_count": 11, "status_en": "Moderate Hallway", "status_ta": "மிதமான நடைபாதை"},
    "STAIRS_1_F1": {"level": "moderate", "percentage": 40, "people_count": 7, "status_en": "Normal Stair Flow", "status_ta": "வழக்கமான படிகள்"},
    "STAIRS_2_F1": {"level": "low", "percentage": 22, "people_count": 3, "status_en": "Clear Stairway", "status_ta": "சுலப படிகள்"},
    "LIFT_A_F1": {"level": "moderate", "percentage": 55, "people_count": 8, "status_en": "Moderate Lift Queue", "status_ta": "லிஃப்ட் காத்திருப்பு"},
    "LIFT_B_F1": {"level": "moderate", "percentage": 45, "people_count": 6, "status_en": "Normal Lift Queue", "status_ta": "வழக்கமான லிஃப்ட்"},

    # Floor 2 (Specialty & ICU)
    "ROOM_ICU": {"level": "low", "percentage": 15, "people_count": 2, "status_en": "Restricted Access (Very Low)", "status_ta": "கட்டுப்படுத்தப்பட்ட பகுதி"},
    "ROOM_OT": {"level": "low", "percentage": 10, "people_count": 2, "status_en": "Sterile Complex (Zero Rush)", "status_ta": "ஆபரேஷன் தியேட்டர் பிரிவு"},
    "ROOM_201": {"level": "moderate", "percentage": 42, "people_count": 9, "status_en": "Normal (Neurology OPD)", "status_ta": "நியூராலஜி காத்திருப்பு"},
    "ROOM_202": {"level": "low", "percentage": 35, "people_count": 7, "status_en": "Low-Moderate (Nephrology)", "status_ta": "மிதமான நெரிசல்"},
    "ROOM_203": {"level": "low", "percentage": 28, "people_count": 5, "status_en": "Low (Oncology Lounge)", "status_ta": "குறைந்த காத்திருப்பு"},
    "ROOM_204": {"level": "moderate", "percentage": 44, "people_count": 8, "status_en": "Moderate (ENT & Eye)", "status_ta": "கண் & காது பிரிவு"},
    "ROOM_DIALYSIS": {"level": "low", "percentage": 25, "people_count": 4, "status_en": "Scheduled Care Only", "status_ta": "திட்டமிடப்பட்ட சிகிச்சை"},
    "ROOM_REST_2": {"level": "low", "percentage": 12, "people_count": 1, "status_en": "Free Restrooms", "status_ta": "சுலப பயன்பாடு"},
    "HW_2_MAIN_CENTER": {"level": "low", "percentage": 25, "people_count": 5, "status_en": "Quiet Corridor", "status_ta": "அமைதியான காரிடார்"},
    "LIFT_A_F2": {"level": "low", "percentage": 30, "people_count": 3, "status_en": "Low Lift Demand", "status_ta": "குறைந்த லிஃப்ட் காத்திருப்பு"},
    "LIFT_B_F2": {"level": "low", "percentage": 25, "people_count": 2, "status_en": "Low Lift Demand", "status_ta": "குறைந்த காத்திருப்பு"},
    "STAIRS_1_F2": {"level": "low", "percentage": 20, "people_count": 2, "status_en": "Quiet Stairway", "status_ta": "அமைதியான படிகள்"},
    "STAIRS_2_F2": {"level": "low", "percentage": 15, "people_count": 2, "status_en": "Quiet Stairway", "status_ta": "அமைதியான படிகள்"}
}


def get_crowd_density():
    """Returns real-time crowd density data for all nodes."""
    return {
        "success": True,
        "crowd_data": CROWD_DENSITY,
        "floor_summary": {
            0: {"status": "high", "label_en": "Ground Floor: Heavy Rush (Reception & Pharmacy)", "label_ta": "தரைத்தளம்: அதிக கூட்டம் (பார்மசி & வரவேற்பு)"},
            1: {"status": "moderate", "label_en": "1st Floor: Moderate OPD Traffic", "label_ta": "1-வது தளம்: மிதமான OPD கூட்டம்"},
            2: {"status": "low", "label_en": "2nd Floor: Quiet / Low Congestion", "label_ta": "2-வது தளம்: அமைதி / குறைந்த நெரிசல்"}
        }
    }


# ==============================================================================
# 1-CLICK NEAREST AMENITIES DEFINITION
# ==============================================================================
AMENITY_CATEGORIES = {
    "restroom": {
        "id": "restroom",
        "title_en": "Nearest Restroom / Washroom",
        "title_ta": "அருகிலுள்ள கழிப்பறை",
        "icon": "🚻",
        "nodes": ["RESTROOM_G", "RESTROOM_F1", "RESTROOM_F2"],
        "description_en": "Sanitized universal washrooms with support bars and wheelchair ramp access.",
        "description_ta": "சுகாதாரமான கழிப்பறை வசதி (வீல்சேர் செல்லும் வசதியுடன்)."
    },
    "water": {
        "id": "water",
        "title_en": "Drinking Water (RO Dispenser)",
        "title_ta": "குடிநீர் வசதி (RO)",
        "icon": "🚰",
        "nodes": ["ROOM_CAFETERIA", "WAITING_LOUNGE_F1", "RESTROOM_F2"],
        "description_en": "24/7 Purified RO cold and normal drinking water stations.",
        "description_ta": "சுத்திகரிக்கப்பட்ட குடிநீர் வசதி (24 மணி நேரமும்)."
    },
    "pharmacy": {
        "id": "pharmacy",
        "title_en": "24/7 Main Pharmacy",
        "title_ta": "24/7 மெயின் பார்மசி",
        "icon": "💊",
        "nodes": ["ROOM_PHARMACY"],
        "description_en": "Prescription dispensing, surgical supplies, and patient medications.",
        "description_ta": "மருந்துகள் & மாத்திரைகள் வழங்கும் பிரிவு."
    },
    "cafeteria": {
        "id": "cafeteria",
        "title_en": "Cafeteria & Canteen",
        "title_ta": "உணவகம் & சிற்றுண்டி",
        "icon": "☕",
        "nodes": ["ROOM_CAFETERIA"],
        "description_en": "Healthy refreshments, hot tea, coffee, meals, and attendant dining.",
        "description_ta": "சூடான உணவு, தேநீர், காபி மற்றும் சிற்றுண்டி."
    },
    "atm": {
        "id": "atm",
        "title_en": "ATM & Cash Billing Counter",
        "title_ta": "ATM & கட்டண கவுண்டர்",
        "icon": "🏧",
        "nodes": ["RECEPTION"],
        "description_en": "Hospital main cashier, insurance desk, and 24/7 Bank ATM kiosk.",
        "description_ta": "பணம் செலுத்தும் கவுண்டர் & 24/7 வங்கி ATM."
    },
    "lift": {
        "id": "lift",
        "title_en": "Wheelchair Elevator / Lift",
        "title_ta": "அருகிலுள்ள லிஃப்ட்",
        "icon": "🛗",
        "nodes": ["LIFT_A_F0", "LIFT_A_F1", "LIFT_A_F2", "LIFT_B_F0", "LIFT_B_F1", "LIFT_B_F2"],
        "description_en": "High-capacity bed lift and passenger elevator for easy floor transitions.",
        "description_ta": "மாடிகளுக்கு எளிதாக செல்லும் லிஃப்ட்."
    }
}


def get_amenity_categories():
    """Returns the list of available hospital amenity categories."""
    return AMENITY_CATEGORIES


