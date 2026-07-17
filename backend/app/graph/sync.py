import json
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.graph.persistence import GraphPersistence
import structlog

logger = structlog.get_logger()


class GraphSync:
    def __init__(self, db: AsyncSession):
        self.persistence = GraphPersistence(db)

    async def add_node(self, graph, node_id: str, node_type: str, **attrs):
        graph.add_node(node_id, type=node_type, **attrs)
        await self.persistence.save_node(node_id, node_type, attrs)
        logger.info("graph_sync_node_added", node_id=node_id)

    async def add_edge(self, graph, source: str, target: str, relation: str = "", **attrs):
        graph.add_edge(source, target, relation=relation, **attrs)
        await self.persistence.save_edge(source, target, relation, attrs)
        logger.info("graph_sync_edge_added", source=source, target=target)

    async def remove_node(self, graph, node_id: str) -> bool:
        if graph.has_node(node_id):
            graph.remove_node(node_id)
            await self.persistence.delete_node(node_id)
            return True
        return False

    async def remove_edge(self, graph, source: str, target: str) -> bool:
        if graph.has_edge(source, target):
            graph.remove_edge(source, target)
            await self.persistence.delete_edge(source, target)
            return True
        return False
