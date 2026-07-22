from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.cross_district_service import CrossDistrictService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return CrossDistrictService(db)


@router.get("/stats")
async def cross_district_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/matches")
async def list_matches(
    match_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    matches = await svc.get_matches(match_type)
    return success_response(data={"items": matches, "total": len(matches)})


@router.get("/matches/{match_id}")
async def get_match(match_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    match = await svc.get_match(match_id)
    if not match:
        return success_response(message="Match not found")
    return success_response(data=match)


@router.get("/compare")
async def compare_districts(
    district1: str = Query(...),
    district2: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.compare_districts(district1, district2))


@router.post("/detect")
async def detect_matches(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.detect_matches()
    return success_response(data=result, message="Cross-district detection complete")
