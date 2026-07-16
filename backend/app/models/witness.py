from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class Witness(Base):
    __tablename__ = "witnesses"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer)
    case_id = Column(Integer)
    statement = Column(Text)
    reliability = Column(String(20), default="unknown")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
