from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class RepeatOffender(Base):
    __tablename__ = "repeat_offenders"

    id = Column(Integer, primary_key=True, index=True)
    criminal_id = Column(Integer, index=True)
    suspect_id = Column(Integer, index=True)
    offender_name = Column(String(200), nullable=False)
    total_offenses = Column(Integer, default=0)
    frequency_score = Column(Float, default=0)
    recency_score = Column(Float, default=0)
    severity_score = Column(Float, default=0)
    geographic_score = Column(Float, default=0)
    overall_score = Column(Float, default=0)
    risk_level = Column(String(20), default="low")
    risk_factors = Column(Text)
    first_offense_date = Column(String(10))
    last_offense_date = Column(String(10))
    districts_active = Column(Text)
    crime_types = Column(Text)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
