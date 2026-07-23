from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey("unit_types.id"), nullable=True)
    parent_unit = Column(Integer, nullable=True)
    nationality_id = Column(Integer, nullable=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    address = Column(String(200))
    phone = Column(String(20))
    type = Column(String(50), default="police_station")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
