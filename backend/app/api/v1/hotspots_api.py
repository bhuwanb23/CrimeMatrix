from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.hotspot_service import HotspotService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return HotspotService(db)


async def _phase1_hotspots():
    from app.db.phase1_aggregations import derive_hotspots, geo_context

    ctx = await geo_context()
    return ctx, derive_hotspots(ctx)


@router.get("/stats")
async def hotspot_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import hotspot_stats as build_stats

        _, hotspots = await _phase1_hotspots()
        return success_response(data=build_stats(hotspots))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_hotspots(
    risk_level: str = Query(default=None),
    hotspot_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        _, hotspots = await _phase1_hotspots()
        if risk_level:
            hotspots = [h for h in hotspots if h["risk_level"] == risk_level]
        if hotspot_type:
            hotspots = [h for h in hotspots if h["hotspot_type"] == hotspot_type]
        return success_response(data={"items": hotspots, "total": len(hotspots)})
    svc = get_service(db)
    hotspots = await svc.get_hotspots(risk_level=risk_level, hotspot_type=hotspot_type)
    return success_response(data={"items": hotspots, "total": len(hotspots)})


@router.get("/rankings")
async def hotspot_rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        _, hotspots = await _phase1_hotspots()
        return success_response(data=hotspots[:limit])
    svc = get_service(db)
    rankings = await svc.get_rankings(limit)
    return success_response(data=rankings)


@router.get("/risk-map")
async def risk_map(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import hotspot_risk_map

        _, hotspots = await _phase1_hotspots()
        return success_response(data=hotspot_risk_map(hotspots))
    svc = get_service(db)
    return success_response(data=await svc.get_risk_map())


@router.get("/clusters")
async def get_clusters(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import hotspot_clusters

        _, hotspots = await _phase1_hotspots()
        return success_response(data=hotspot_clusters(hotspots))
    svc = get_service(db)
    return success_response(data=await svc.get_clusters())


@router.get("/density/{district_id}")
async def density_analysis(district_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import geo_context, hotspot_density

        return success_response(data=hotspot_density(await geo_context(), district_id))
    if not district_id.isdigit():
        return success_response(message="Invalid district id")
    svc = get_service(db)
    return success_response(data=await svc.get_density(int(district_id)))


@router.post("/detect")
async def detect_hotspots(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        ctx, hotspots = await _phase1_hotspots()
        return success_response(
            data={
                "hotspots_found": len(hotspots),
                "hotspots_saved": len(hotspots),
                "total_crimes_analyzed": len(ctx["crimes"]),
                "items": hotspots,
            },
            message="Hotspot detection complete",
        )
    svc = get_service(db)
    result = await svc.detect_hotspots()
    return success_response(data=result, message="Hotspot detection complete")


@router.get("/{hotspot_id}")
async def get_hotspot(hotspot_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        _, hotspots = await _phase1_hotspots()
        match = next((h for h in hotspots if str(h["id"]) == str(hotspot_id)), None)
        if not match:
            return success_response(message="Hotspot not found")
        return success_response(data=match)
    if not hotspot_id.isdigit():
        return success_response(message="Hotspot not found")
    svc = get_service(db)
    hotspot = await svc.get_hotspot(int(hotspot_id))
    if not hotspot:
        return success_response(message="Hotspot not found")
    return success_response(data=hotspot)
