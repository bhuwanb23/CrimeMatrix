from fastapi import APIRouter
from app.core.response import success_response

router = APIRouter()


@router.get("/version")
async def get_version():
    return success_response(data={
        "version": "1.0.0",
        "api_version": "v1",
        "build": "2026-07-16",
        "python_version": "3.13",
        "framework": "FastAPI",
    })
