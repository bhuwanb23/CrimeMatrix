import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.reports.templates import TemplateEngine
from app.reports.pdf_generator import PDFGenerator
from app.reports.timeline_export import TimelineExporter
from app.reports.evidence_export import EvidenceExporter
from app.reports.investigation_export import InvestigationExporter
from app.reports.queue import ReportQueue
from app.core.response import success_response
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

template_engine = TemplateEngine()
pdf_gen = PDFGenerator()
report_queue = ReportQueue()


class GenerateReportRequest(BaseModel):
    crime_id: int
    template_id: Optional[str] = None


class QueueReportRequest(BaseModel):
    report_type: str
    crime_id: int
    template_id: Optional[str] = None


# Templates
@router.get("/templates")
async def list_templates():
    return success_response(data=template_engine.list_templates())


@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    t = template_engine.get_template(template_id)
    if "error" in t:
        return success_response(message=t["error"])
    return success_response(data=t)


# Generate PDFs
@router.post("/generate/summary")
async def generate_summary(data: GenerateReportRequest, db: AsyncSession = Depends(get_db)):
    exporter = InvestigationExporter(db)
    report_data = await exporter.export_json(data.crime_id)
    if "error" in report_data:
        return success_response(message=report_data["error"])
    filepath = pdf_gen.generate_summary(report_data)
    filename = os.path.basename(filepath)
    return success_response(data={"filename": filename, "path": filepath})


@router.post("/generate/timeline")
async def generate_timeline(data: GenerateReportRequest, db: AsyncSession = Depends(get_db)):
    exporter = TimelineExporter(db)
    report_data = await exporter.export_json(data.crime_id)
    if "error" in report_data:
        return success_response(message=report_data["error"])
    filepath = pdf_gen.generate_timeline(report_data)
    filename = os.path.basename(filepath)
    return success_response(data={"filename": filename, "path": filepath})


@router.post("/generate/evidence")
async def generate_evidence(data: GenerateReportRequest, db: AsyncSession = Depends(get_db)):
    exporter = EvidenceExporter(db)
    report_data = await exporter.export_json(data.crime_id)
    if "error" in report_data:
        return success_response(message=report_data["error"])
    filepath = pdf_gen.generate_evidence(report_data)
    filename = os.path.basename(filepath)
    return success_response(data={"filename": filename, "path": filepath})


@router.post("/generate/investigation")
async def generate_investigation(data: GenerateReportRequest, db: AsyncSession = Depends(get_db)):
    exporter = InvestigationExporter(db)
    report_data = await exporter.export_json(data.crime_id)
    if "error" in report_data:
        return success_response(message=report_data["error"])
    filepath = pdf_gen.generate_investigation(report_data)
    filename = os.path.basename(filepath)
    return success_response(data={"filename": filename, "path": filepath})


# Export JSON
@router.get("/export/timeline/{crime_id}")
async def export_timeline_json(crime_id: int, db: AsyncSession = Depends(get_db)):
    exporter = TimelineExporter(db)
    data = await exporter.export_json(crime_id)
    return success_response(data=data)


@router.get("/export/evidence/{crime_id}")
async def export_evidence_json(crime_id: int, db: AsyncSession = Depends(get_db)):
    exporter = EvidenceExporter(db)
    data = await exporter.export_json(crime_id)
    return success_response(data=data)


@router.get("/export/investigation/{crime_id}")
async def export_investigation_json(crime_id: int, db: AsyncSession = Depends(get_db)):
    exporter = InvestigationExporter(db)
    data = await exporter.export_json(crime_id)
    return success_response(data=data)


# Report Queue
@router.post("/queue")
async def queue_report(data: QueueReportRequest):
    job = report_queue.submit(data.report_type, {"crime_id": data.crime_id}, data.template_id)
    return success_response(data=job, message="Report queued")


@router.get("/queue")
async def list_queue():
    return success_response(data=report_queue.list_jobs())


@router.get("/queue/{job_id}")
async def get_queue_job(job_id: str):
    job = report_queue.get_job(job_id)
    if not job:
        return success_response(message="Job not found")
    return success_response(data=job)


@router.delete("/queue/{job_id}")
async def cancel_queue_job(job_id: str):
    cancelled = report_queue.cancel(job_id)
    return success_response(message="Job cancelled" if cancelled else "Cannot cancel job")


# Download
@router.get("/download/{filename}")
async def download_report(filename: str):
    filepath = os.path.join(os.path.dirname(__file__), "generated", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, media_type="application/pdf", filename=filename)
