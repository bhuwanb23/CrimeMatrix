from fastapi import APIRouter
from app.api.v1 import health, ai

router = APIRouter(prefix="/api/v1")
router.include_router(health.router, tags=["Health"])
router.include_router(ai.router, prefix="/ai", tags=["AI"])
