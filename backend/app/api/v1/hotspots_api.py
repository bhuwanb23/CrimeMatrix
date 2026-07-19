from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.hotspot_service import HotspotService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return HotspotService(db)


@router.get("/stats")
async def hotspot_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_hotspots(
    risk_level: str = Query(default=None),
    hotspot_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    hotspots = await svc.get_hotspots(risk_level=risk_level, hotspot_type=hotspot_type)
    return success_response(data={"items": hotspots, "total": len(hotspots)})


@router.get("/rankings")
async def hotspot_rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    rankings = await svc.get_rankings(limit)
    return success_response(data=rankings)


@router.get("/risk-map")
async def risk_map(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_risk_map())


@router.get("/clusters")
async def get_clusters(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_clusters())


@router.get("/density/{district_id}")
async def density_analysis(district_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_density(district_id))


@router.post("/detect")
async def detect_hotspots(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.detect_hotspots()
    return success_response(data=result, message="Hotspot detection complete")


@router.get("/{hotspot_id}")
async def get_hotspot(hotspot_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    hotspot = await svc.get_hotspot(hotspot_id)
    if not hotspot:
        return success_response(message="Hotspot not found")
    return success_response(data=hotspot)
