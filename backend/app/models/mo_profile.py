from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class MOProfile(Base):
    __tablename__ = "mo_profiles"

    id = Column(Integer, primary_key=True, index=True)
    crime_id = Column(Integer, index=True)
    case_id = Column(Integer)
    entry_method = Column(String(100))
    exit_method = Column(String(100))
    timing_pattern = Column(String(100))
    weapon_type = Column(String(100))
    target_type = Column(String(100))
    location_pattern = Column(String(100))
    victim_profile = Column(String(100))
    escape_method = Column(String(100))
    mo_text = Column(Text)
    fingerprint_json = Column(Text)
    confidence = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
