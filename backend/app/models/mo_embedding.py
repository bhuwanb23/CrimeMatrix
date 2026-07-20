from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class MOEmbedding(Base):
    __tablename__ = "mo_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, nullable=False, index=True)
    dimension = Column(String(50))
    vector_json = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
