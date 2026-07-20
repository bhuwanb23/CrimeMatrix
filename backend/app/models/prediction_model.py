from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class PredictionModelRecord(Base):
    __tablename__ = "prediction_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20))
    description = Column(Text)
    accuracy = Column(Float, default=0)
    last_trained = Column(DateTime(timezone=True))
    status = Column(String(20), default="active")
    parameters_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
