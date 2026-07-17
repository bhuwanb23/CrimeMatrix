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
            self.graph.add_node(node["node_id"], type=node["node_type"], **node["properties"])

        for edge in edges:
            if self.graph.has_node(edge["source_id"]) and self.graph.has_node(edge["target_id"]):
                self.graph.add_edge(edge["source_id"], edge["target_id"], relation=edge["relation"], **edge["properties"])

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
            properties = {k: v for k, v in data.items() if k != "type"}
            await persistence.save_node(node_id, node_type, properties)

        for source, target, data in self.graph.edges(data=True):
            relation = data.get("relation", "")
            properties = {k: v for k, v in data.items() if k != "relation"}
            await persistence.save_edge(source, target, relation, properties)

        await persistence.save_version(self.graph.number_of_nodes(), self.graph.number_of_edges())
        stats = {"nodes_saved": self.graph.number_of_nodes(), "edges_saved": self.graph.number_of_edges()}
        logger.info("graph_saved", **stats)
        return stats
