from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Complainant(Base):
    __tablename__ = "complainants"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    age_year = Column(Integer, nullable=True)
    occupation_id = Column(Integer, ForeignKey("occupations.id"), nullable=True)
    religion_id = Column(Integer, ForeignKey("religions.id"), nullable=True)
    caste_id = Column(Integer, ForeignKey("caste_master.id"), nullable=True)
    gender_id = Column(Integer, ForeignKey("genders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
