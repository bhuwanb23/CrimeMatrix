import networkx as nx
from typing import Dict, List
import structlog

logger = structlog.get_logger()


class RelationshipDiscovery:
    def __init__(self, graph: nx.Graph = None):
        self.graph = graph or nx.Graph()

    def find_hidden_connections(self, node1: str, node2: str) -> List[Dict]:
        paths = []
        try:
            for path in nx.all_simple_paths(self.graph, node1, node2, cutoff=5):
                path_details = []
                for i in range(len(path) - 1):
                    edge_data = dict(self.graph.edges[path[i], path[i + 1]])
                    node_data = dict(self.graph.nodes[path[i + 1]])
                    path_details.append({
                        "from": path[i],
                        "to": path[i + 1],
                        "relation": edge_data.get("relation", "unknown"),
                        "target_type": node_data.get("type", "unknown"),
                    })
                paths.append({"path": path, "length": len(path) - 1, "details": path_details})
        except (nx.NetworkXError, nx.NodeNotFound):
            pass
        paths.sort(key=lambda x: x["length"])
        return paths

    def shared_connections(self, node1: str, node2: str) -> List[Dict]:
        if not self.graph.has_node(node1) or not self.graph.has_node(node2):
            return []
        n1_neighbors = set(self.graph.neighbors(node1))
        n2_neighbors = set(self.graph.neighbors(node2))
        shared = n1_neighbors & n2_neighbors
        results = []
        for n in shared:
            data = dict(self.graph.nodes[n])
            results.append({"node_id": n, **data})
        return results

    def relationship_strength(self, node1: str, node2: str) -> Dict:
        if not self.graph.has_node(node1) or not self.graph.has_node(node2):
            return {"strength": 0, "paths": 0, "shared": 0}

        paths = list(nx.all_simple_paths(self.graph, node1, node2, cutoff=4))
        shared = self.shared_connections(node1, node2)
        direct = 1 if self.graph.has_edge(node1, node2) else 0

        strength = min(100, direct * 40 + len(shared) * 20 + max(0, 30 - len(paths) * 5))
        return {
            "strength": strength,
            "direct_connection": bool(direct),
            "paths": len(paths),
            "shared_connections": len(shared),
        }

    def node_importance(self, node_id: str) -> Dict:
        if not self.graph.has_node(node_id):
            return {"importance": 0}

        degree = self.graph.degree(node_id)
        centrality = nx.degree_centrality(self.graph).get(node_id, 0)
        try:
            betweenness = nx.betweenness_centrality(self.graph).get(node_id, 0)
        except Exception:
            betweenness = 0

        importance = min(100, int(degree * 8 + centrality * 40 + betweenness * 60))
        return {
            "importance": importance,
            "degree": degree,
            "centrality": round(centrality, 4),
            "betweenness": round(betweenness, 4),
        }
