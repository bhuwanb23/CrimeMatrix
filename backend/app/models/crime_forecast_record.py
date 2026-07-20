from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class CrimeForecastRecord(Base):
    __tablename__ = "crime_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    forecast_type = Column(String(50), nullable=False)
    district_id = Column(Integer)
    crime_type_id = Column(Integer)
    forecast_date = Column(DateTime(timezone=True), server_default=func.now())
    target_period = Column(String(20))
    predicted_value = Column(Float, default=0)
    confidence = Column(Float, default=0)
    actual_value = Column(Float)
    model_name = Column(String(100))
    parameters_json = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
