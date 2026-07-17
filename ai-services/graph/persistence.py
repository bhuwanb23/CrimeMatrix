import httpx
import json
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class GraphPersistenceClient:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    async def save_node(self, node_id: str, node_type: str, properties: dict = None,
                         confidence: float = 1.0) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                data = {"node_id": node_id, "node_type": node_type,
                        "properties": properties or {}, "confidence": confidence}
                resp = await client.post(f"{self.backend_url}/api/v1/graph/nodes", json=data, timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("save_node_error", error=str(e))
        return False

    async def save_edge(self, source: str, target: str, relation: str,
                         properties: dict = None, weight: float = 1.0) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                data = {"source": source, "target": target, "relation": relation,
                        "properties": properties or {}, "weight": weight}
                resp = await client.post(f"{self.backend_url}/api/v1/graph/edges", json=data, timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("save_edge_error", error=str(e))
        return False

    async def load_all(self) -> Dict:
        try:
            async with httpx.AsyncClient() as client:
                nodes_resp = await client.get(f"{self.backend_url}/api/v1/graph/nodes", timeout=10.0)
                edges_resp = await client.get(f"{self.backend_url}/api/v1/graph/edges", timeout=10.0)
                nodes = nodes_resp.json().get("data", []) if nodes_resp.status_code == 200 else []
                edges = edges_resp.json().get("data", []) if edges_resp.status_code == 200 else []
                return {"nodes": nodes, "edges": edges}
        except Exception as e:
            logger.warning("load_all_error", error=str(e))
        return {"nodes": [], "edges": []}

    async def save_all(self, graph_data: Dict) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.backend_url}/api/v1/graph/save-all",
                                          json=graph_data, timeout=30.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("save_all_error", error=str(e))
        return False

    async def get_stats(self) -> Dict:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/graph/stats", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {})
        except Exception as e:
            logger.warning("get_stats_error", error=str(e))
        return {}
