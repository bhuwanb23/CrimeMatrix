import json
from typing import Dict, List, Optional
from sqlalchemy import select, delete, func as sql_func
from sqlalchemy.ext.asyncio import AsyncSession
from app.monitoring.models import ModelUsage, LatencyRecord, TokenUsageRecord, ToolCall
import structlog

logger = structlog.get_logger()


class MonitoringPersistence:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Model Usage
    async def record_model_usage(self, provider: str, model: str, prompt_tokens: int,
                                  completion_tokens: int, duration_ms: float,
                                  session_id: str = "default", status: str = "success") -> int:
        record = ModelUsage(provider=provider, model=model, prompt_tokens=prompt_tokens,
                           completion_tokens=completion_tokens, duration_ms=duration_ms,
                           session_id=session_id, status=status)
        self.db.add(record)
        await self.db.commit()
        return record.id

    async def get_model_usage(self, provider: str = None, limit: int = 100) -> List[Dict]:
        query = select(ModelUsage)
        if provider:
            query = query.where(ModelUsage.provider == provider)
        query = query.order_by(ModelUsage.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return [
            {"id": r.id, "provider": r.provider, "model": r.model,
             "prompt_tokens": r.prompt_tokens, "completion_tokens": r.completion_tokens,
             "duration_ms": r.duration_ms, "status": r.status, "created_at": str(r.created_at)}
            for r in result.scalars().all()
        ]

    async def get_model_usage_summary(self) -> Dict:
        result = await self.db.execute(select(ModelUsage))
        records = result.scalars().all()
        if not records:
            return {"total_calls": 0, "total_tokens": 0, "avg_duration_ms": 0}

        by_provider = {}
        for r in records:
            p = r.provider
            if p not in by_provider:
                by_provider[p] = {"calls": 0, "tokens": 0, "duration_ms": 0}
            by_provider[p]["calls"] += 1
            by_provider[p]["tokens"] += r.prompt_tokens + r.completion_tokens
            by_provider[p]["duration_ms"] += r.duration_ms

        total_tokens = sum(r.prompt_tokens + r.completion_tokens for r in records)
        return {
            "total_calls": len(records),
            "total_tokens": total_tokens,
            "avg_duration_ms": round(sum(r.duration_ms for r in records) / len(records), 2),
            "by_provider": by_provider,
        }

    # Latency
    async def record_latency(self, endpoint: str, duration_ms: float,
                              provider: str = None, status: str = "ok") -> int:
        record = LatencyRecord(endpoint=endpoint, provider=provider,
                              duration_ms=duration_ms, status=status)
        self.db.add(record)
        await self.db.commit()
        return record.id

    async def get_latency(self, endpoint: str = None, limit: int = 100) -> List[Dict]:
        query = select(LatencyRecord)
        if endpoint:
            query = query.where(LatencyRecord.endpoint == endpoint)
        query = query.order_by(LatencyRecord.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return [
            {"id": r.id, "endpoint": r.endpoint, "provider": r.provider,
             "duration_ms": r.duration_ms, "status": r.status, "created_at": str(r.created_at)}
            for r in result.scalars().all()
        ]

    async def get_latency_stats(self, endpoint: str = None) -> Dict:
        query = select(LatencyRecord)
        if endpoint:
            query = query.where(LatencyRecord.endpoint == endpoint)
        result = await self.db.execute(query)
        records = result.scalars().all()
        if not records:
            return {"count": 0, "avg_ms": 0, "min_ms": 0, "max_ms": 0}

        durations = sorted(r.duration_ms for r in records)
        n = len(durations)
        return {
            "count": n,
            "avg_ms": round(sum(durations) / n, 2),
            "min_ms": durations[0],
            "max_ms": durations[-1],
            "p50": durations[n // 2],
            "p95": durations[int(n * 0.95)] if n > 1 else durations[0],
        }

    # Token Usage
    async def record_tokens(self, provider: str, model: str, prompt_tokens: int,
                             completion_tokens: int, session_id: str = "default") -> int:
        record = TokenUsageRecord(provider=provider, model=model,
                                  prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
                                  total_tokens=prompt_tokens + completion_tokens,
                                  session_id=session_id)
        self.db.add(record)
        await self.db.commit()
        return record.id

    async def get_token_usage(self, provider: str = None, limit: int = 100) -> List[Dict]:
        query = select(TokenUsageRecord)
        if provider:
            query = query.where(TokenUsageRecord.provider == provider)
        query = query.order_by(TokenUsageRecord.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return [
            {"id": r.id, "provider": r.provider, "model": r.model,
             "prompt_tokens": r.prompt_tokens, "completion_tokens": r.completion_tokens,
             "total_tokens": r.total_tokens, "session_id": r.session_id,
             "created_at": str(r.created_at)}
            for r in result.scalars().all()
        ]

    async def get_token_summary(self) -> Dict:
        result = await self.db.execute(select(TokenUsageRecord))
        records = result.scalars().all()
        if not records:
            return {"total_calls": 0, "total_tokens": 0}

        by_provider = {}
        for r in records:
            p = r.provider
            if p not in by_provider:
                by_provider[p] = {"calls": 0, "tokens": 0}
            by_provider[p]["calls"] += 1
            by_provider[p]["tokens"] += r.total_tokens

        return {
            "total_calls": len(records),
            "total_tokens": sum(r.total_tokens for r in records),
            "by_provider": by_provider,
        }

    # Tool Calls
    async def record_tool_call(self, tool_name: str, success: bool, duration_ms: float,
                                error: str = None, request_id: str = None) -> int:
        record = ToolCall(tool_name=tool_name, success=success, duration_ms=duration_ms,
                         error=error, request_id=request_id)
        self.db.add(record)
        await self.db.commit()
        return record.id

    async def get_tool_calls(self, tool_name: str = None, limit: int = 100) -> List[Dict]:
        query = select(ToolCall)
        if tool_name:
            query = query.where(ToolCall.tool_name == tool_name)
        query = query.order_by(ToolCall.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return [
            {"id": r.id, "tool_name": r.tool_name, "success": r.success,
             "duration_ms": r.duration_ms, "error": r.error, "created_at": str(r.created_at)}
            for r in result.scalars().all()
        ]

    async def get_tool_call_stats(self) -> Dict:
        result = await self.db.execute(select(ToolCall))
        records = result.scalars().all()
        if not records:
            return {"total": 0, "success_rate": 0}

        success = sum(1 for r in records if r.success)
        by_tool = {}
        for r in records:
            t = r.tool_name
            if t not in by_tool:
                by_tool[t] = {"total": 0, "success": 0}
            by_tool[t]["total"] += 1
            if r.success:
                by_tool[t]["success"] += 1

        for t in by_tool:
            total = by_tool[t]["total"]
            by_tool[t]["success_rate"] = round(by_tool[t]["success"] / total * 100, 1) if total else 0

        return {
            "total": len(records),
            "success": success,
            "success_rate": round(success / len(records) * 100, 1),
            "by_tool": by_tool,
        }
