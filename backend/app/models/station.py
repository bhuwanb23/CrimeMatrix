from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    district_id = Column(Integer)
    address = Column(String(200))
    phone = Column(String(20))
    type = Column(String(50), default="police_station")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
