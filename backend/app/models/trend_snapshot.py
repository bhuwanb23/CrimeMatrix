from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.db.base import Base


class TrendSnapshot(Base):
    __tablename__ = "trend_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(DateTime(timezone=True), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    comparison_value = Column(Float)
    change_pct = Column(Float)
    direction = Column(String(20))
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
