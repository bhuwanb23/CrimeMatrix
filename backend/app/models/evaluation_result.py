from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_type = Column(String(50))
    model_name = Column(String(100))
    accuracy = Column(Float)
    precision_score = Column(Float)
    recall_score = Column(Float)
    f1_score = Column(Float)
    drift_indicator = Column(Float)
    sample_size = Column(Integer)
    evaluation_date = Column(DateTime(timezone=True), server_default=func.now())
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
