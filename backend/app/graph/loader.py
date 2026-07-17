import networkx as nx
import json
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.graph.persistence import GraphPersistence
import structlog

logger = structlog.get_logger()


class GraphLoader:
    def __init__(self, db: AsyncSession):
        self.persistence = GraphPersistence(db)
        self.graph = nx.Graph()

    async def load(self) -> Dict:
        nodes = await self.persistence.load_all_nodes()
        edges = await self.persistence.load_all_edges()

        self.graph.clear()

        for node in nodes:
            attrs = dict(node["properties"])
            attrs["type"] = node["node_type"]
            attrs["confidence"] = node.get("confidence", 1.0)
            attrs["version"] = node.get("version", 1)
            self.graph.add_node(node["node_id"], **attrs)

        for edge in edges:
            if self.graph.has_node(edge["source_id"]) and self.graph.has_node(edge["target_id"]):
                attrs = dict(edge["properties"])
                attrs["relation"] = edge["relation"]
                attrs["weight"] = edge.get("weight", 1.0)
                attrs["version"] = edge.get("version", 1)
                self.graph.add_edge(edge["source_id"], edge["target_id"], **attrs)

        stats = {
            "nodes_loaded": self.graph.number_of_nodes(),
            "edges_loaded": self.graph.number_of_edges(),
        }
        logger.info("graph_loaded", **stats)
        return stats

    async def save(self):
        persistence = self.persistence
        await persistence.clear()

        for node_id, data in self.graph.nodes(data=True):
            node_type = data.get("type", "unknown")
            confidence = data.get("confidence", 1.0)
            properties = {k: v for k, v in data.items() if k not in ("type", "confidence", "version")}
            await persistence.save_node(node_id, node_type, properties, confidence)

        for source, target, data in self.graph.edges(data=True):
            relation = data.get("relation", "")
            weight = data.get("weight", 1.0)
            properties = {k: v for k, v in data.items() if k not in ("relation", "weight", "version")}
            await persistence.save_edge(source, target, relation, properties, weight)

        await persistence.save_version(self.graph.number_of_nodes(), self.graph.number_of_edges())
        stats = {"nodes_saved": self.graph.number_of_nodes(), "edges_saved": self.graph.number_of_edges()}
        logger.info("graph_saved", **stats)
        return stats
