from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class RiskScoreHistory(Base):
    __tablename__ = "risk_score_history"

    id = Column(Integer, primary_key=True, index=True)
    suspect_id = Column(Integer, nullable=False, index=True)
    score = Column(Float)
    risk_level = Column(String(20))
    scored_at = Column(DateTime(timezone=True), server_default=func.now())
    change_from_previous = Column(Float)
