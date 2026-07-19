from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class CaseEmbedding(Base):
    __tablename__ = "case_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, nullable=False, index=True)
    dimension = Column(String(20), nullable=False)
    vector_json = Column(Text, nullable=False)
    content = Column(Text)
    model_version = Column(String(50), default="tfidf_v1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
