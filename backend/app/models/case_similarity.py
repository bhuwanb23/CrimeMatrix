from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.db.base import Base


class CaseSimilarity(Base):
    __tablename__ = "case_similarity"

    id = Column(Integer, primary_key=True, index=True)
    case_id_1 = Column(Integer, nullable=False, index=True)
    case_id_2 = Column(Integer, nullable=False, index=True)
    overall_score = Column(Float, nullable=False)
    mo_score = Column(Float, default=0)
    location_score = Column(Float, default=0)
    time_score = Column(Float, default=0)
    suspects_score = Column(Float, default=0)
    evidence_score = Column(Float, default=0)
    vehicles_score = Column(Float, default=0)
    reasons_json = Column(Text)
    status = Column(String(20), default="active")
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
