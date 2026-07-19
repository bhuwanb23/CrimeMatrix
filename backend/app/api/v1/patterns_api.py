from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.pattern_service import PatternService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return PatternService(db)


@router.get("/stats")
async def pattern_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_patterns(
    pattern_type: str = Query(default=None),
    crime_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    patterns = await svc.get_patterns(pattern_type=pattern_type, crime_type=crime_type)
    return success_response(data={"items": patterns, "total": len(patterns)})


@router.get("/clusters")
async def get_clusters(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    clusters = await svc.get_clusters()
    return success_response(data=clusters)


@router.post("/detect")
async def detect_patterns(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.detect_patterns()
    return success_response(data=result, message="Pattern detection complete")


@router.get("/compare/{p1_id}/{p2_id}")
async def compare_patterns(p1_id: int, p2_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.compare_patterns(p1_id, p2_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)


@router.get("/{pattern_id}")
async def get_pattern(pattern_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    pattern = await svc.get_pattern(pattern_id)
    if not pattern:
        return success_response(message="Pattern not found")
    return success_response(data=pattern)


@router.get("/{pattern_id}/occurrences")
async def get_pattern_occurrences(pattern_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    occurrences = await svc.get_pattern_occurrences(pattern_id)
    return success_response(data={"items": occurrences, "total": len(occurrences)})
