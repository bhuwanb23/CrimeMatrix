from fastapi import APIRouter
from app.core.response import success_response
from config import get_settings

router = APIRouter()


@router.get("/config")
async def get_config():
    settings = get_settings()
    return success_response(data={
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "debug": settings.app_debug,
        "default_ai_provider": settings.default_ai_provider,
        "features": {
            "authentication": False,
            "ai_chat": True,
            "file_upload": True,
            "real_time": True,
            "offline_sync": True,
        },
    })
