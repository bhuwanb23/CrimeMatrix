from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Court(Base):
    __tablename__ = "courts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=True)
    district = Column(String(100), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    court_type = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
