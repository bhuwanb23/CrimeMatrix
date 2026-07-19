from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PatternCluster(Base):
    __tablename__ = "pattern_clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    pattern_ids = Column(Text)
    cluster_type = Column(String(50))
    strength = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
