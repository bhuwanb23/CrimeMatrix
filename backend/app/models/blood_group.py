from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class BloodGroup(Base):
    __tablename__ = "blood_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), nullable=False)
    code = Column(String(5), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
