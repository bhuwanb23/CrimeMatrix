from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)
    content = Column(Text)
    format = Column(String(20), default="pdf")
    generated_by = Column(Integer)
    status = Column(String(20), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReportTemplate(Base):
    __tablename__ = "report_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    template_content = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReportExport(Base):
    __tablename__ = "report_exports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, nullable=False, index=True)
    file_path = Column(String(500))
    file_size = Column(Integer)
    format = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
