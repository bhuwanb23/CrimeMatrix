from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class Criminal(Base):
    __tablename__ = "criminals"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer)
    alias = Column(String(100))
    risk_score = Column(Float, default=0.0)
    status = Column(String(20), default="at_large")
    mo_description = Column(Text)
    behavioral_profile = Column(Text)
    first_offense_date = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
