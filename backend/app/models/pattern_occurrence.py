from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PatternOccurrence(Base):
    __tablename__ = "pattern_occurrences"

    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, nullable=False, index=True)
    crime_id = Column(Integer, nullable=False, index=True)
    similarity_score = Column(Float, default=0)
    matched_at = Column(DateTime(timezone=True), server_default=func.now())
