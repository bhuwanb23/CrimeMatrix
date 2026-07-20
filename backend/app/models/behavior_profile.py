from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class BehaviorProfile(Base):
    __tablename__ = "behavior_profiles"

    id = Column(Integer, primary_key=True, index=True)
    criminal_id = Column(Integer, index=True)
    profile_type = Column(String(50), nullable=False)
    pattern_description = Column(Text)
    confidence = Column(Float, default=0)
    frequency = Column(Integer, default=0)
    features_json = Column(Text)
    risk_level = Column(String(20), default="low")
    risk_score = Column(Float, default=0)
    last_analyzed = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
