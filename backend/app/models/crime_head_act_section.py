from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class CrimeHeadActSection(Base):
    __tablename__ = "crime_head_act_sections"

    id = Column(Integer, primary_key=True, index=True)
    crime_head_id = Column(Integer, ForeignKey("crime_heads.id"), nullable=False, index=True)
    act_code = Column(String(50), ForeignKey("acts.act_code"), nullable=False)
    section_code = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
