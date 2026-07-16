from typing import Dict, Any, List, Optional
from app.graph.network import GraphManager
import structlog

logger = structlog.get_logger()


class RelationshipManager:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def add_edge(self, source: str, target: str, edge_type: str, **attrs) -> Dict[str, Any]:
        self.graph.add_edge(source, target, edge_type=edge_type, **attrs)
        return {"source": source, "target": target, "type": edge_type, **attrs}

    def get_edges(self) -> List[Dict]:
        return [
            {"source": u, "target": v, **data}
            for u, v, data in self.graph.graph.edges(data=True)
        ]

    def get_node_edges(self, node_id: str) -> List[Dict]:
        edges = []
        for neighbor in self.graph.graph.neighbors(node_id):
            edge_data = self.graph.graph.edges[node_id, neighbor]
            edges.append({
                "source": node_id,
                "target": neighbor,
                "type": edge_data.get("type", "unknown"),
                **{k: v for k, v in edge_data.items() if k != "type"},
            })
        return edges

    def delete_edge(self, source: str, target: str) -> bool:
        if self.graph.graph.has_edge(source, target):
            self.graph.graph.remove_edge(source, target)
            return True
        return False

    def get_edges_by_type(self, edge_type: str) -> List[Dict]:
        return [
            {"source": u, "target": v, **data}
            for u, v, data in self.graph.graph.edges(data=True)
            if data.get("type") == edge_type
        ]
