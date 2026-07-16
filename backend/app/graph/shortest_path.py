from typing import List, Dict, Optional
from app.graph.network import GraphManager
import networkx as nx
import structlog

logger = structlog.get_logger()


class PathFinder:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        try:
            return nx.shortest_path(self.graph.graph, source=source, target=target)
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound:
            return None

    def shortest_path_length(self, source: str, target: str) -> Optional[int]:
        try:
            return nx.shortest_path_length(self.graph.graph, source=source, target=target)
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound:
            return None

    def all_shortest_paths(self, source: str, target: str) -> List[List[str]]:
        try:
            return list(nx.all_shortest_paths(self.graph.graph, source=source, target=target))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def dijkstra_path(self, source: str, target: str) -> Optional[List[str]]:
        try:
            return nx.dijkstra_path(self.graph.graph, source=source, target=target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_path_details(self, path: List[str]) -> List[Dict]:
        details = []
        for i, node_id in enumerate(path):
            node_data = dict(self.graph.graph.nodes.get(node_id, {}))
            node_data["id"] = node_id
            node_data["step"] = i + 1

            if i < len(path) - 1:
                edge_data = self.graph.graph.edges[node_id, path[i + 1]]
                node_data["edge_type"] = edge_data.get("type", "unknown")

            details.append(node_data)
        return details
