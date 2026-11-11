"""
Comprehensive Test Suite:
1. Single Route & Walking Stairs Priority
2. Dynamic Obstacle Rerouting
3. Multi-Stop Journey Planner (Chained Dijkstra)
4. Emergency Code Red Fire Evacuation (No Lifts, Nearest Exit)
"""
from graph import HospitalGraph
from navigation_service import NavigationService


def run_tests():
    print("=" * 65)
    print("Hospital Navigation: Multi-Stop & Fire Evacuation Tests")
    print("=" * 65)

    graph = HospitalGraph()
    nav = NavigationService(graph)

    # 1. By Walk Default: Must use STAIRS (Staircase 1)
    res_walk = nav.plan_route("ENTRANCE_MAIN", "DOC_ORTHO_01", is_doctor=True, travel_mode="walk")
    assert res_walk["success"] is True, "Failed Walking route"
    assert "STAIRS_1_F0" in res_walk["path_nodes"], "Error: Expected Staircase 1 to be used!"
    print(f"\n1. 🚶 By Walk (Stairs Priority):")
    print(f"   - Selected: Staircase 1 (West)")
    print(f"   - Distance: {res_walk['total_distance']} m, Steps: {res_walk['estimated_steps']}")

    # 2. Block Staircase 1: Reroute to Staircase 2
    res_block_s1 = nav.plan_route(
        "ENTRANCE_MAIN", "DOC_ORTHO_01", is_doctor=True,
        travel_mode="walk",
        blocked_nodes=["STAIRS_1_F0"]
    )
    assert res_block_s1["success"] is True, "Failed to reroute via alternate stairs"
    assert "STAIRS_2_F0" in res_block_s1["path_nodes"], "Error: Expected alternate Staircase 2!"
    print(f"\n2. 🚧 Staircase 1 Blocked -> Reroute via Alternate Staircase 2: PASS ✅")

    # 3. Multi-Stop Journey: Entrance -> Orthology (Stop 1) -> Radiology (Stop 2) -> Pharmacy (Stop 3)
    print(f"\n3. 🏥 Multi-Stop Journey Planner (Doctor -> X-Ray -> Pharmacy):")
    stops = ["ROOM_102", "ROOM_RADIOLOGY", "ROOM_PHARMACY"]
    res_multistop = nav.plan_multi_stop_route("ENTRANCE_MAIN", stops, travel_mode="walk")
    assert res_multistop["success"] is True, "Failed multi-stop route planning"
    assert len(res_multistop["legs"]) == 3, "Error: Expected 3 legs in multi-stop journey"
    print(f"   - Total Combined Distance: {res_multistop['total_distance']} m")
    print(f"   - Total Est. Time: {res_multistop['estimated_minutes']} mins, Steps: {res_multistop['estimated_steps']}")
    print(f"   - Floors Visited: {res_multistop['floors_traversed']}")
    for leg in res_multistop["legs"]:
        print(f"     Leg {leg['leg_index']}: {leg['from_node']} -> {leg['to_node']} ({leg['stop_title']}, {leg['distance']}m)")
    print("   - Multi-Stop Journey: PASS ✅")

    # 4. Emergency Fire Evacuation from Floor 2 (ICU)
    print(f"\n4. 🔥 Emergency Code Red Fire Evacuation from Floor 2 (ICU):")
    res_fire_f2 = nav.plan_fire_evacuation("ROOM_ICU")
    assert res_fire_f2["success"] is True, "Failed fire evacuation"
    assert res_fire_f2["is_fire_evacuation"] is True
    # Verify NO elevators are used in fire evacuation
    has_lift = any("LIFT" in n for n in res_fire_f2["path_nodes"])
    assert not has_lift, "CRITICAL ERROR: Elevator used in fire evacuation route!"
    has_fire_stairs = any("STAIRS" in n for n in res_fire_f2["path_nodes"])
    assert has_fire_stairs, "Error: Staircase must be used to descend during fire evacuation!"
    print(f"   - Nearest Fire Exit: {res_fire_f2['nearest_exit']}")
    print(f"   - Escape Distance: {res_fire_f2['total_distance']} m (Stairs only, Lifts disabled)")
    print(f"   - Path: {' -> '.join(res_fire_f2['path_nodes'])}")
    print("   - Fire Evacuation from F2: PASS ✅")

    # 5. Emergency Fire Evacuation from Ground Floor (Reception)
    print(f"\n5. 🔥 Emergency Fire Evacuation from Ground Floor (Reception):")
    res_fire_g = nav.plan_fire_evacuation("RECEPTION")
    assert res_fire_g["success"] is True
    print(f"   - Nearest Fire Exit: {res_fire_g['nearest_exit']} ({res_fire_g['total_distance']} m)")
    print("   - Fire Evacuation from Ground: PASS ✅")

    # 6. Bilingual Symptom Search
    from hospital_data import search_symptoms_and_doctors, get_doctor_queue_info, optimize_multistop_order_by_queue
    print(f"\n6. 🔍 Bilingual Symptom to Doctor Smart Search:")
    sym_en = search_symptoms_and_doctors("headache")
    assert len(sym_en) > 0
    print(f"   - Query: 'headache' -> Match: {sym_en[0]['title_en']} ({sym_en[0]['target_node_name']})")
    sym_ta = search_symptoms_and_doctors("நெஞ்சு வலி")
    assert len(sym_ta) > 0
    print(f"   - Query: 'நெஞ்சு வலி' -> Match: {sym_ta[0]['title_ta']} ({sym_ta[0]['target_node_name']})")
    print("   - Symptom Smart Search: PASS ✅")

    # 7. Live Token Queue Analytics & Wait Time
    print(f"\n7. ⏱️ Live Token Queue Analytics:")
    queue = get_doctor_queue_info("DOC_ORTHO_01", patient_token=24)
    assert queue["patients_ahead"] == 10
    assert queue["estimated_wait_minutes"] == 40
    print(f"   - Doctor: {queue['doctor_name']} | Serving: #{queue['current_token']} | Patient Token: #{queue['patient_token']}")
    print(f"   - Patients Ahead: {queue['patients_ahead']} | Est. Wait: {queue['estimated_wait_minutes']} mins")
    print("   - Queue Analytics: PASS ✅")

    # 8. Smart Journey Queue Optimization
    print(f"\n8. 💡 Smart Journey Queue Optimization:")
    opt = optimize_multistop_order_by_queue("ENTRANCE_MAIN", ["ROOM_102", "ROOM_RADIOLOGY", "ROOM_PHARMACY"], patient_token=24)
    assert opt["can_optimize"] is True
    assert opt["optimized_stops"][0] == "ROOM_RADIOLOGY"
    print(f"   - Reordered to: {' -> '.join(opt['optimized_stops'])}")
    print(f"   - Time Saved: ~{opt['time_saved_mins']} minutes of idle OPD waiting!")
    print("   - Smart Journey Optimization: PASS ✅")

    # 9. Live Crowd Density & Rush Indicator API
    print(f"\n9. 🔥 Live Crowd Density & Rush Indicators:")
    from hospital_data import get_crowd_density
    from app import app
    crowd_res = get_crowd_density()
    assert crowd_res["success"] is True
    crowd_map = crowd_res["crowd_data"]
    assert "RECEPTION" in crowd_map
    assert "ROOM_PHARMACY" in crowd_map
    assert crowd_map["ROOM_PHARMACY"]["level"] == "high"
    print(f"   - Ground Floor Pharmacy Rush: {crowd_map['ROOM_PHARMACY']['percentage']}% ({crowd_map['ROOM_PHARMACY']['status_en']})")
    
    with app.test_client() as client:
        res = client.get("/api/crowd-density")
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert "crowd_data" in json_data
        assert "ROOM_101" in json_data["crowd_data"]
    print("   - Crowd Density API Endpoint: PASS ✅")

    # 10. 1-Click Nearest Amenities Finder
    print(f"\n10. ⚡ 1-Click Nearest Amenities Finder:")
    # Test 1: From Floor 1 (ROOM_102), find nearest Restroom -> should pick Floor 1 Restroom (50m)
    amenity_f1 = nav.find_nearest_amenity("ROOM_102", "restroom")
    assert amenity_f1["success"] is True
    assert amenity_f1["found_node_id"] == "RESTROOM_F1"
    assert amenity_f1["total_distance"] == 50
    print(f"   - From Room 102 (Floor 1): Found {amenity_f1['found_name']} ({amenity_f1['total_distance']} m) ✅")

    # Test 2: From Ground (ENTRANCE_MAIN), find nearest Restroom -> should pick Ground Restroom (40m)
    amenity_g = nav.find_nearest_amenity("ENTRANCE_MAIN", "restroom")
    assert amenity_g["success"] is True
    assert amenity_g["found_node_id"] == "RESTROOM_G"
    assert amenity_g["total_distance"] == 40
    print(f"   - From Entrance (Ground): Found {amenity_g['found_name']} ({amenity_g['total_distance']} m) ✅")

    # Test 3: From Floor 2 (ROOM_201), find nearest Restroom -> should pick Floor 2 Restroom
    amenity_f2 = nav.find_nearest_amenity("ROOM_201", "restroom")
    assert amenity_f2["success"] is True
    assert amenity_f2["found_node_id"] == "RESTROOM_F2"
    print(f"   - From Room 201 (Floor 2): Found {amenity_f2['found_name']} ({amenity_f2['total_distance']} m) ✅")

    # Test 4: Dynamic Obstacle Fallback (Ground hallway HW_G_S_WEST blocked -> reroutes to Floor 1 Restroom)
    amenity_blocked = nav.find_nearest_amenity("ENTRANCE_MAIN", "restroom", blocked_nodes=["HW_G_S_WEST"])
    assert amenity_blocked["success"] is True
    assert amenity_blocked["found_node_id"] == "RESTROOM_F1"
    print(f"   - Ground Restroom Blocked: Successfully rerouted to {amenity_blocked['found_name']} ({amenity_blocked['total_distance']} m) ✅")

    # Test 5: Nearest Drinking Water & Pharmacy via Flask API
    with app.test_client() as client:
        r_amenities = client.get("/api/amenities")
        assert r_amenities.status_code == 200
        assert "restroom" in r_amenities.get_json()["amenities"]

        r_near = client.post("/api/nearest-amenity", json={"start": "ROOM_102", "amenity_type": "water"})
        assert r_near.status_code == 200
        near_json = r_near.get_json()
        assert near_json["success"] is True
        assert near_json["found_node_id"] == "WAITING_LOUNGE_F1"
    print(f"   - Nearest Drinking Water API: Found {near_json['found_name']} ({near_json['total_distance']} m) ✅")
    print("   - 1-Click Nearest Amenities Finder: PASS ✅")

    print("\n" + "=" * 65)
    print("🎉 ALL 10 TESTS (ROUTING, MULTI-STOP, FIRE, SEARCH, QUEUE, CROWD, AMENITIES) PASSED!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
