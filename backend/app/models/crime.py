from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    crime_type_id = Column(Integer)
    district_id = Column(Integer)
    location_id = Column(Integer)
    status = Column(String(20), default="open")
    priority = Column(String(20), default="medium")
    reported_by = Column(Integer)
    occurred_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
