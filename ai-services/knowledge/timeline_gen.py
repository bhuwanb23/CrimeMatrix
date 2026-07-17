import networkx as nx
from typing import Dict, List
from datetime import datetime
import structlog

logger = structlog.get_logger()


class TimelineGenerator:
    def __init__(self, graph: nx.Graph = None):
        self.graph = graph or nx.Graph()

    def generate(self, node_id: str = None) -> List[Dict]:
        events = []
        nodes_to_check = [node_id] if node_id else list(self.graph.nodes())

        for nid in nodes_to_check:
            if not self.graph.has_node(nid):
                continue
            data = dict(self.graph.nodes[nid])
            date = data.get("created_at") or data.get("date") or data.get("occurred_at", "")
            if date:
                events.append({
                    "node_id": nid,
                    "type": data.get("type", "unknown"),
                    "name": data.get("name", nid),
                    "date": str(date)[:19],
                    "connections": self.graph.degree(nid),
                })

        for u, v, data in self.graph.edges(data=True):
            edge_data = dict(data)
            date = edge_data.get("date", "")
            if date:
                events.append({
                    "node_id": f"{u}->{v}",
                    "type": "relationship",
                    "name": f"{u} → {v}",
                    "date": str(date)[:19],
                    "relation": edge_data.get("relation", ""),
                })

        events.sort(key=lambda x: x.get("date", ""))
        return events

    def activity_bursts(self) -> List[Dict]:
        events = self.generate()
        if not events:
            return []

        date_counts = {}
        for e in events:
            d = e.get("date", "")[:10]
            if d:
                date_counts[d] = date_counts.get(d, 0) + 1

        avg = sum(date_counts.values()) / len(date_counts) if date_counts else 0
        bursts = [
            {"date": d, "count": c, "above_average": c > avg * 1.5}
            for d, c in date_counts.items()
            if c > avg * 1.5
        ]
        bursts.sort(key=lambda x: x["count"], reverse=True)
        return bursts

    def entity_timeline(self, node_id: str) -> List[Dict]:
        if not self.graph.has_node(node_id):
            return []

        events = []
        data = dict(self.graph.nodes[node_id])
        date = data.get("created_at") or data.get("date", "")
        if date:
            events.append({
                "node_id": node_id,
                "type": data.get("type", "unknown"),
                "name": data.get("name", node_id),
                "date": str(date)[:19],
                "event": "created",
            })

        for neighbor in self.graph.neighbors(node_id):
            edge_data = dict(self.graph.edges[node_id, neighbor])
            neighbor_data = dict(self.graph.nodes[neighbor])
            events.append({
                "node_id": neighbor,
                "type": neighbor_data.get("type", "unknown"),
                "name": neighbor_data.get("name", neighbor),
                "date": edge_data.get("date", ""),
                "event": edge_data.get("relation", "connected"),
            })

        events.sort(key=lambda x: x.get("date", ""))
        return events
