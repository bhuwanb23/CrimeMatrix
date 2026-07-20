from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CasePriority(Base):
    __tablename__ = "case_priorities"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, nullable=False, index=True)
    overall_priority_score = Column(Float, default=0)
    severity_score = Column(Float, default=0)
    victim_vulnerability_score = Column(Float, default=0)
    evidence_availability_score = Column(Float, default=0)
    repeat_offender_score = Column(Float, default=0)
    active_threats_score = Column(Float, default=0)
    investigation_age_score = Column(Float, default=0)
    cross_district_score = Column(Float, default=0)
    officer_workload_score = Column(Float, default=0)
    priority_level = Column(String(20), default="low")
    explanation_json = Column(Text)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
