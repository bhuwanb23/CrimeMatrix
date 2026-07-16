from typing import List, Dict
from app.graph.network import GraphManager
import structlog

logger = structlog.get_logger()


class NeighborFinder:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def get_neighbors(self, node_id: str) -> List[Dict]:
        neighbors = []
        for neighbor in self.graph.graph.neighbors(node_id):
            edge_data = self.graph.graph.edges[node_id, neighbor]
            node_data = dict(self.graph.graph.nodes.get(neighbor, {}))
            node_data["id"] = neighbor
            node_data["edge_type"] = edge_data.get("type", "unknown")
            neighbors.append(node_data)
        return neighbors

    def get_neighbors_by_type(self, node_id: str, edge_type: str) -> List[Dict]:
        neighbors = []
        for neighbor in self.graph.graph.neighbors(node_id):
            edge_data = self.graph.graph.edges[node_id, neighbor]
            if edge_data.get("type") == edge_type:
                node_data = dict(self.graph.graph.nodes.get(neighbor, {}))
                node_data["id"] = neighbor
                node_data["edge_type"] = edge_type
                neighbors.append(node_data)
        return neighbors

    def get_n_degree_neighbors(self, node_id: str, degree: int = 2) -> List[Dict]:
        visited = set()
        result = []
        current_level = {node_id}

        for _ in range(degree):
            next_level = set()
            for node in current_level:
                if node in visited:
                    continue
                visited.add(node)
                for neighbor in self.graph.graph.neighbors(node):
                    if neighbor not in visited:
                        next_level.add(neighbor)
                        node_data = dict(self.graph.graph.nodes.get(neighbor, {}))
                        node_data["id"] = neighbor
                        result.append(node_data)
            current_level = next_level

        return result
