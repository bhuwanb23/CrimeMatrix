from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class CaseLink(Base):
    __tablename__ = "case_links"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    linked_case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    link_type = Column(String(50), nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
