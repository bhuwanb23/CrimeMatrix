from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CrimeHotspot(Base):
    __tablename__ = "crime_hotspots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    hotspot_type = Column(String(50), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    radius_km = Column(Float)
    crime_count = Column(Integer, default=0)
    dominant_crime_type = Column(String(100))
    risk_level = Column(String(20), default="low")
    density_score = Column(Float, default=0)
    trend_direction = Column(String(20))
    trend_change_pct = Column(Float)
    district_id = Column(Integer)
    station_id = Column(Integer)
    first_detected = Column(DateTime(timezone=True))
    last_updated = Column(DateTime(timezone=True))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
