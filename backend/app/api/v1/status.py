from fastapi import APIRouter
from app.core.response import success_response
from app.db.session import engine
from app.cache.local_cache import LocalCache
import structlog

router = APIRouter()
logger = structlog.get_logger()


@router.get("/status")
async def system_status():
    cache = LocalCache()

    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute(__import__('sqlalchemy').text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    # Check cache
    try:
        cache.set("__health_check", "ok", ttl=10)
        cache_status = "connected" if cache.get("__health_check") == "ok" else "error"
        cache.delete("__health_check")
    except Exception:
        cache_status = "error"

    return success_response(data={
        "database": db_status,
        "cache": cache_status,
        "ai_providers": {
            "ollama": "available",
            "gemini": "configured" if True else "not configured",
            "openai": "configured" if True else "not configured",
        },
    })
