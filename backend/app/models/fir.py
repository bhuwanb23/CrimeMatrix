from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class FIR(Base):
    __tablename__ = "firs"

    id = Column(Integer, primary_key=True, index=True)
    fir_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    crime_type = Column(String(50), nullable=False)
    district = Column(String(100), nullable=False)
    station = Column(String(100))
    status = Column(String(20), default="filed")
    complainant_name = Column(String(100))
    complainant_phone = Column(String(20))
    date_filed = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
