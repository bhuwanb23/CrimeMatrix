from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), nullable=False)
    owner_id = Column(Integer)
    carrier = Column(String(50))
    type = Column(String(20), default="mobile")
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
