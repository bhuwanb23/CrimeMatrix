from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class EmbeddingDocument(Base):
    __tablename__ = "embedding_documents"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(50), nullable=False, index=True)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    source = Column(String(100), default="unknown")
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EmbeddingChunk(Base):
    __tablename__ = "embedding_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    vector_json = Column(Text, nullable=False)
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
