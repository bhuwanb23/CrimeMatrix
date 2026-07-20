from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PriorityExplanation(Base):
    __tablename__ = "priority_explanations"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, nullable=False, index=True)
    factor_name = Column(String(100), nullable=False)
    factor_score = Column(Float)
    weight = Column(Float)
    explanation = Column(Text)
    evidence_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
