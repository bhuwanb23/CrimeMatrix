from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class SuspectRiskScore(Base):
    __tablename__ = "suspect_risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    suspect_id = Column(Integer, nullable=False, index=True)
    overall_score = Column(Float, default=0)
    risk_level = Column(String(20), default="low")
    criminal_history_score = Column(Float, default=0)
    offense_severity_score = Column(Float, default=0)
    age_factor_score = Column(Float, default=0)
    location_risk_score = Column(Float, default=0)
    associate_risk_score = Column(Float, default=0)
    recency_score = Column(Float, default=0)
    network_influence_score = Column(Float, default=0)
    mo_similarity_score = Column(Float, default=0)
    investigation_links_score = Column(Float, default=0)
    behavioral_score = Column(Float, default=0)
    explanation_json = Column(Text)
    evidence_json = Column(Text)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
