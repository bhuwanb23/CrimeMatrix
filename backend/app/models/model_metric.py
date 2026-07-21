from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class ModelMetric(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float)
    measurement_date = Column(DateTime(timezone=True), server_default=func.now())
    period_type = Column(String(20))
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
