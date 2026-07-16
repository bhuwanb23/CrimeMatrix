from typing import List, Dict
from app.graph.network import GraphManager
import structlog

logger = structlog.get_logger()


class TimelineAnalyzer:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def get_activity_timeline(self) -> List[Dict]:
        timeline = []
        for node_id, data in self.graph.graph.nodes(data=True):
            timeline.append({
                "node_id": node_id,
                "type": data.get("type", "unknown"),
                "name": data.get("name", node_id),
                "connections": self.graph.graph.degree(node_id),
            })
        timeline.sort(key=lambda x: x["connections"], reverse=True)
        return timeline

    def get_node_timeline(self, node_id: str) -> List[Dict]:
        timeline = []
        node_data = dict(self.graph.graph.nodes.get(node_id, {}))
        created = node_data.get("created_at") or node_data.get("date", "")
        if created:
            timeline.append({
                "node_id": node_id,
                "type": node_data.get("type", "unknown"),
                "name": node_data.get("name", node_id),
                "date": str(created),
            })

        for neighbor in self.graph.graph.neighbors(node_id):
            edge_data = self.graph.graph.edges[node_id, neighbor]
            neighbor_data = dict(self.graph.graph.nodes.get(neighbor, {}))
            timeline.append({
                "node_id": neighbor,
                "type": neighbor_data.get("type", "unknown"),
                "name": neighbor_data.get("name", neighbor),
                "relationship": edge_data.get("type", "unknown"),
                "date": neighbor_data.get("created_at", ""),
            })

        timeline.sort(key=lambda x: x.get("date", ""), reverse=True)
        return timeline

    def get_activity_bursts(self) -> List[Dict]:
        bursts = []
        for node_id, data in self.graph.graph.nodes(data=True):
            degree = self.graph.graph.degree(node_id)
            if degree >= 3:
                bursts.append({
                    "node_id": node_id,
                    "name": data.get("name", node_id),
                    "type": data.get("type", "unknown"),
                    "connections": degree,
                })
        bursts.sort(key=lambda x: x["connections"], reverse=True)
        return bursts
