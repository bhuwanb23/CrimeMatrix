from typing import List, Dict
from app.graph.network import GraphManager
import networkx as nx
import structlog

logger = structlog.get_logger()


class ComponentAnalyzer:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def get_connected_components(self) -> List[List[str]]:
        try:
            return [list(c) for c in nx.connected_components(self.graph.graph)]
        except Exception:
            return []

    def get_largest_component(self) -> List[str]:
        components = self.get_connected_components()
        if not components:
            return []
        return max(components, key=len)

    def get_component_count(self) -> int:
        return nx.number_connected_components(self.graph.graph)

    def get_component_size(self, node_id: str) -> int:
        try:
            component = nx.node_connected_component(self.graph.graph, node_id)
            return len(component)
        except Exception:
            return 0

    def get_component_stats(self) -> Dict:
        components = self.get_connected_components()
        sizes = [len(c) for c in components]
        return {
            "total_components": len(components),
            "largest_component": max(sizes) if sizes else 0,
            "smallest_component": min(sizes) if sizes else 0,
            "avg_component_size": round(sum(sizes) / len(sizes), 1) if sizes else 0,
            "isolated_nodes": sizes.count(1),
        }
