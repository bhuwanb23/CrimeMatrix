from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    badge_number = Column(String(20), unique=True, nullable=False)
    rank = Column(String(50))
    station_id = Column(Integer)
    specialization = Column(String(100))
    phone = Column(String(20))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
