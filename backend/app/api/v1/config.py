from fastapi import APIRouter
from app.core.response import success_response
from config import get_settings
from app.core.service_urls import get_ai_services_url, get_backend_url
from app.db.providers import get_db_provider_name

router = APIRouter()


@router.get("/config")
async def get_config():
    settings = get_settings()
    return success_response(data={
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "debug": settings.app_debug,
        "default_ai_provider": settings.default_ai_provider,
        "db_provider": get_db_provider_name(),
        "ai_services_url": get_ai_services_url(),
        "backend_url": get_backend_url(),
        "features": {
            "authentication": False,
            "ai_chat": True,
            "file_upload": True,
            "real_time": True,
            "offline_sync": True,
        },
    })
