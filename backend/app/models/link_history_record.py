from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class LinkHistoryRecord(Base):
    __tablename__ = "link_history"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, nullable=False, index=True)
    action = Column(String(50))
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
