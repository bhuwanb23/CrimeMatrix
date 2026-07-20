from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PriorityHistoryRecord(Base):
    __tablename__ = "priority_history"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, nullable=False, index=True)
    priority_score = Column(Float)
    priority_level = Column(String(20))
    scored_at = Column(DateTime(timezone=True), server_default=func.now())
    change_from_previous = Column(Float)
