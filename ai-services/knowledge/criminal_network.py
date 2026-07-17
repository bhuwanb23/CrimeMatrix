import networkx as nx
from typing import Dict, List
from collections import Counter
import structlog

logger = structlog.get_logger()


class CriminalNetwork:
    def __init__(self, graph: nx.Graph = None):
        self.graph = graph or nx.Graph()

    def find_clusters(self) -> List[Dict]:
        if self.graph.number_of_nodes() == 0:
            return []
        clusters = []
        for component in nx.connected_components(self.graph):
            subgraph = self.graph.subgraph(component)
            key_players = self._find_key_players(subgraph)
            clusters.append({
                "size": len(component),
                "nodes": list(component),
                "key_players": key_players,
                "density": round(nx.density(subgraph), 4) if len(component) > 1 else 0,
            })
        clusters.sort(key=lambda x: x["size"], reverse=True)
        return clusters

    def _find_key_players(self, subgraph: nx.Graph) -> List[Dict]:
        if subgraph.number_of_nodes() == 0:
            return []
        centrality = nx.degree_centrality(subgraph)
        ranked = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        return [
            {"node_id": n, "centrality": round(c, 4), **dict(subgraph.nodes[n])}
            for n, c in ranked
        ]

    def network_risk_score(self, node_id: str) -> Dict:
        if not self.graph.has_node(node_id):
            return {"risk": 0, "factors": []}

        degree = self.graph.degree(node_id)
        centrality = nx.degree_centrality(self.graph).get(node_id, 0)
        neighbors = list(self.graph.neighbors(node_id))

        criminal_neighbors = sum(1 for n in neighbors if self.graph.nodes[n].get("type") == "person")
        crime_neighbors = sum(1 for n in neighbors if self.graph.nodes[n].get("type") == "crime")

        risk = min(100, int(degree * 10 + centrality * 50 + criminal_neighbors * 5 + crime_neighbors * 3))
        factors = []
        if degree > 5:
            factors.append(f"high connectivity ({degree} connections)")
        if centrality > 0.3:
            factors.append(f"high centrality ({centrality:.2f})")
        if criminal_neighbors > 3:
            factors.append(f"many criminal links ({criminal_neighbors})")

        return {"risk": risk, "factors": factors, "degree": degree, "centrality": round(centrality, 4)}

    def accomplice_network(self, node_id: str, depth: int = 2) -> Dict:
        if not self.graph.has_node(node_id):
            return {"nodes": [], "edges": []}

        visited = set()
        queue = [(node_id, 0)]
        result_nodes = []
        result_edges = []

        while queue:
            current, d = queue.pop(0)
            if current in visited or d > depth:
                continue
            visited.add(current)
            result_nodes.append({"node_id": current, **dict(self.graph.nodes[current])})

            for neighbor in self.graph.neighbors(current):
                edge_data = dict(self.graph.edges[current, neighbor])
                result_edges.append({"source": current, "target": neighbor, **edge_data})
                if neighbor not in visited:
                    queue.append((neighbor, d + 1))

        return {"nodes": result_nodes, "edges": result_edges}
