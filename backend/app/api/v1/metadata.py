from fastapi import APIRouter
from app.core.response import success_response

router = APIRouter()


@router.get("/metadata")
async def get_metadata():
    return success_response(data={
        "api_version": "1.0.0",
        "api_prefix": "/api/v1",
        "supported_features": [
            "health_check",
            "ai_chat",
            "file_upload",
            "real_time_websocket",
            "offline_sync",
            "case_management",
            "investigation_tracking",
            "criminal_profiling",
            "evidence_management",
        ],
        "rate_limits": {
            "requests_per_minute": 60,
            "ai_requests_per_minute": 10,
        },
        "pagination": {
            "default_page_size": 20,
            "max_page_size": 100,
        },
    })
