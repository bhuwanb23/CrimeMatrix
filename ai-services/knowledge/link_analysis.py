import networkx as nx
from typing import Dict, List
import structlog

logger = structlog.get_logger()


class LinkAnalysis:
    def __init__(self, graph: nx.Graph = None):
        self.graph = graph or nx.Graph()

    def shortest_path(self, source: str, target: str) -> Dict:
        try:
            path = nx.shortest_path(self.graph, source, target)
            path_details = []
            for i, node_id in enumerate(path):
                node_data = dict(self.graph.nodes[node_id])
                step = {"node_id": node_id, "type": node_data.get("type", "unknown"), "name": node_data.get("name", node_id)}
                if i < len(path) - 1:
                    edge_data = dict(self.graph.edges[node_id, path[i + 1]])
                    step["relation"] = edge_data.get("relation", "unknown")
                path_details.append(step)
            return {"path": path, "length": len(path) - 1, "details": path_details}
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return {"path": [], "length": -1, "details": []}

    def centrality(self) -> List[Dict]:
        if self.graph.number_of_nodes() == 0:
            return []
        degree_cent = nx.degree_centrality(self.graph)
        try:
            between_cent = nx.betweenness_centrality(self.graph)
        except Exception:
            between_cent = {n: 0 for n in self.graph.nodes()}
        try:
            close_cent = nx.closeness_centrality(self.graph)
        except Exception:
            close_cent = {n: 0 for n in self.graph.nodes()}

        results = []
        for node_id in self.graph.nodes():
            data = dict(self.graph.nodes[node_id])
            combined = (degree_cent.get(node_id, 0) * 40 +
                       between_cent.get(node_id, 0) * 40 +
                       close_cent.get(node_id, 0) * 20)
            results.append({
                "node_id": node_id,
                "type": data.get("type", "unknown"),
                "name": data.get("name", node_id),
                "degree_centrality": round(degree_cent.get(node_id, 0), 4),
                "betweenness_centrality": round(between_cent.get(node_id, 0), 4),
                "closeness_centrality": round(close_cent.get(node_id, 0), 4),
                "importance_score": round(combined, 2),
            })
        results.sort(key=lambda x: x["importance_score"], reverse=True)
        return results

    def communities(self) -> List[List[str]]:
        try:
            return [list(c) for c in nx.community.greedy_modularity_communities(self.graph)]
        except Exception:
            return [list(self.graph.nodes())]

    def bridges(self) -> List[Dict]:
        try:
            bridge_edges = list(nx.bridges(self.graph))
            return [{"source": u, "target": v} for u, v in bridge_edges]
        except Exception:
            return []

    def isolated_nodes(self) -> List[str]:
        return [n for n in self.graph.nodes() if self.graph.degree(n) == 0]
