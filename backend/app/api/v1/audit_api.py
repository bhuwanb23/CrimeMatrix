from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.audit.request_logs import RequestLogStore
from app.audit.system_logs import SystemLogStore
from app.audit.activity_logs import ActivityLogStore
from app.audit.model_logs import ModelLogStore
from app.audit.error_logs import ErrorLogStore
from app.audit.jobs import BackgroundJobStore
from app.audit.stores import request_logs, api_logs, metrics
from app.core.response import success_response
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

# Non-shared instances (only used by API, not middleware)
system_logs = SystemLogStore()
activity_logs = ActivityLogStore()
model_logs = ModelLogStore()
error_logs = ErrorLogStore()
jobs = BackgroundJobStore()


# Request Logs
@router.get("/request-logs")
async def list_request_logs(limit: int = 100, offset: int = 0, method: str = None,
                           status_code: int = None, path: str = None):
    logs = request_logs.list_logs(limit, offset, method, status_code, path)
    return success_response(data={"logs": logs, "total": request_logs.get_count()})


# System Logs
@router.get("/system-logs")
async def list_system_logs(limit: int = 100, offset: int = 0, level: str = None):
    logs = system_logs.list_logs(limit, offset, level)
    return success_response(data=logs)


class SystemLogRequest(BaseModel):
    level: str = "info"
    message: str
    component: str = "system"
    details: Optional[Dict[str, Any]] = None


@router.post("/system-logs")
async def create_system_log(data: SystemLogRequest):
    entry = system_logs.log(data.level, data.message, data.component, data.details)
    return success_response(data=entry, message="System log created")


# Activity Logs
@router.get("/activity-logs")
async def list_activity_logs(limit: int = 100, offset: int = 0, user_id: str = None,
                             action: str = None, entity_type: str = None):
    logs = activity_logs.list_logs(limit, offset, user_id, action, entity_type)
    return success_response(data=logs)


class ActivityLogRequest(BaseModel):
    user_id: str
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None


@router.post("/activity-logs")
async def create_activity_log(data: ActivityLogRequest):
    entry = activity_logs.log(data.user_id, data.action, data.entity_type,
                              data.entity_id, data.details, data.ip_address)
    metrics.increment("activity_actions_total")
    return success_response(data=entry, message="Activity log created")


# API Logs
@router.get("/api-logs")
async def list_api_logs(limit: int = 100, offset: int = 0, method: str = None,
                        status_code: int = None):
    logs = api_logs.list_logs(limit, offset, method, status_code)
    return success_response(data=logs)


@router.get("/api-logs/summary")
async def api_logs_summary():
    summary = api_logs.get_summary()
    return success_response(data=summary)


# Model Logs
@router.get("/model-logs")
async def list_model_logs(limit: int = 100, offset: int = 0, provider: str = None,
                          status: str = None):
    logs = model_logs.list_logs(limit, offset, provider, status)
    stats = model_logs.get_stats()
    return success_response(data={"logs": logs, "stats": stats})


class ModelLogRequest(BaseModel):
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    duration_ms: float = 0
    status: str = "success"
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@router.post("/model-logs")
async def create_model_log(data: ModelLogRequest):
    entry = model_logs.log(data.provider, data.model, data.prompt_tokens,
                           data.completion_tokens, data.duration_ms,
                           data.status, data.error, data.metadata)
    metrics.increment("model_calls_total")
    metrics.observe("model_duration_ms", data.duration_ms)
    return success_response(data=entry, message="Model log created")


# Error Logs
@router.get("/error-logs")
async def list_error_logs(limit: int = 100, offset: int = 0, error_type: str = None,
                          status_code: int = None):
    logs = error_logs.list_logs(limit, offset, error_type, status_code)
    return success_response(data={"logs": logs, "total": error_logs.get_count()})


class ErrorLogRequest(BaseModel):
    error_type: str
    message: str
    path: Optional[str] = None
    method: Optional[str] = None
    status_code: int = 500
    stack_trace: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@router.post("/error-logs")
async def create_error_log(data: ErrorLogRequest):
    entry = error_logs.log(data.error_type, data.message, data.path, data.method,
                           data.status_code, data.stack_trace, data.details)
    metrics.increment("errors_total")
    return success_response(data=entry, message="Error log created")


# Background Jobs
@router.get("/jobs")
async def list_jobs(status: str = None, limit: int = 50):
    job_list = jobs.list_jobs(status, limit)
    stats = jobs.get_stats()
    return success_response(data={"jobs": job_list, "stats": stats})


class JobSubmitRequest(BaseModel):
    job_type: str
    name: str
    payload: Optional[Dict[str, Any]] = None


@router.post("/jobs")
async def submit_job(data: JobSubmitRequest):
    job = jobs.submit(data.job_type, data.name, data.payload)
    metrics.increment("jobs_submitted_total")
    return success_response(data=job, message="Job submitted")


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if not job:
        return success_response(message="Job not found")
    return success_response(data=job)


@router.put("/jobs/{job_id}/complete")
async def complete_job(job_id: str, result: Dict[str, Any] = None):
    success = jobs.complete(job_id, result)
    if success:
        metrics.increment("jobs_completed_total")
    return success_response(message="Job completed" if success else "Job not found")


@router.put("/jobs/{job_id}/fail")
async def fail_job(job_id: str, error: str = "Unknown error"):
    success = jobs.fail(job_id, error)
    if success:
        metrics.increment("jobs_failed_total")
    return success_response(message="Job failed" if success else "Job not found")


# Metrics
@router.get("/metrics")
async def get_all_metrics():
    data = metrics.get_all_metrics()
    return success_response(data=data)


@router.get("/metrics/summary")
async def get_metrics_summary():
    summary = metrics.get_summary()
    return success_response(data=summary)
