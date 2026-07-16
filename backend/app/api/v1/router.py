from fastapi import APIRouter
from app.api.v1 import health, ai, status, config, metadata, version, statistics, uploads

router = APIRouter(prefix="/api/v1")
router.include_router(health.router, tags=["Health"])
router.include_router(status.router, tags=["System"])
router.include_router(config.router, tags=["Configuration"])
router.include_router(metadata.router, tags=["Metadata"])
router.include_router(version.router, tags=["Version"])
router.include_router(statistics.router, tags=["Statistics"])
router.include_router(uploads.router, tags=["Uploads"])
router.include_router(ai.router, prefix="/ai", tags=["AI"])
