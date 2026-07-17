from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rule_type = Column(String(50), nullable=False)
    conditions = Column(Text)
    actions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AlertMatch(Base):
    __tablename__ = "alert_matches"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, nullable=False, index=True)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    match_data = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
