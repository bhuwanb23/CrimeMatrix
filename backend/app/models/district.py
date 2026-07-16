from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    state = Column(String(50), default="Karnataka")
    population = Column(Integer)
    area_sq_km = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
