from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    crime_type = Column(String(50), nullable=False)
    district = Column(String(100), nullable=False)
    status = Column(String(20), default="active")
    priority = Column(String(20), default="medium")
    officer_id = Column(Integer, ForeignKey("users.id"))
    fir_id = Column(Integer, ForeignKey("firs.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
