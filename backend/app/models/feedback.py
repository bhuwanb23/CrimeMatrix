from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    query = Column(Text)
    response = Column(Text)
    rating = Column(Integer)
    comment = Column(Text)
    tags = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ResponseRating(Base):
    __tablename__ = "response_ratings"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text)
    response = Column(Text)
    rating = Column(Integer)
    domain = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HallucinationReport(Base):
    __tablename__ = "hallucination_reports"

    id = Column(Integer, primary_key=True, index=True)
    response = Column(Text)
    claim = Column(Text)
    supported = Column(Boolean)
    evidence = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
