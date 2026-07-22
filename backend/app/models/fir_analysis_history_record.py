from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class FIRAnalysisHistoryRecord(Base):
    __tablename__ = "fir_analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    fir_id = Column(Integer, nullable=False, index=True)
    analysis_type = Column(String(50))
    analysis_result = Column(Text)
    model_used = Column(String(100))
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
