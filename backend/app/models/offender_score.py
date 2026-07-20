from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class OffenderScore(Base):
    __tablename__ = "offender_scores"

    id = Column(Integer, primary_key=True, index=True)
    offender_id = Column(Integer, nullable=False, index=True)
    dimension = Column(String(50), nullable=False)
    score = Column(Float, default=0)
    details = Column(Text)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
