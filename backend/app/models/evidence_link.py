from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class EvidenceLink(Base):
    __tablename__ = "evidence_links"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id_1 = Column(Integer)
    evidence_id_2 = Column(Integer)
    link_type = Column(String(50), nullable=False)
    confidence = Column(Float, default=0)
    link_reason = Column(Text)
    status = Column(String(20), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
