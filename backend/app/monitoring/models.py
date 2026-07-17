from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class ModelUsage(Base):
    __tablename__ = "model_usage"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False, index=True)
    model = Column(String(50), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    duration_ms = Column(Float, default=0)
    session_id = Column(String(50))
    status = Column(String(20), default="success")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LatencyRecord(Base):
    __tablename__ = "latency_records"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(200), nullable=False, index=True)
    provider = Column(String(50))
    duration_ms = Column(Float, nullable=False)
    status = Column(String(20), default="ok")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TokenUsageRecord(Base):
    __tablename__ = "token_usage_records"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False, index=True)
    model = Column(String(50))
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    session_id = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String(50), nullable=False, index=True)
    success = Column(Boolean, default=True)
    duration_ms = Column(Float, default=0)
    error = Column(Text)
    request_id = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
