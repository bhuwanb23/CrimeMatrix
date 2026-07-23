from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class ActSectionAssociation(Base):
    __tablename__ = "act_section_associations"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    act_id = Column(Integer, ForeignKey("acts.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    act_order = Column(Integer, default=1)
    section_order = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
