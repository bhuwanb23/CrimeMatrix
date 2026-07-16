import networkx as nx
from typing import List, Dict, Optional
import structlog

logger = structlog.get_logger()


class GraphManager:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node_id: str, node_type: str, **attrs):
        self.graph.add_node(node_id, type=node_type, **attrs)
        logger.debug("graph_node_added", node_id=node_id, node_type=node_type)

    def add_edge(self, source: str, target: str, edge_type: str, **attrs):
        self.graph.add_edge(source, target, type=edge_type, **attrs)
        logger.debug("graph_edge_added", source=source, target=target, edge_type=edge_type)

    def get_neighbors(self, node_id: str) -> List[Dict]:
        neighbors = []
        for neighbor in self.graph.neighbors(node_id):
            edge_data = self.graph.edges[node_id, neighbor]
            neighbors.append({
                "id": neighbor,
                "type": self.graph.nodes[neighbor].get("type", "unknown"),
                "edge_type": edge_data.get("type", "unknown"),
            })
        return neighbors

    def find_paths(self, source: str, target: str, max_length: int = 3) -> List[List[str]]:
        try:
            return list(nx.all_simple_paths(self.graph, source, target, cutoff=max_length))
        except nx.NetworkXError:
            return []

    def get_subgraph(self, node_id: str, depth: int = 2) -> nx.Graph:
        nodes = set()
        nodes.add(node_id)
        current_level = {node_id}
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in nodes:
                        next_level.add(neighbor)
                        nodes.add(neighbor)
            current_level = next_level
        return self.graph.subgraph(nodes).copy()

    def get_communities(self) -> List[List[str]]:
        try:
            return [list(c) for c in nx.community.greedy_modularity_communities(self.graph)]
        except Exception:
            return [list(self.graph.nodes)]

    def clear(self):
        self.graph.clear()
