import networkx as nx
from typing import Dict, List, Optional
from storage.base import GraphProvider
import structlog

logger = structlog.get_logger()


class NetworkXProvider(GraphProvider):
    def __init__(self):
        self.graph = nx.Graph()

    async def connect(self):
        logger.info("networkx_connected")

    async def disconnect(self):
        pass

    async def add_node(self, node_id: str, node_type: str = "", **attrs):
        self.graph.add_node(node_id, type=node_type, **attrs)

    async def add_edge(self, source: str, target: str, relation: str = "", **attrs):
        self.graph.add_edge(source, target, relation=relation, **attrs)

    async def get_node(self, node_id: str) -> Optional[Dict]:
        if self.graph.has_node(node_id):
            data = dict(self.graph.nodes[node_id])
            data["id"] = node_id
            return data
        return None

    async def get_neighbors(self, node_id: str, edge_type: str = None) -> List[Dict]:
        results = []
        if not self.graph.has_node(node_id):
            return results
        for neighbor in self.graph.neighbors(node_id):
            edge_data = dict(self.graph.edges[node_id, neighbor])
            if edge_type and edge_data.get("relation") != edge_type:
                continue
            node_data = dict(self.graph.nodes[neighbor])
            node_data["id"] = neighbor
            node_data["relation"] = edge_data.get("relation", "")
            results.append(node_data)
        return results

    async def shortest_path(self, source: str, target: str) -> List[str]:
        try:
            return nx.shortest_path(self.graph, source, target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    async def traverse(self, start: str, method: str = "bfs", max_depth: int = 5) -> List[Dict]:
        if not self.graph.has_node(start):
            return []
        visited = set()
        queue = [(start, 0)]
        results = []
        while queue:
            node, depth = queue.pop(0) if method == "bfs" else queue.pop()
            if node in visited or depth > max_depth:
                continue
            visited.add(node)
            data = dict(self.graph.nodes[node])
            data["id"] = node
            data["depth"] = depth
            results.append(data)
            neighbors = list(self.graph.neighbors(node))
            if method == "dfs":
                for n in reversed(neighbors):
                    queue.append((n, depth + 1))
            else:
                for n in neighbors:
                    queue.append((n, depth + 1))
        return results

    async def get_nodes(self, node_type: str = None) -> List[Dict]:
        results = []
        for node_id, data in self.graph.nodes(data=True):
            if node_type and data.get("type") != node_type:
                continue
            d = dict(data)
            d["id"] = node_id
            results.append(d)
        return results

    async def get_edges(self) -> List[Dict]:
        return [{"source": u, "target": v, **dict(d)} for u, v, d in self.graph.edges(data=True)]

    async def remove_node(self, node_id: str) -> bool:
        if self.graph.has_node(node_id):
            self.graph.remove_node(node_id)
            return True
        return False

    async def remove_edge(self, source: str, target: str) -> bool:
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
            return True
        return False

    async def stats(self) -> Dict:
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "components": nx.number_connected_components(self.graph) if self.graph.number_of_nodes() > 0 else 0,
            "density": round(nx.density(self.graph), 4) if self.graph.number_of_nodes() > 1 else 0,
        }

    async def clear(self):
        self.graph.clear()
