from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class ChargesheetDetail(Base):
    __tablename__ = "chargesheet_details"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    cs_date = Column(DateTime, nullable=True)
    cs_type = Column(String(1), nullable=True)
    police_person_id = Column(Integer, ForeignKey("officers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
