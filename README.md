# 🏥 Hospital Department Navigation System (Indoor Dijkstra Routing)

An intelligent, multi-floor indoor hospital navigation system with **Python Flask backend** and **Interactive 2D Canvas Architectural Blueprint Frontend**. Calculates the mathematically guaranteed shortest path to any hospital room or specialist doctor (Orthology, Neurology, Cardiology, etc.) using **Dijkstra's Algorithm**.

---

## 📁 Project Architecture & File Breakdown

```
d:\Navigation System\
│
├── 🐍 app.py                    # Main Flask REST API & Web Server
├── 🐍 dijkstra.py               # Dijkstra Algorithm with Travel Modes & Dynamic Rerouting
├── 🐍 graph.py                  # Hospital Graph data structure (Adjacency list, Obstacle filter)
├── 🐍 hospital_data.py          # Architectural Blueprint Floor plan dataset (64 Nodes, 82 Edges)
├── 🐍 navigation_service.py     # Bilingual Turn-by-Turn Instruction Generator (English & Tamil)
├── 🐍 test_navigation.py        # Automated test suite verifying modes & dynamic rerouting
├── 📄 requirements.txt          # Python dependencies (Flask >= 3.0.0)
│
├── 📂 templates/
│   └── 🌐 index.html            # Medical-grade interactive web interface & controls
│
└── 📂 static/
    ├── 📂 css/
    │   └── 🎨 style.css         # Modern healthcare UI styling, animations & responsive layout
    └── 📂 js/
        ├── ⚡ api.js            # API client communicating with Python backend
        ├── 🗺️ map_renderer.js   # Fixed-frame 2D Blueprint Floor Plan Renderer (No drift/jitter)
        ├── 🔊 voice.js          # On-demand Web Speech API Audio Navigation (English & Tamil)
        ├── 📷 qr_simulator.js   # Wall/Pillar QR Code indoor positioning simulator
        └── 🎮 app.js            # Frontend master coordinator connecting UI, Map & Voice
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Verification Tests
```bash
python test_navigation.py
```

### 3. Start the Flask Server
```bash
python app.py
```

### 4. Open in Browser
Visit in your web browser:
```
http://127.0.0.1:5000
```

---

## 🌟 Advanced Features Implemented

### 1. 🚶 Mobility & Travel Mode Preference (Walk / Wheelchair / Stretcher)
User can choose their mobility preference:
- 🚶 **By Walk**: Fastest path, utilizes stairs or elevators (~1.1 m/s, step count displayed).
- ♿ **Wheelchair**: Strict accessibility constraint — bypasses all stairs, routes exclusively via elevators & ramps (~0.85 m/s).
- 🛏️ **Stretcher / Patient Trolley**: Slower, steady transit avoiding narrow turns and restricted to express bed elevators (~0.65 m/s).

### 2. 🔊 Audio Voice Guidance (Strictly On-Demand)
- By default, audio voice guidance is **OFF** so it does not speak unexpectedly.
- User can toggle **`🔊 Voice Audio: [ON / OFF]`** at the top right, or click the **"Read Aloud"** button to hear turn-by-turn spoken guidance in either **English** or **தமிழ் (Tamil)**!

### 3. 🚧 Dynamic Corridor / Lift Blockage & Real-Time Rerouting
- Simulates real hospital conditions (e.g., corridor wet floor cleaning, Lift A maintenance, emergency ward sterile lockdown).
- Check the **"Hospital Corridor & Lift Maintenance Simulator"** options:
  - Check `Lift A Under Maintenance` ➡️ System instantly recalculates route via `Lift B`!
  - Check `Central Corridor Blocked` ➡️ System recalculates an alternate route around the block via side hallways!
  - Map marks blocked areas with a `🚧 BLOCKED` hazard overlay.
  - Generates real-time audio and text alerts: *"⚠️ Notice: Path rerouted to avoid blocked/maintenance areas."*

### 4. 🏢 Strict Floor Segregation & Architectural Blueprint
- **Ground Floor**: Reception, Emergency 24/7, Triage, Pharmacy, Radiology/CT, Blood Bank, Cafeteria, Restrooms, Lifts A/B, Stairs 1/2.
- **1st Floor (OPD Wings)**: Cardiology (Dr. Kumar), Orthology (Dr. Priya), Surgery (Dr. Selvam), Pediatrics (Dr. Anitha), Ultrasound, Physiotherapy, OPD Lounge.
- **2nd Floor (Specialist & ICU)**: Neurology (Dr. Ramesh), Nephrology (Dr. Deepa), Oncology (Dr. Vignesh), ENT/Eye (Dr. Gayathri), ICU, OT, Dialysis.
- **One-Tap Lift / Stairs Transition**: When a route reaches an elevator on Ground floor, a single tap transitions the blueprint directly to 1st/2nd floor with continuing walking arrows!
