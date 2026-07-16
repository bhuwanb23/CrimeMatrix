from typing import Dict, Any, List, Optional
from app.graph.network import GraphManager
import structlog

logger = structlog.get_logger()


class NodeManager:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def add_node(self, node_id: str, node_type: str, **attrs) -> Dict[str, Any]:
        self.graph.add_node(node_id, node_type=node_type, **attrs)
        return {"id": node_id, "type": node_type, **attrs}

    def get_node(self, node_id: str) -> Optional[Dict]:
        if self.graph.graph.has_node(node_id):
            data = dict(self.graph.graph.nodes[node_id])
            data["id"] = node_id
            return data
        return None

    def get_all_nodes(self) -> List[Dict]:
        return [
            {"id": n, **dict(data)}
            for n, data in self.graph.graph.nodes(data=True)
        ]

    def update_node(self, node_id: str, **attrs) -> Optional[Dict]:
        if self.graph.graph.has_node(node_id):
            self.graph.graph.nodes[node_id].update(attrs)
            return self.get_node(node_id)
        return None

    def delete_node(self, node_id: str) -> bool:
        if self.graph.graph.has_node(node_id):
            self.graph.graph.remove_node(node_id)
            return True
        return False

    def search_nodes(self, query: str) -> List[Dict]:
        results = []
        for n, data in self.graph.graph.nodes(data=True):
            name = data.get("name", "").lower()
            if query.lower() in name or query.lower() in n.lower():
                results.append({"id": n, **data})
        return results
