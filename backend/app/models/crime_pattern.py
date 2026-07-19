from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CrimePattern(Base):
    __tablename__ = "crime_patterns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    pattern_type = Column(String(50), nullable=False)
    crime_type = Column(String(100))
    confidence = Column(Float, default=0)
    frequency = Column(Integer, default=0)
    time_pattern = Column(String(100))
    location_pattern = Column(String(100))
    mo_summary = Column(Text)
    first_seen = Column(DateTime(timezone=True))
    last_seen = Column(DateTime(timezone=True))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
