from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class LocationCluster(Base):
    __tablename__ = "location_clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    cluster_type = Column(String(50))
    center_lat = Column(Float)
    center_lng = Column(Float)
    radius_km = Column(Float)
    member_count = Column(Integer, default=0)
    avg_crime_count = Column(Float, default=0)
    cohesion_score = Column(Float, default=0)
    hotspot_ids = Column(Text)
    crime_type_ids = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
