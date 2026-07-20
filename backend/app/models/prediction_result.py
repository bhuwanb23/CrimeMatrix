from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, nullable=False, index=True)
    metric_name = Column(String(100))
    expected_value = Column(Float)
    actual_value = Column(Float)
    error = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
