"""
Dijkstra's Shortest Path Algorithm for Hospital Navigation
Supports:
1. Travel Modes:
   - 'walk': Prefers STAIRS over Elevators. If nearest stairs is blocked, routes via alternate stairs.
   - 'wheelchair': Elevators only, strictly avoids stairs.
   - 'stretcher': Bed elevators & wide corridors only.
2. Dynamic Obstacle Blockage & Real-Time Rerouting
3. Multi-Floor Transitions & Accurate Physical Meter Calculation
"""
import heapq
import math


def dijkstra_shortest_path(graph, start_id, end_id, travel_mode="walk", blocked_nodes=None):
    """
    Executes Dijkstra's algorithm on the hospital graph with constraints.
    """
    blocked_set = set(blocked_nodes or [])

    if start_id not in graph.nodes:
        return {"success": False, "error": f"Invalid start location: '{start_id}'"}
    if end_id not in graph.nodes:
        return {"success": False, "error": f"Invalid destination: '{end_id}'"}

    if start_id in blocked_set:
        start_name = graph.get_node(start_id).get("name", start_id)
        return {"success": False, "error": f"Your starting location '{start_name}' is currently blocked or under maintenance."}
    if end_id in blocked_set:
        dest_name = graph.get_node(end_id).get("name", end_id)
        return {"success": False, "error": f"Destination '{dest_name}' is currently closed or under maintenance."}

    if start_id == end_id:
        start_node = graph.get_node(start_id)
        return {
            "success": True,
            "total_distance": 0,
            "estimated_minutes": 0,
            "estimated_steps": 0,
            "travel_mode": travel_mode,
            "blocked_nodes": list(blocked_set),
            "rerouted": False,
            "path_nodes": [start_id],
            "path_details": [{
                "id": start_id,
                "name": start_node["name"],
                "floor": start_node["floor"],
                "x": start_node["x"],
                "y": start_node["y"],
                "type": start_node["type"]
            }],
            "floor_segments": {start_node["floor"]: [start_id]},
            "floors_traversed": [start_node["floor"]],
            "message": "You are already at your destination!"
        }

    # Dijkstra Data Structures
    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_id] = 0
    previous = {}
    edge_meta = {}

    pq = [(0, start_id)]
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end_id:
            break

        if current_distance > distances[current_node]:
            continue

        neighbors = graph.get_neighbors(current_node, travel_mode=travel_mode, blocked_nodes=blocked_set)
        for edge in neighbors:
            neighbor_id = edge["neighbor"]
            weight = edge["weight"]

            if neighbor_id in visited:
                continue

            new_distance = current_distance + weight

            if new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                previous[neighbor_id] = current_node
                edge_meta[neighbor_id] = edge
                heapq.heappush(pq, (new_distance, neighbor_id))

    # Reachability Check
    if distances[end_id] == float('inf'):
        if blocked_set:
            reason = "Destination unreachable due to active corridor/staircase maintenance blocks. Try clearing blocked paths."
        elif travel_mode in ["wheelchair", "stretcher"]:
            reason = f"No accessible route found for {travel_mode} mode (elevators may be unreachable or path requires stairs)."
        else:
            reason = "Destination is currently unreachable."
        return {
            "success": False,
            "error": reason
        }

    # Path Reconstruction
    path_nodes = []
    curr = end_id
    while curr is not None:
        path_nodes.append(curr)
        curr = previous.get(curr)
    path_nodes.reverse()

    # Calculate actual physical meters (using true edge raw distances)
    actual_physical_distance = 0
    for idx in range(1, len(path_nodes)):
        u = path_nodes[idx - 1]
        v = path_nodes[idx]
        for e in graph.adjacency_list.get(u, []):
            if e["neighbor"] == v:
                actual_physical_distance += e["weight"]
                break

    path_details = []
    floor_segments = {}
    floors_traversed_set = []

    for idx, node_id in enumerate(path_nodes):
        node_info = graph.get_node(node_id)
        floor = node_info["floor"]

        if floor not in floors_traversed_set:
            floors_traversed_set.append(floor)

        if floor not in floor_segments:
            floor_segments[floor] = []
        floor_segments[floor].append(node_id)

        transition_type = None
        if idx > 0:
            edge_info = edge_meta.get(node_id, {})
            transition_type = edge_info.get("type", "corridor")

        path_details.append({
            "id": node_id,
            "name": node_info.get("name", node_id),
            "floor": floor,
            "x": node_info.get("x", 0),
            "y": node_info.get("y", 0),
            "door_x": node_info.get("door_x"),
            "door_y": node_info.get("door_y"),
            "type": node_info.get("type", "corridor"),
            "transition_via": transition_type
        })

    total_dist = round(actual_physical_distance, 1)

    speed_map = {"walk": 66.0, "wheelchair": 50.0, "stretcher": 40.0}
    speed = speed_map.get(travel_mode, 66.0)

    has_floor_change = len(floors_traversed_set) > 1
    walk_minutes = total_dist / speed
    if has_floor_change:
        # Buffer for stairs climb or elevator wait
        walk_minutes += 0.5 * (len(floors_traversed_set) - 1)
    estimated_minutes = max(1, math.ceil(walk_minutes))

    if travel_mode == "walk":
        estimated_steps = int(round(total_dist / 0.75))
    else:
        estimated_steps = 0

    return {
        "success": True,
        "total_distance": total_dist,
        "estimated_minutes": estimated_minutes,
        "estimated_steps": estimated_steps,
        "travel_mode": travel_mode,
        "blocked_nodes": list(blocked_set),
        "rerouted": len(blocked_set) > 0,
        "path_nodes": path_nodes,
        "path_details": path_details,
        "floor_segments": floor_segments,
        "floors_traversed": floors_traversed_set
    }
