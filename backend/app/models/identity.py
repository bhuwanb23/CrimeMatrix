from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base


class IdentityGroup(Base):
    __tablename__ = "identity_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    group_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IdentityMatch(Base):
    __tablename__ = "identity_matches"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    score = Column(Float)
    match_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EntityAlias(Base):
    __tablename__ = "entity_aliases"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    alias = Column(String(100), nullable=False)
    alias_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
