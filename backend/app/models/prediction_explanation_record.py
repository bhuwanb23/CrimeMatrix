from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class PredictionExplanationRecord(Base):
    __tablename__ = "prediction_explanations"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, nullable=False, index=True)
    explanation_type = Column(String(50))
    contributing_factors = Column(Text)
    confidence_breakdown = Column(Text)
    model_explanation = Column(Text)
    evidence_links = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
