"""
Flask Application - Hospital Indoor Navigation System
Provides REST APIs for Dijkstra routing, Travel Modes (Walk/Wheelchair/Stretcher),
Dynamic Obstacle Blockages & Rerouting, Doctor Directory, and Floor Blueprint.
"""
from flask import Flask, jsonify, request, render_template
from graph import HospitalGraph
from navigation_service import NavigationService
from hospital_data import (
    search_symptoms_and_doctors,
    get_doctor_queue_info,
    optimize_multistop_order_by_queue,
    get_crowd_density,
    CROWD_DENSITY,
    get_amenity_categories,
    AMENITY_CATEGORIES
)

app = Flask(__name__)

hospital_graph = HospitalGraph()
nav_service = NavigationService(hospital_graph)


@app.route("/")
def index():
    """Renders the main hospital interactive navigation dashboard."""
    return render_template("index.html")


@app.route("/api/hospital-map", methods=["GET"])
def get_hospital_map():
    """Returns the complete hospital graph schema for architectural floor plan visualization."""
    return jsonify({
        "success": True,
        "data": hospital_graph.to_dict()
    })


@app.route("/api/doctors", methods=["GET"])
def get_doctors():
    """Returns directory of specialist doctors, rooms, OPD timings, and status."""
    return jsonify({
        "success": True,
        "doctors": hospital_graph.doctors
    })


@app.route("/api/locations", methods=["GET"])
def get_locations():
    """Returns list of selectable hospital locations grouped by floor."""
    grouped_locations = {0: [], 1: [], 2: []}

    for node_id, node in hospital_graph.nodes.items():
        if node.get("type") in ["entrance", "reception", "room", "amenity", "lift", "stairs"]:
            floor = node["floor"]
            grouped_locations[floor].append({
                "id": node_id,
                "name": node["name"],
                "room_code": node.get("room_code", ""),
                "type": node["type"],
                "floor": floor,
                "qr_code": node.get("qr_code")
            })

    return jsonify({
        "success": True,
        "floors": hospital_graph.floors,
        "locations_by_floor": grouped_locations
    })


@app.route("/api/floor-directory/<int:floor>", methods=["GET"])
def get_floor_directory(floor):
    """Returns full room directory and live status for a specific floor."""
    floor_rooms = []
    for node_id, node in hospital_graph.nodes.items():
        if node.get("floor") == floor and node.get("type") in ["room", "reception", "entrance", "amenity", "lift", "stairs"]:
            doc_info = None
            if node.get("doctor_id"):
                doc_info = hospital_graph.find_doctor_by_id_or_keyword(node["doctor_id"])

            crowd = CROWD_DENSITY.get(node_id, {"level": "low", "percentage": 20, "status_en": "Normal", "status_ta": "வழக்கமானது"})

            floor_rooms.append({
                "id": node_id,
                "name": node.get("name"),
                "room_code": node.get("room_code", "RM"),
                "type": node.get("type"),
                "floor": floor,
                "status": node.get("status", "Open"),
                "availability_status": node.get("availability_status", "open"),
                "availability_text": node.get("availability_text", "Available"),
                "description": node.get("description", ""),
                "doctor": doc_info,
                "crowd_level": crowd.get("level", "low"),
                "crowd_percentage": crowd.get("percentage", 20),
                "crowd_status_en": crowd.get("status_en", ""),
                "crowd_status_ta": crowd.get("status_ta", "")
            })

    return jsonify({
        "success": True,
        "floor": floor,
        "floor_meta": hospital_graph.floors.get(floor),
        "rooms": floor_rooms
    })


@app.route("/api/navigate", methods=["POST"])
def navigate():
    """
    Main Navigation API:
    Supports travel_mode ('walk' | 'wheelchair' | 'stretcher') and
    blocked_nodes (list of currently blocked corridors/lifts for instant rerouting).
    """
    data = request.get_json(silent=True) or {}
    start_id = data.get("start")
    destination = data.get("destination")
    is_doctor = data.get("is_doctor", False)
    
    # Travel Mode preference
    travel_mode = data.get("travel_mode", "walk")
    if data.get("wheelchair_mode"):
        travel_mode = "wheelchair"

    # List of blocked nodes (e.g. ['LIFT_A_F0', 'HW_G_MAIN_CENTER'])
    blocked_nodes = data.get("blocked_nodes", [])

    if not start_id or not destination:
        return jsonify({
            "success": False,
            "error": "Both 'start' location and 'destination' are required."
        }), 400

    result = nav_service.plan_route(
        start_id=start_id,
        destination_query=destination,
        is_doctor=is_doctor,
        travel_mode=travel_mode,
        blocked_nodes=blocked_nodes
    )

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/navigate-multistop", methods=["POST"])
def navigate_multistop():
    """
    Multi-Stop Journey Planning API:
    Calculates chained Dijkstra shortest route visiting multiple departments in sequence.
    Payload:
    {
        "start": "ENTRANCE_MAIN",
        "stops": ["ROOM_102", "ROOM_RADIOLOGY", "ROOM_PHARMACY"],
        "travel_mode": "walk",
        "blocked_nodes": []
    }
    """
    data = request.get_json(silent=True) or {}
    start_id = data.get("start")
    stops = data.get("stops", [])
    travel_mode = data.get("travel_mode", "walk")
    blocked_nodes = data.get("blocked_nodes", [])

    if not start_id or not stops:
        return jsonify({
            "success": False,
            "error": "Both 'start' location and a list of 'stops' are required."
        }), 400

    result = nav_service.plan_multi_stop_route(
        start_id=start_id,
        stops_list=stops,
        travel_mode=travel_mode,
        blocked_nodes=blocked_nodes
    )

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/fire-evacuate", methods=["POST"])
def fire_evacuate():
    """
    Emergency Code Red Fire Evacuation API:
    Identifies the nearest ground-level fire exit, forces staircase escape,
    and strictly forbids elevator usage per safety regulations.
    Payload:
    {
        "current_location": "ROOM_102",
        "blocked_nodes": []
    }
    """
    data = request.get_json(silent=True) or {}
    current_location = data.get("current_location") or data.get("start")
    blocked_nodes = data.get("blocked_nodes", [])

    if not current_location:
        return jsonify({
            "success": False,
            "error": "Current location is required for emergency evacuation."
        }), 400

    result = nav_service.plan_fire_evacuation(
        current_location=current_location,
        blocked_nodes=blocked_nodes
    )

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/amenities", methods=["GET"])
def get_amenities_list():
    """Returns directory of searchable hospital amenity categories."""
    return jsonify({
        "success": True,
        "amenities": get_amenity_categories()
    })


