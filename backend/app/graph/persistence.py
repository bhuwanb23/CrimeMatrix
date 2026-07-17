import json
from datetime import datetime
import networkx as nx
from typing import Dict, List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.graph_meta import GraphNode, GraphEdge, GraphVersion
import structlog

logger = structlog.get_logger()


class GraphPersistence:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_node(self, node_id: str, node_type: str, properties: dict = None,
                         confidence: float = 1.0):
        existing = (await self.db.execute(
            select(GraphNode).where(GraphNode.node_id == node_id)
        )).scalar_one_or_none()

        if existing:
            existing.node_type = node_type
            existing.properties = json.dumps(properties or {})
            existing.confidence = confidence
            existing.version = existing.version + 1
        else:
            node = GraphNode(
                node_id=node_id,
                node_type=node_type,
                properties=json.dumps(properties or {}),
                confidence=confidence,
                version=1,
            )
            self.db.add(node)
        await self.db.commit()

    async def save_edge(self, source_id: str, target_id: str, relation: str,
                         properties: dict = None, weight: float = 1.0):
        existing = (await self.db.execute(
            select(GraphEdge).where(
                GraphEdge.source_id == source_id,
                GraphEdge.target_id == target_id,
                GraphEdge.relation == relation,
            )
        )).scalar_one_or_none()

        if existing:
            existing.properties = json.dumps(properties or {})
            existing.weight = weight
            existing.version = existing.version + 1
        else:
            edge = GraphEdge(
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                properties=json.dumps(properties or {}),
                weight=weight,
                version=1,
            )
            self.db.add(edge)
        await self.db.commit()

    async def delete_node(self, node_id: str) -> bool:
        node = (await self.db.execute(
            select(GraphNode).where(GraphNode.node_id == node_id)
        )).scalar_one_or_none()
        if node:
            await self.db.delete(node)
            await self.db.execute(
                delete(GraphEdge).where(
                    (GraphEdge.source_id == node_id) | (GraphEdge.target_id == node_id)
                )
            )
            await self.db.commit()
            return True
        return False

    async def delete_edge(self, source_id: str, target_id: str) -> bool:
        result = await self.db.execute(
            delete(GraphEdge).where(
                GraphEdge.source_id == source_id,
                GraphEdge.target_id == target_id,
            )
        )
        await self.db.commit()
        return result.rowcount > 0

    async def load_all_nodes(self) -> List[Dict]:
        result = await self.db.execute(select(GraphNode))
        return [
            {
                "node_id": n.node_id,
                "node_type": n.node_type,
                "properties": json.loads(n.properties) if n.properties else {},
                "confidence": n.confidence,
                "version": n.version,
                "created_at": str(n.created_at) if n.created_at else None,
            }
            for n in result.scalars().all()
        ]

    async def load_all_edges(self) -> List[Dict]:
        result = await self.db.execute(select(GraphEdge))
        return [
            {
                "source_id": e.source_id,
                "target_id": e.target_id,
                "relation": e.relation,
                "properties": json.loads(e.properties) if e.properties else {},
                "weight": e.weight,
                "version": e.version,
                "created_at": str(e.created_at) if e.created_at else None,
            }
            for e in result.scalars().all()
        ]

    async def save_version(self, node_count: int, edge_count: int):
        version = GraphVersion(
            version=await self._get_next_version(),
            node_count=node_count,
            edge_count=edge_count,
        )
        self.db.add(version)
        await self.db.commit()

    async def get_latest_version(self) -> Optional[Dict]:
        result = await self.db.execute(
            select(GraphVersion).order_by(GraphVersion.version.desc()).limit(1)
        )
        v = result.scalar_one_or_none()
        if v:
            return {
                "version": v.version, "node_count": v.node_count,
                "edge_count": v.edge_count, "created_at": str(v.created_at),
            }
        return None

    async def get_version_history(self) -> List[Dict]:
        result = await self.db.execute(
            select(GraphVersion).order_by(GraphVersion.version.desc())
        )
        return [
            {"version": v.version, "node_count": v.node_count, "edge_count": v.edge_count}
            for v in result.scalars().all()
        ]

    async def _get_next_version(self) -> int:
        result = await self.db.execute(
            select(GraphVersion.version).order_by(GraphVersion.version.desc()).limit(1)
        )
        v = result.scalar_one_or_none()
        return (v or 0) + 1

    async def clear(self):
        await self.db.execute(delete(GraphEdge))
        await self.db.execute(delete(GraphNode))
        await self.db.commit()

    async def get_stats(self) -> Dict:
        node_count = (await self.db.execute(select(GraphNode))).scalars().count()
        edge_count = (await self.db.execute(select(GraphEdge))).scalars().count()
        version = await self.get_latest_version()
        return {
            "total_nodes": node_count,
            "total_edges": edge_count,
            "current_version": version.get("version") if version else 0,
        }
