from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class MOSimilarityRecord(Base):
    __tablename__ = "mo_similarity"

    id = Column(Integer, primary_key=True, index=True)
    profile_id_1 = Column(Integer, nullable=False, index=True)
    profile_id_2 = Column(Integer, nullable=False, index=True)
    similarity_score = Column(Float, default=0)
    match_level = Column(String(20))
    shared_features = Column(Text)
    compared_at = Column(DateTime(timezone=True), server_default=func.now())
