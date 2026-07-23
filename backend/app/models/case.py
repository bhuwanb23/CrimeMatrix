from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    crime_no = Column(String(50), unique=True, nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    crime_type = Column(String(50), nullable=False)
    district = Column(String(100), nullable=False)
    status = Column(String(20), default="active")
    priority = Column(String(20), default="medium")
    officer_id = Column(Integer, ForeignKey("users.id"))
    fir_id = Column(Integer, ForeignKey("firs.id"))

    # ER Diagram columns — CaseMaster
    incident_from_date = Column(DateTime(timezone=True), nullable=True)
    incident_to_date = Column(DateTime(timezone=True), nullable=True)
    info_received_ps_date = Column(DateTime(timezone=True), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    brief_facts = Column(Text, nullable=True)

    # FK references to lookup tables
    case_category_id = Column(Integer, ForeignKey("case_categories.id"), nullable=True)
    gravity_offence_id = Column(Integer, ForeignKey("gravity_offences.id"), nullable=True)
    crime_major_head_id = Column(Integer, ForeignKey("crime_heads.id"), nullable=True)
    crime_minor_head_id = Column(Integer, ForeignKey("crime_sub_heads.id"), nullable=True)
    case_status_id = Column(Integer, ForeignKey("case_status_master.id"), nullable=True)
    court_id = Column(Integer, ForeignKey("courts.id"), nullable=True)
    police_person_id = Column(Integer, ForeignKey("officers.id"), nullable=True)
    police_station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
