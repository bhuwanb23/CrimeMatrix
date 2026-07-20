from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class BehaviorFeature(Base):
    __tablename__ = "behavior_features"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, nullable=False, index=True)
    feature_name = Column(String(100), nullable=False)
    feature_value = Column(String(200))
    weight = Column(Float, default=0)
    source_crime_ids = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
