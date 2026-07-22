from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class IntelligenceEvent(Base):
    __tablename__ = "intelligence_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    entity_type = Column(String(50))
    event_data = Column(Text)
    status = Column(String(20), default="pending")
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
