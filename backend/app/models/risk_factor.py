from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(Integer, primary_key=True, index=True)
    suspect_id = Column(Integer, nullable=False, index=True)
    factor_name = Column(String(100), nullable=False)
    factor_value = Column(Float)
    weight = Column(Float, default=0)
    description = Column(Text)
    source = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