@app.route("/api/nearest-amenity", methods=["POST"])
def get_nearest_amenity():
    """
    1-Click Nearest Amenities Finder:
    Calculates Dijkstra shortest path from patient's current location to the
    closest available amenity (Restroom, Drinking Water, Pharmacy, Cafeteria, ATM, Lift).
    """
    data = request.get_json(silent=True) or {}
    start_id = data.get("start") or data.get("current_location") or "ENTRANCE_MAIN"
    amenity_type = data.get("amenity_type") or "restroom"
    travel_mode = data.get("travel_mode", "walk")
    blocked_nodes = data.get("blocked_nodes", [])

    result = nav_service.find_nearest_amenity(
        start_id=start_id,
        amenity_type=amenity_type,
        travel_mode=travel_mode,
        blocked_nodes=blocked_nodes
    )

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/blockable-facilities", methods=["GET"])
def get_blockable_facilities():
    """Returns list of corridor segments, lifts, and stairs that can be simulated as blocked."""
    blockable = [
        {"id": "STAIRS_1_F0", "name": "Staircase 1 (West - Ground)", "type": "stairs", "floor": 0, "icon": "🪜"},
        {"id": "STAIRS_2_F0", "name": "Staircase 2 (East - Ground)", "type": "stairs", "floor": 0, "icon": "🪜"},
        {"id": "LIFT_A_F0", "name": "Elevator / Lift A (Ground)", "type": "lift", "floor": 0, "icon": "🛗"},
        {"id": "LIFT_B_F0", "name": "Elevator / Lift B (Ground)", "type": "lift", "floor": 0, "icon": "🛗"},
        {"id": "HW_G_MAIN_CENTER", "name": "Ground Central Corridor (Wet Floor / Cleaning)", "type": "hallway", "floor": 0, "icon": "🚧"},
        {"id": "HW_G_MAIN_WEST", "name": "Ground West Corridor (Maintenance)", "type": "hallway", "floor": 0, "icon": "🚧"}
    ]
    return jsonify({
        "success": True,
        "blockable_facilities": blockable
    })


@app.route("/api/emergency-routes", methods=["GET"])
def get_emergency_routes():
    """Returns quick access emergency departments."""
    return jsonify({
        "success": True,
        "emergency_locations": hospital_graph.emergency_locations
    })


@app.route("/api/qr-locations", methods=["GET"])
def get_qr_locations():
    """Returns wall/pillar QR code markers."""
    qr_markers = []
    for node_id, node in hospital_graph.nodes.items():
        if "qr_code" in node:
            qr_markers.append({
                "qr_code": node["qr_code"],
                "node_id": node_id,
                "name": node["name"],
                "floor": node["floor"],
                "floor_name": hospital_graph.floors[node["floor"]]["name"]
            })
    return jsonify({
        "success": True,
        "markers": qr_markers
    })


@app.route("/api/search-symptoms", methods=["GET"])
def search_symptoms():
    """Bilingual symptom-to-doctor & room search engine."""
    q = request.args.get("q", "").strip()
    results = search_symptoms_and_doctors(q)
    return jsonify({
        "success": True,
        "query": q,
        "results": results
    })


@app.route("/api/queue-status", methods=["POST"])
def queue_status():
    """Live OPD token queue analytics and wait times."""
    data = request.get_json(silent=True) or {}
    doctor_id = data.get("doctor_id")
    patient_token = data.get("patient_token")
    if patient_token is not None:
        try:
            patient_token = int(patient_token)
        except (ValueError, TypeError):
            patient_token = None

    if not doctor_id:
        return jsonify({"success": False, "error": "Missing 'doctor_id'"}), 400

    info = get_doctor_queue_info(doctor_id, patient_token)
    return jsonify(info), 200 if info.get("success") else 400


@app.route("/api/optimize-journey", methods=["POST"])
def optimize_journey():
    """Smart journey queue optimizer: reorders stops to save waiting time."""
    data = request.get_json(silent=True) or {}
    start = data.get("start", "ENTRANCE_MAIN")
    stops = data.get("stops", [])
    patient_token = data.get("patient_token")
    if patient_token is not None:
        try:
            patient_token = int(patient_token)
        except (ValueError, TypeError):
            patient_token = None

    result = optimize_multistop_order_by_queue(start, stops, patient_token)
    return jsonify(result), 200


@app.route("/api/crowd-density", methods=["GET"])
def crowd_density():
    """Live crowd density and rush metrics across all floors and hubs."""
    return jsonify(get_crowd_density()), 200


if __name__ == "__main__":
    print("=" * 65)
    print("🏥 Hospital Navigation System (Multi-Mode Dijkstra with Rerouting)")
    print("⚡ Server running at: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(host="127.0.0.1", port=5000, debug=True)
