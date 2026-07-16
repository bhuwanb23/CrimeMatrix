from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300))
    latitude = Column(Float)
    longitude = Column(Float)
    district_id = Column(Integer)
    type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
