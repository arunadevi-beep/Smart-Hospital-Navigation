"""
Navigation Service & Step-by-Step Direction Generator
Converts Dijkstra node paths into intuitive human-readable directions in both English & Tamil.
Supports Travel Modes (Walk, Wheelchair, Stretcher) and Dynamic Obstacle Reroute Alerts.
"""
from dijkstra import dijkstra_shortest_path


class NavigationService:
    def __init__(self, graph):
        self.graph = graph

    def resolve_destination(self, destination_query, is_doctor=False):
        """Resolves destination query into room node ID and optional doctor profile."""
        if is_doctor:
            doc = self.graph.find_doctor_by_id_or_keyword(destination_query)
            if doc:
                return doc["room_id"], doc
            return None, None

        if destination_query in self.graph.nodes:
            room_node = self.graph.get_node(destination_query)
            doc_id = room_node.get("doctor_id")
            doc = self.graph.find_doctor_by_id_or_keyword(doc_id) if doc_id else None
            return destination_query, doc

        doc = self.graph.find_doctor_by_id_or_keyword(destination_query)
        if doc:
            return doc["room_id"], doc

        return None, None

    def plan_route(self, start_id, destination_query, is_doctor=False, travel_mode="walk", blocked_nodes=None):
        """
        Plans optimal route with travel mode and blocked obstacles handling.
        """
        dest_node_id, doctor_info = self.resolve_destination(destination_query, is_doctor=is_doctor)

        if not dest_node_id:
            return {
                "success": False,
                "error": f"Could not find hospital department, room, or doctor matching '{destination_query}'."
            }

        # Run Dijkstra Shortest Path
        result = dijkstra_shortest_path(
            self.graph,
            start_id=start_id,
            end_id=dest_node_id,
            travel_mode=travel_mode,
            blocked_nodes=blocked_nodes
        )

        if not result["success"]:
            return result

        if doctor_info:
            result["doctor"] = doctor_info

        # Generate Bilingual Directions
        steps_en, steps_ta = self._generate_step_directions(result["path_details"], doctor_info, travel_mode)
        result["instructions_en"] = steps_en
        result["instructions_ta"] = steps_ta

        start_name = self.graph.get_node(start_id)["name"]
        dest_name = doctor_info["room_name"] if doctor_info else self.graph.get_node(dest_node_id)["name"]

        result["summary"] = {
            "start": start_name,
            "destination": dest_name,
            "distance_meters": result["total_distance"],
            "walking_time_mins": result["estimated_minutes"],
            "steps_count": result["estimated_steps"],
            "floor_count": len(result["floors_traversed"]),
            "travel_mode": travel_mode,
            "rerouted": result["rerouted"],
            "blocked_count": len(result.get("blocked_nodes", []))
        }

        # Dynamic Obstacle Alert Note
        if result["rerouted"]:
            blocked_names = [self.graph.get_node(n).get("name", n) for n in result["blocked_nodes"] if self.graph.get_node(n)]
            names_str = ", ".join(blocked_names)
            result["reroute_alert_en"] = f"⚠️ Notice: Path rerouted to avoid blocked/maintenance areas: {names_str}."
            result["reroute_alert_ta"] = f"⚠️ தகவல்: {names_str} பகுதிகளில் தடை/பராமரிப்பு உள்ளதால் மாற்று வழியாக புதிய பாதை கணக்கிடப்பட்டது."

        return result

    def plan_multi_stop_route(self, start_id, stops_list, travel_mode="walk", blocked_nodes=None):
        """
        Plans a sequential Multi-Stop Journey (e.g. Entrance -> Doctor -> Scan -> Pharmacy).
        Executes chained Dijkstra for each leg and aggregates metrics and staged instructions.
        """
        if not stops_list or len(stops_list) == 0:
            return {"success": False, "error": "At least one destination stop is required."}

        # Resolve all stops
        resolved_stops = []
        for query in stops_list:
            node_id, doc = self.resolve_destination(query, is_doctor=False)
            if not node_id:
                # Try doctor lookup
                doc = self.graph.find_doctor_by_id_or_keyword(query)
                if doc:
                    node_id = doc["room_id"]
            if not node_id or node_id not in self.graph.nodes:
                return {"success": False, "error": f"Invalid stop in journey: '{query}'"}
            resolved_stops.append({"node_id": node_id, "doctor": doc, "query": query})

        # Calculate each leg
        legs = []
        current_start = start_id
        combined_path_nodes = []
        combined_path_details = []
        total_distance = 0
        total_minutes = 0
        total_steps = 0
        all_floors_set = set()

        instructions_en = []
        instructions_ta = []
        step_counter = 1

        for idx, stop in enumerate(resolved_stops):
            target_id = stop["node_id"]
            target_name = self.graph.get_node(target_id)["name"]
            extra = f" ({stop['doctor']['name']})" if stop.get("doctor") else ""
            stop_title = f"{target_name}{extra}"

            leg_res = dijkstra_shortest_path(
                self.graph,
                start_id=current_start,
                end_id=target_id,
                travel_mode=travel_mode,
                blocked_nodes=blocked_nodes
            )

            if not leg_res["success"]:
                return {
                    "success": False,
                    "error": f"Unreachable stop #{idx + 1} ({target_name}): {leg_res.get('error')}"
                }

            legs.append({
                "leg_index": idx + 1,
                "from_node": current_start,
                "to_node": target_id,
                "stop_title": stop_title,
                "distance": leg_res["total_distance"],
                "minutes": leg_res["estimated_minutes"],
                "path_nodes": leg_res["path_nodes"]
            })

            total_distance += leg_res["total_distance"]
            total_minutes += leg_res["estimated_minutes"]
            total_steps += leg_res["estimated_steps"]
            for f in leg_res["floors_traversed"]:
                all_floors_set.add(f)

            # Stage Header in instructions
            stage_num = idx + 1
            instructions_en.append({
                "step": step_counter,
                "icon": "🛑",
                "text": f"STAGE {stage_num}: Head to Stop #{stage_num} — {stop_title}.",
                "type": "stage_header"
            })
            instructions_ta.append({
                "step": step_counter,
                "icon": "🛑",
                "text": f"பகுதி {stage_num}: நிறுத்தம் #{stage_num} — {stop_title}-க்கு செல்லவும்.",
                "type": "stage_header"
            })
            step_counter += 1

            # Leg step directions
            leg_en, leg_ta = self._generate_step_directions(leg_res["path_details"], stop.get("doctor"), travel_mode)
            for s_en, s_ta in zip(leg_en, leg_ta):
                s_en["step"] = step_counter
                s_ta["step"] = step_counter
                instructions_en.append(s_en)
                instructions_ta.append(s_ta)
                step_counter += 1

            # Merge node sequence (avoid duplicate join node)
            if idx == 0:
                combined_path_nodes.extend(leg_res["path_nodes"])
                combined_path_details.extend(leg_res["path_details"])
            else:
                combined_path_nodes.extend(leg_res["path_nodes"][1:])
                combined_path_details.extend(leg_res["path_details"][1:])

            # Mark this node as a stop waypoint
            combined_path_details[-1]["is_stop"] = True
            combined_path_details[-1]["stop_number"] = stage_num
            combined_path_details[-1]["stop_name"] = stop_title

            current_start = target_id

        # Mark final destination
        combined_path_details[-1]["is_final_destination"] = True

        return {
            "success": True,
            "is_multi_stop": True,
            "total_distance": round(total_distance, 1),
            "estimated_minutes": total_minutes,
            "estimated_steps": total_steps,
            "travel_mode": travel_mode,
            "floors_traversed": sorted(list(all_floors_set)),
            "path_nodes": combined_path_nodes,
            "path_details": combined_path_details,
            "legs": legs,
            "instructions_en": instructions_en,
            "instructions_ta": instructions_ta,
            "summary": {
                "start": self.graph.get_node(start_id)["name"],
                "destination": f"Multi-Stop Journey ({len(resolved_stops)} stops)",
                "distance_meters": round(total_distance, 1),
                "walking_time_mins": total_minutes,
                "steps_count": total_steps,
                "floor_count": len(all_floors_set),
                "stops_count": len(resolved_stops),
                "travel_mode": travel_mode,
                "rerouted": bool(blocked_nodes and len(blocked_nodes) > 0)
            }
        }

    def plan_fire_evacuation(self, current_location, blocked_nodes=None):
        """
        Emergency Code Red Fire Evacuation Route.
        Rule 1: Elevators are strictly FORBIDDEN in a fire emergency!
        Rule 2: Identifies the quickest safe fire exit door from current location.
        """
        if current_location not in self.graph.nodes:
            return {"success": False, "error": f"Invalid location: '{current_location}'"}

        # Fire safety: All elevators are inoperable
        fire_blocked = set(blocked_nodes or [])
        for node_id, node in self.graph.nodes.items():
            if node.get("type") == "lift":
                fire_blocked.add(node_id)

        # Ground floor fire exits and arrival gates
        fire_exits = ["FIRE_EXIT_WEST", "FIRE_EXIT_EAST", "ENTRANCE_MAIN"]

        best_route = None
        best_exit = None
        min_distance = float('inf')

        for exit_id in fire_exits:
            if exit_id in fire_blocked or exit_id not in self.graph.nodes:
                continue

            res = dijkstra_shortest_path(
                self.graph,
                start_id=current_location,
                end_id=exit_id,
                travel_mode="walk",
                blocked_nodes=fire_blocked
            )

            if res["success"] and res["total_distance"] < min_distance:
                min_distance = res["total_distance"]
                best_route = res
                best_exit = exit_id

        if not best_route:
            return {
                "success": False,
                "error": "No safe fire exit path found! Use nearest emergency fire staircase."
            }

        exit_node = self.graph.get_node(best_exit)
        exit_name = exit_node["name"]

        # Urgent Fire Directions
        steps_en = [
            {
                "step": 1,
                "icon": "🔥",
                "text": "CRITICAL CODE RED: Fire Alarm Active. DO NOT USE ELEVATORS!",
                "type": "fire_alert"
            },
            {
                "step": 2,
                "icon": "🚪🏃",
                "text": f"Proceed immediately via Fire Staircase towards {exit_name}.",
                "type": "fire_action"
            }
        ]
        steps_ta = [
            {
                "step": 1,
                "icon": "🔥",
                "text": "அவசர தீ எச்சரிக்கை (CODE RED): லிஃப்ட்டை பயன்படுத்த வேண்டாம்!",
                "type": "fire_alert"
            },
            {
                "step": 2,
                "icon": "🚪🏃",
                "text": f"தீயணைப்பு படிக்கட்டுகள் வழியாக உடனடியாக {exit_name}-க்கு வெளியேறவும்.",
                "type": "fire_action"
            }
        ]

        leg_en, leg_ta = self._generate_step_directions(best_route["path_details"], None, travel_mode="walk")
        curr_step = 3
        for se, st in zip(leg_en, leg_ta):
            se["step"] = curr_step
            st["step"] = curr_step
            steps_en.append(se)
            steps_ta.append(st)
            curr_step += 1

        best_route["is_fire_evacuation"] = True
        best_route["nearest_exit"] = exit_name
        best_route["instructions_en"] = steps_en
        best_route["instructions_ta"] = steps_ta
        best_route["alert_message_en"] = f"🔥 FIRE EVACUATION ROUTE ACTIVE: Evacuating to {exit_name} (Lifts Disabled)."
        best_route["alert_message_ta"] = f"🔥 அவசர தீயணைப்பு வெளியேறும் பாதை: {exit_name} நோக்கி வெளியேறவும் (லிஃப்ட் துண்டிக்கப்பட்டது)."

        best_route["summary"] = {
            "start": self.graph.get_node(current_location)["name"],
            "destination": f"🔥 Nearest Fire Exit: {exit_name}",
            "distance_meters": best_route["total_distance"],
            "walking_time_mins": best_route["estimated_minutes"],
            "steps_count": best_route["estimated_steps"],
            "floor_count": len(best_route["floors_traversed"]),
            "travel_mode": "Emergency Evacuation (Stairs Only)",
            "is_fire_evacuation": True
        }

        return best_route

    def _generate_step_directions(self, path_details, doctor_info=None, travel_mode="walk"):
        """Generates turn-by-turn guidance tailored to travel mode."""
        steps_en = []
        steps_ta = []

        if len(path_details) <= 1:
            steps_en.append({
                "step": 1,
                "icon": "📍",
                "text": "You are currently at your destination.",
                "type": "arrival"
            })
            steps_ta.append({
                "step": 1,
                "icon": "📍",
                "text": "நீங்கள் ஏற்கனவே நீங்கள் செல்ல வேண்டிய இடத்தில் தான் உள்ளீர்கள்.",
                "type": "arrival"
            })
            return steps_en, steps_ta

        step_num = 1
        start_node = path_details[0]
        floor_name = self.graph.floors.get(start_node["floor"], {}).get("name", f"Floor {start_node['floor']}")

        mode_prefix_en = "🚶 Walk" if travel_mode == "walk" else ("♿ Roll wheelchair" if travel_mode == "wheelchair" else "🛏️ Move stretcher")
        mode_prefix_ta = "🚶 புறப்படவும்" if travel_mode == "walk" else ("♿ வீல்சேரை நகர்த்தவும்" if travel_mode == "wheelchair" else "🛏️ ஸ்ட்ரெச்சரை நகர்த்தவும்")

        steps_en.append({
            "step": step_num,
            "icon": "🚶" if travel_mode == "walk" else ("♿" if travel_mode == "wheelchair" else "🛏️"),
            "text": f"Start from {start_node['name']} ({floor_name}) - {mode_prefix_en}.",
            "type": "depart",
            "node_id": start_node["id"],
            "floor": start_node["floor"]
        })
        steps_ta.append({
            "step": step_num,
            "icon": "🚶" if travel_mode == "walk" else ("♿" if travel_mode == "wheelchair" else "🛏️"),
            "text": f"{start_node['name']} ({floor_name})-ல் இருந்து {mode_prefix_ta}.",
            "type": "depart",
            "node_id": start_node["id"],
            "floor": start_node["floor"]
        })
        step_num += 1

        i = 1
        while i < len(path_details):
            prev = path_details[i - 1]
            curr = path_details[i]

            # Multi-Floor Transition
            if curr["floor"] != prev["floor"]:
                via = curr.get("transition_via", "lift")
                target_floor = self.graph.floors.get(curr["floor"], {}).get("name", f"Floor {curr['floor']}")

                if via == "lift":
                    steps_en.append({
                        "step": step_num,
                        "icon": "🛗",
                        "text": f"Board Elevator ({prev['name']}) and go to {target_floor}.",
                        "type": "lift",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    steps_ta.append({
                        "step": step_num,
                        "icon": "🛗",
                        "text": f"{prev['name']} லிஃப்ட்டில் ஏறி {target_floor}-க்கு செல்லவும்.",
                        "type": "lift",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                else:
                    steps_en.append({
                        "step": step_num,
                        "icon": "🪜",
                        "text": f"Use the Staircase ({prev['name']}) up to {target_floor}.",
                        "type": "stairs",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    steps_ta.append({
                        "step": step_num,
                        "icon": "🪜",
                        "text": f"{prev['name']} படிக்கட்டுகள் வழியாக {target_floor}-க்கு செல்லவும்.",
                        "type": "stairs",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                step_num += 1
                i += 1
                continue

            # Arrival Step
            if i == len(path_details) - 1:
                dest_title = curr["name"]
                extra = f" ({doctor_info['name']} - {doctor_info['specialty']})" if doctor_info else ""
                steps_en.append({
                    "step": step_num,
                    "icon": "🏁",
                    "text": f"Arrive at destination: {dest_title}{extra}.",
                    "type": "arrival",
                    "node_id": curr["id"],
                    "floor": curr["floor"]
                })
                steps_ta.append({
                    "step": step_num,
                    "icon": "🏁",
                    "text": f"நீங்கள் சென்றடைய வேண்டிய இடம் வந்துவிட்டது: {dest_title}{extra}.",
                    "type": "arrival",
                    "node_id": curr["id"],
                    "floor": curr["floor"]
                })
                step_num += 1
                break

            # Turn calculation
            if i + 1 < len(path_details) and path_details[i + 1]["floor"] == curr["floor"]:
                nxt = path_details[i + 1]
                turn = self._calculate_turn(prev, curr, nxt)

                if turn == "left":
                    steps_en.append({
                        "step": step_num,
                        "icon": "⬅️",
                        "text": f"Turn left at {curr['name']} and continue straight.",
                        "type": "turn_left",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    steps_ta.append({
                        "step": step_num,
                        "icon": "⬅️",
                        "text": f"{curr['name']} அருகே இடதுபுறம் திரும்பி நேராக செல்லவும்.",
                        "type": "turn_left",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    step_num += 1
                elif turn == "right":
                    steps_en.append({
                        "step": step_num,
                        "icon": "➡️",
                        "text": f"Turn right at {curr['name']} along the corridor.",
                        "type": "turn_right",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    steps_ta.append({
                        "step": step_num,
                        "icon": "➡️",
                        "text": f"{curr['name']} அருகே வலதுபுறம் திரும்பி காரிடாரில் செல்லவும்.",
                        "type": "turn_right",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    step_num += 1
                else:
                    steps_en.append({
                        "step": step_num,
                        "icon": "⬆️",
                        "text": f"Continue straight past {curr['name']}.",
                        "type": "straight",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    steps_ta.append({
                        "step": step_num,
                        "icon": "⬆️",
                        "text": f"{curr['name']} கடந்து நேராக செல்லவும்.",
                        "type": "straight",
                        "node_id": curr["id"],
                        "floor": curr["floor"]
                    })
                    step_num += 1
            else:
                steps_en.append({
                    "step": step_num,
                    "icon": "⬆️",
                    "text": f"Proceed forward along hallway past {curr['name']}.",
                    "type": "straight",
                    "node_id": curr["id"],
                    "floor": curr["floor"]
                })
                steps_ta.append({
                    "step": step_num,
                    "icon": "⬆️",
                    "text": f"{curr['name']} வழியே தொடர்ந்து செல்லவும்.",
                    "type": "straight",
                    "node_id": curr["id"],
                    "floor": curr["floor"]
                })
                step_num += 1

            i += 1

        return steps_en, steps_ta

    def _calculate_turn(self, p1, p2, p3):
        dx1 = p2["x"] - p1["x"]
        dy1 = p2["y"] - p1["y"]
        dx2 = p3["x"] - p2["x"]
        dy2 = p3["y"] - p2["y"]

        cross = (dx1 * dy2) - (dy1 * dx2)
        if cross > 250:
            return "right"
        elif cross < -250:
            return "left"
        return "straight"

    def find_nearest_amenity(self, start_id, amenity_type, travel_mode="walk", blocked_nodes=None):
        """
        1-Click Nearest Amenities Finder:
        Finds the closest amenity node of the requested category (restroom, water, cafeteria, pharmacy, atm, lift)
        from start_id using Dijkstra shortest path.
        """
        from hospital_data import AMENITY_CATEGORIES

        if start_id not in self.graph.nodes:
            return {"success": False, "error": f"Invalid start location: '{start_id}'"}

        category = AMENITY_CATEGORIES.get(amenity_type)
        if not category:
            return {"success": False, "error": f"Unknown amenity type: '{amenity_type}'"}

        candidates = category["nodes"]
        best_route = None
        best_candidate = None
        min_distance = float('inf')

        for candidate_id in candidates:
            if candidate_id not in self.graph.nodes:
                continue
            if blocked_nodes and candidate_id in blocked_nodes:
                continue

            # If user is already at this candidate
            if candidate_id == start_id:
                start_node = self.graph.get_node(start_id)
                route_res = {
                    "success": True,
                    "total_distance": 0,
                    "estimated_minutes": 0,
                    "estimated_steps": 0,
                    "path": [start_id],
                    "path_details": [start_node],
                    "is_multi_floor": False,
                    "floors_traversed": [start_node["floor"]],
                    "travel_mode": travel_mode,
                    "instructions_en": [{
                        "step": 1,
                        "icon": category["icon"],
                        "text": f"You are already at {category['icon']} {start_node['name']}!",
                        "type": "destination",
                        "node_id": start_id,
                        "floor": start_node["floor"]
                    }],
                    "instructions_ta": [{
                        "step": 1,
                        "icon": category["icon"],
                        "text": f"நீங்கள் ஏற்கனவே {category['icon']} {start_node['name']}-ல் உள்ளீர்கள்!",
                        "type": "destination",
                        "node_id": start_id,
                        "floor": start_node["floor"]
                    }],
                    "summary": {
                        "start": start_node["name"],
                        "destination": start_node["name"],
                        "distance_meters": 0,
                        "walking_time_mins": 0,
                        "steps_count": 0,
                        "floor_count": 1,
                        "travel_mode": travel_mode
                    }
                }
            else:
                route_res = self.plan_route(
                    start_id=start_id,
                    destination_query=candidate_id,
                    is_doctor=False,
                    travel_mode=travel_mode,
                    blocked_nodes=blocked_nodes
                )

            if route_res.get("success") and route_res.get("total_distance", 0) < min_distance:
                min_distance = route_res["total_distance"]
                best_route = route_res
                best_candidate = candidate_id

        if not best_route:
            return {
                "success": False,
                "error": f"No accessible route found to any {category['title_en']} from your current location."
            }

        cand_node = self.graph.get_node(best_candidate)
        dest_name = cand_node["name"]
        dist_m = best_route["total_distance"]
        mins = best_route["estimated_minutes"]
        floor_num = cand_node["floor"]
        floor_name = self.graph.floors.get(floor_num, {}).get("name", f"Floor {floor_num}")

        best_route["is_amenity_route"] = True
        best_route["amenity_type"] = amenity_type
        best_route["amenity_icon"] = category["icon"]
        best_route["amenity_title"] = category["title_en"]
        best_route["amenity_title_ta"] = category["title_ta"]
        best_route["found_node_id"] = best_candidate
        best_route["found_name"] = dest_name
        best_route["found_floor"] = floor_num

        if dist_m == 0:
            alert_en = f"You are already at {category['icon']} {dest_name} ({floor_name})!"
            alert_ta = f"நீங்கள் ஏற்கனவே {category['icon']} {dest_name}-ல் உள்ளீர்கள்!"
        else:
            alert_en = f"Nearest {category['icon']} {category['title_en']}: {dest_name} on {floor_name} ({dist_m} m away, ~{mins} min walk)."
            alert_ta = f"அருகிலுள்ள {category['icon']} {category['title_ta']}: {dest_name} ({floor_name}, {dist_m} மீட்டர் தூரம், ~{mins} நிமிடம்)."

        best_route["amenity_alert_en"] = alert_en
        best_route["amenity_alert_ta"] = alert_ta

        return best_route
