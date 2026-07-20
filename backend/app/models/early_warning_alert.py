from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class EarlyWarningAlert(Base):
    __tablename__ = "early_warning_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default="medium")
    district_id = Column(Integer)
    crime_type_id = Column(Integer)
    case_id = Column(Integer)
    detected_value = Column(Float)
    threshold = Column(Float)
    confidence = Column(Float, default=0)
    status = Column(String(20), default="active")
    acknowledged_by = Column(String(100))
    acknowledged_at = Column(DateTime(timezone=True))
    evidence_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
