from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CrimeStatistic(Base):
    __tablename__ = "crime_statistics"

    id = Column(Integer, primary_key=True, index=True)
    period_type = Column(String(20), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True))
    total_crimes = Column(Integer, default=0)
    open_crimes = Column(Integer, default=0)
    closed_crimes = Column(Integer, default=0)
    resolution_rate = Column(Float, default=0)
    district_id = Column(Integer)
    crime_type_id = Column(Integer)
    station_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
