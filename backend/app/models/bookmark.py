from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    entity_type = Column(String(50), default="investigation")
    entity_id = Column(Integer, index=True)
    bookmark_note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
