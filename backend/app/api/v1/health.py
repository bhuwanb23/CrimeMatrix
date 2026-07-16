from fastapi import APIRouter
from app.core.response import success_response
from config import get_settings
import time

router = APIRouter()
start_time = time.time()


@router.get("/health")
async def health_check():
    settings = get_settings()
    return success_response(
        data={
            "status": "healthy",
            "version": "1.0.0",
            "uptime": round(time.time() - start_time, 2),
            "environment": settings.app_env,
        }
    )
