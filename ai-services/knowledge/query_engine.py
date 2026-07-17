import networkx as nx
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()


class GraphQueryEngine:
    def __init__(self, graph: nx.Graph = None):
        self.graph = graph or nx.Graph()

    def crimes_linked_to(self, node_id: str) -> List[Dict]:
        results = []
        if not self.graph.has_node(node_id):
            return results
        for neighbor in self.graph.neighbors(node_id):
            data = dict(self.graph.nodes[neighbor])
            if data.get("type") == "crime":
                edge_data = self.graph.edges[node_id, neighbor]
                results.append({"node_id": neighbor, "relation": edge_data.get("relation", ""), **data})
        return results

    def suspects_in_crime(self, crime_id: str) -> List[Dict]:
        results = []
        node_id = crime_id if crime_id.startswith("crime_") else f"crime_{crime_id}"
        if not self.graph.has_node(node_id):
            return results
        for neighbor in self.graph.neighbors(node_id):
            data = dict(self.graph.nodes[neighbor])
            if data.get("type") == "person":
                edge_data = self.graph.edges[node_id, neighbor]
                results.append({"node_id": neighbor, "relation": edge_data.get("relation", ""), **data})
        return results

    def common_crimes(self, node1: str, node2: str) -> List[Dict]:
        if not self.graph.has_node(node1) or not self.graph.has_node(node2):
            return []
        neighbors1 = set(self.graph.neighbors(node1))
        neighbors2 = set(self.graph.neighbors(node2))
        common = neighbors1 & neighbors2
        results = []
        for n in common:
            data = dict(self.graph.nodes[n])
            if data.get("type") == "crime":
                results.append({"node_id": n, **data})
        return results

    def find_paths(self, source: str, target: str, max_length: int = 5) -> List[List[str]]:
        try:
            return list(nx.all_simple_paths(self.graph, source, target, cutoff=max_length))
        except (nx.NetworkXError, nx.NodeNotFound):
            return []

    def subgraph(self, node_id: str, depth: int = 2) -> nx.Graph:
        if not self.graph.has_node(node_id):
            return nx.Graph()
        nodes = set()
        current = {node_id}
        for _ in range(depth):
            next_level = set()
            for n in current:
                if n not in nodes:
                    nodes.add(n)
                    next_level.update(self.graph.neighbors(n))
            current = next_level
        return self.graph.subgraph(nodes).copy()

    def search_nodes(self, query: str, node_type: str = None) -> List[Dict]:
        results = []
        query_lower = query.lower()
        for node_id, data in self.graph.nodes(data=True):
            name = str(data.get("name", "")).lower()
            if query_lower in name or query_lower in node_id.lower():
                if node_type and data.get("type") != node_type:
                    continue
                results.append({"node_id": node_id, **data})
        return results
