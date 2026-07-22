from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class EvidenceRelationship(Base):
    __tablename__ = "evidence_relationships"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer)
    case_id_1 = Column(Integer)
    case_id_2 = Column(Integer)
    relationship_type = Column(String(50))
    strength = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
