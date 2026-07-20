from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CrimePrediction(Base):
    __tablename__ = "crime_predictions"

    id = Column(Integer, primary_key=True, index=True)
    prediction_type = Column(String(50), nullable=False)
    district_id = Column(Integer)
    crime_type_id = Column(Integer)
    predicted_value = Column(Float, default=0)
    confidence = Column(Float, default=0)
    actual_value = Column(Float)
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())
    target_date = Column(String(20))
    model_name = Column(String(100))
    model_version = Column(String(20))
    features_json = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
