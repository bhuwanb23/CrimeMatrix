from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class FIRSuggestion(Base):
    __tablename__ = "fir_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    fir_id = Column(Integer, nullable=False, index=True)
    suggestion_type = Column(String(50), nullable=False)
    suggestion_text = Column(Text)
    confidence = Column(Float, default=0)
    entity_id = Column(Integer)
    entity_type = Column(String(50))
    status = Column(String(20), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
