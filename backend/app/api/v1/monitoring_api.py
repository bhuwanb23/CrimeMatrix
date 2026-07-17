from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.monitoring.persistence import MonitoringPersistence
from app.core.response import success_response
from fastapi import Query

router = APIRouter()


class ModelUsageRequest(BaseModel):
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    duration_ms: float = 0
    session_id: str = "default"
    status: str = "success"


class LatencyRequest(BaseModel):
    endpoint: str
    duration_ms: float
    provider: Optional[str] = None
    status: str = "ok"


class TokenUsageRequest(BaseModel):
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    session_id: str = "default"


class ToolCallRequest(BaseModel):
    tool_name: str
    success: bool = True
    duration_ms: float = 0
    error: Optional[str] = None
    request_id: Optional[str] = None


@router.post("/model-usage")
async def record_model_usage(data: ModelUsageRequest, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    record_id = await mon.record_model_usage(data.provider, data.model, data.prompt_tokens,
                                             data.completion_tokens, data.duration_ms,
                                             data.session_id, data.status)
    return success_response(data={"id": record_id})


@router.get("/model-usage")
async def get_model_usage(provider: str = None, limit: int = 100, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    records = await mon.get_model_usage(provider, limit)
    return success_response(data=records)


@router.get("/model-usage/summary")
async def model_usage_summary(db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    summary = await mon.get_model_usage_summary()
    return success_response(data=summary)


@router.post("/latency")
async def record_latency(data: LatencyRequest, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    record_id = await mon.record_latency(data.endpoint, data.duration_ms, data.provider, data.status)
    return success_response(data={"id": record_id})


@router.get("/latency")
async def get_latency(endpoint: str = None, limit: int = 100, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    records = await mon.get_latency(endpoint, limit)
    return success_response(data=records)


@router.get("/latency/stats")
async def latency_stats(endpoint: str = None, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    stats = await mon.get_latency_stats(endpoint)
    return success_response(data=stats)


@router.post("/tokens")
async def record_tokens(data: TokenUsageRequest, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    record_id = await mon.record_tokens(data.provider, data.model, data.prompt_tokens,
                                        data.completion_tokens, data.session_id)
    return success_response(data={"id": record_id})


@router.get("/tokens")
async def get_tokens(provider: str = None, limit: int = 100, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    records = await mon.get_token_usage(provider, limit)
    return success_response(data=records)


@router.get("/tokens/summary")
async def token_summary(db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    summary = await mon.get_token_summary()
    return success_response(data=summary)


@router.post("/tool-calls")
async def record_tool_call(data: ToolCallRequest, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    record_id = await mon.record_tool_call(data.tool_name, data.success, data.duration_ms,
                                           data.error, data.request_id)
    return success_response(data={"id": record_id})


@router.get("/tool-calls")
async def get_tool_calls(tool_name: str = None, limit: int = 100, db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    records = await mon.get_tool_calls(tool_name, limit)
    return success_response(data=records)


@router.get("/tool-calls/stats")
async def tool_call_stats(db: AsyncSession = Depends(get_db)):
    mon = MonitoringPersistence(db)
    stats = await mon.get_tool_call_stats()
    return success_response(data=stats)
