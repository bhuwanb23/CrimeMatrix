from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.map_service import MapService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return MapService(db)


@router.get("/stats")
async def map_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_spatial_stats())


@router.get("/crime-markers")
async def crime_markers(
    district_id: int = Query(default=None),
    crime_type_id: int = Query(default=None),
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_crime_markers(district_id, crime_type_id, days))


@router.get("/districts")
async def district_geojson(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_district_geojson())


@router.get("/heatmap")
async def heatmap_data(
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_heatmap_data(days))


@router.get("/hotspots")
async def hotspot_markers(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_hotspot_markers())


@router.get("/stations")
async def station_markers(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_station_markers())


@router.get("/routes")
async def route_data(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_route_data())
