from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PredictionSource(Base):
    __tablename__ = "prediction_sources"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, nullable=False, index=True)
    source_type = Column(String(50))
    source_id = Column(Integer)
    source_name = Column(String(200))
    relevance_score = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
