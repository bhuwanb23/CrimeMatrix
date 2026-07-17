from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class GraphNode(Base):
    __tablename__ = "graph_nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), unique=True, nullable=False, index=True)
    node_type = Column(String(50), nullable=False)
    properties = Column(Text)
    confidence = Column(Float, default=1.0)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GraphEdge(Base):
    __tablename__ = "graph_edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(50), nullable=False, index=True)
    target_id = Column(String(50), nullable=False, index=True)
    relation = Column(String(50), nullable=False)
    properties = Column(Text)
    weight = Column(Float, default=1.0)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GraphVersion(Base):
    __tablename__ = "graph_versions"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    node_count = Column(Integer, default=0)
    edge_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
