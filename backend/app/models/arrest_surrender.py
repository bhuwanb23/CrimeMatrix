from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class ArrestSurrender(Base):
    __tablename__ = "arrest_surrender"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    type_id = Column(Integer, ForeignKey("arrest_surrender_types.id"), nullable=True)
    date = Column(DateTime, nullable=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    police_station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    io_id = Column(Integer, ForeignKey("officers.id"), nullable=True)
    court_id = Column(Integer, ForeignKey("courts.id"), nullable=True)
    accused_id = Column(Integer, ForeignKey("accused.id"), nullable=True)
    is_accused = Column(Boolean, default=False)
    is_complainant_accused = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
