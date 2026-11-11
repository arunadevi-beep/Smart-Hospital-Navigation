"""
Graph Data Structure & Adjacency List Builder
Manages nodes, weighted edges, bidirectional connections, accessibility filtering,
travel modes (walk, wheelchair, stretcher), and dynamic obstacle blockages.
"""
from hospital_data import NODES, EDGES, FLOORS, DOCTORS, EMERGENCY_LOCATIONS


class HospitalGraph:
    def __init__(self):
        self.nodes = NODES
        self.edges = EDGES
        self.floors = FLOORS
        self.doctors = DOCTORS
        self.emergency_locations = EMERGENCY_LOCATIONS
        self.adjacency_list = {}
        self._build_graph()

    def _build_graph(self):
        """Build bidirectional adjacency list with edge weights and attributes."""
        for node_id in self.nodes:
            self.adjacency_list[node_id] = []

        for edge in self.edges:
            u = edge["from"]
            v = edge["to"]
            weight = edge["distance"]
            edge_type = edge.get("type", "corridor")
            accessible = edge.get("accessible", True)

            if u in self.adjacency_list and v in self.adjacency_list:
                self.adjacency_list[u].append({
                    "neighbor": v,
                    "weight": weight,
                    "type": edge_type,
                    "accessible": accessible
                })
                self.adjacency_list[v].append({
                    "neighbor": u,
                    "weight": weight,
                    "type": edge_type,
                    "accessible": accessible
                })

    def get_neighbors(self, node_id, travel_mode="walk", blocked_nodes=None):
        """
        Returns list of valid neighbors for a given node.
        
        Travel Modes:
        - 'walk': User explicitly prefers STAIRS over elevators! Elevators have an added
                  wait-time penalty so stairs are chosen first. If the nearest stairs
                  is blocked, it automatically routes via the alternative stairs (e.g. Stairs 2).
                  If all stairs are blocked, it falls back to elevators.
        - 'wheelchair': Requires wheelchair accessibility (bypasses ALL stairs, strictly uses elevators/ramps).
        - 'stretcher': Bed elevator & wide corridors only, avoids stairs completely.
        
        Dynamic Obstacles:
        - blocked_nodes: set or list of node IDs currently blocked/under maintenance.
        """
        if node_id not in self.adjacency_list:
            return []

        blocked_set = set(blocked_nodes or [])

        # If current node itself is blocked, no exit
        if node_id in blocked_set:
            return []

        neighbors = []
        for edge in self.adjacency_list[node_id]:
            neighbor_id = edge["neighbor"]

            # Filter out dynamically blocked nodes
            if neighbor_id in blocked_set:
                continue

            edge_type = edge.get("type", "corridor")
            weight = edge["weight"]
            raw_dist = edge["weight"]

            # Mobility Mode Rules
            if travel_mode in ["wheelchair", "stretcher"]:
                # Wheelchair & Stretcher cannot use stairs under any circumstances
                if not edge["accessible"] or edge_type == "stairs":
                    continue
                neighbor_node = self.nodes.get(neighbor_id)
                if neighbor_node and neighbor_node.get("type") == "stairs":
                    continue
            elif travel_mode == "walk":
                # Healthy walkers prefer STAIRS over waiting for elevators!
                if edge_type == "lift":
                    weight = weight + 50  # Add elevator wait penalty for walkers
                elif edge_type == "stairs":
                    weight = weight  # Stairs are preferred!

            neighbors.append({
                "neighbor": neighbor_id,
                "weight": weight,
                "raw_distance": raw_dist,
                "type": edge_type,
                "accessible": edge["accessible"]
            })
        return neighbors

    def get_node(self, node_id):
        """Retrieve node metadata by ID."""
        return self.nodes.get(node_id)

    def find_doctor_by_id_or_keyword(self, query):
        """Find a doctor matching doctor_id, name, or specialty keyword."""
        query_lower = query.strip().lower()
        for doc in self.doctors:
            if doc["id"].lower() == query_lower:
                return doc

        for doc in self.doctors:
            if (query_lower in doc["name"].lower() or 
                query_lower in doc["specialty"].lower() or 
                query_lower in doc["department"].lower() or
                any(k in query_lower for k in doc.get("keywords", []))):
                return doc

        return None

    def get_room_for_doctor(self, doctor_id):
        """Find corresponding room node ID for a doctor."""
        for doc in self.doctors:
            if doc["id"] == doctor_id:
                return doc["room_id"]
        return None

    def to_dict(self):
        """Export serialized layout for frontend map rendering."""
        return {
            "floors": self.floors,
            "nodes": self.nodes,
            "edges": self.edges,
            "doctors": self.doctors,
            "emergency_locations": self.emergency_locations
        }
