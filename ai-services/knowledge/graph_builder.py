import networkx as nx
from typing import Dict, List, Optional
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class GraphBuilder:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL
        self.graph = nx.Graph()

    async def build(self) -> Dict:
        stats = {"nodes": 0, "edges": 0}

        suspects = await self._load_entities("/api/v1/criminals/")
        for s in suspects:
            self.graph.add_node(f"person_{s.get('id')}", type="person", **{k: v for k, v in s.items() if k != "id"})
            stats["nodes"] += 1

        crimes = await self._load_entities("/api/v1/crimes/")
        for c in crimes:
            self.graph.add_node(f"crime_{c.get('id')}", type="crime", **{k: v for k, v in c.items() if k != "id"})
            stats["nodes"] += 1

        officers = await self._load_entities("/api/v1/officers/")
        for o in officers:
            self.graph.add_node(f"officer_{o.get('id')}", type="officer", **{k: v for k, v in o.items() if k != "id"})
            stats["nodes"] += 1

        vehicles = await self._load_entities("/api/v1/vehicles/")
        for v in vehicles:
            self.graph.add_node(f"vehicle_{v.get('id')}", type="vehicle", **{k: v for k, v in v.items() if k != "id"})
            stats["nodes"] += 1

        for c in crimes:
            crime_id = c.get("id")
            reported_by = c.get("reported_by")
            if reported_by:
                person_node = f"person_{reported_by}"
                if self.graph.has_node(person_node):
                    self.graph.add_edge(person_node, f"crime_{crime_id}", relation="involved_in")
                    stats["edges"] += 1

        logger.info("graph_built", nodes=stats["nodes"], edges=stats["edges"])
        return stats

    async def _load_entities(self, path: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}{path}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    if isinstance(data, dict):
                        return data.get("items", data.get("data", []))
                    if isinstance(data, list):
                        return data
        except Exception as e:
            logger.warning("load_entities_error", path=path, error=str(e))
        return []

    def add_manual_edge(self, source: str, target: str, relation: str):
        self.graph.add_edge(source, target, relation=relation)

    def get_stats(self) -> dict:
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "components": nx.number_connected_components(self.graph) if self.graph.number_of_nodes() > 0 else 0,
            "density": round(nx.density(self.graph), 4) if self.graph.number_of_nodes() > 1 else 0,
        }
