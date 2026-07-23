from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    badge_number = Column(String(20), unique=True, nullable=False)
    rank = Column(String(50))
    rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=True)
    station_id = Column(Integer)
    unit_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    designation_id = Column(Integer, ForeignKey("designations.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    kgid = Column(String(20), unique=True, nullable=True)
    first_name = Column(String(100), nullable=True)
    dob = Column(Date, nullable=True)
    gender_id = Column(Integer, ForeignKey("genders.id"), nullable=True)
    blood_group_id = Column(Integer, ForeignKey("blood_groups.id"), nullable=True)
    physically_challenged = Column(Boolean, default=False)
    appointment_date = Column(Date, nullable=True)
    specialization = Column(String(100))
    phone = Column(String(20))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
