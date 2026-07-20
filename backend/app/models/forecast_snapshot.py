from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class ForecastSnapshot(Base):
    __tablename__ = "forecast_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(DateTime(timezone=True), server_default=func.now())
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float)
    forecast_value = Column(Float)
    confidence = Column(Float)
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
