from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CrossDistrictMatch(Base):
    __tablename__ = "cross_district_matches"

    id = Column(Integer, primary_key=True, index=True)
    match_type = Column(String(50), nullable=False)
    entity_id_1 = Column(Integer)
    entity_type_1 = Column(String(50))
    district_1 = Column(String(100))
    entity_id_2 = Column(Integer)
    entity_type_2 = Column(String(50))
    district_2 = Column(String(100))
    confidence = Column(Float, default=0)
    match_reason = Column(Text)
    evidence_json = Column(Text)
    status = Column(String(20), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
