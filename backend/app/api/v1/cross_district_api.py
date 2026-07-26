from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.cross_district_service import CrossDistrictService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return CrossDistrictService(db)


async def _phase1_matches():
    from app.db.phase1_aggregations import derive_cross_district_matches, fetch_all_safe

    return derive_cross_district_matches(
        await fetch_all_safe("suspects"),
        await fetch_all_safe("vehicles"),
        await fetch_all_safe("phones"),
    )


@router.get("/stats")
async def cross_district_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import cross_district_stats as build_stats

        return success_response(data=build_stats(await _phase1_matches()))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/matches")
async def list_matches(
    match_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        matches = await _phase1_matches()
        if match_type:
            matches = [m for m in matches if m["match_type"] == match_type]
        return success_response(data={"items": matches, "total": len(matches)})
    svc = get_service(db)
    matches = await svc.get_matches(match_type)
    return success_response(data={"items": matches, "total": len(matches)})


@router.get("/compare")
async def compare_districts(
    district1: str = Query(...),
    district2: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        pair = {district1.strip().lower(), district2.strip().lower()}
        matches = [
            m
            for m in await _phase1_matches()
            if {str(m["district_1"]).lower(), str(m["district_2"]).lower()} == pair
        ]
        return success_response(data={
            "district_1": district1,
            "district_2": district2,
            "matches": matches,
            "total": len(matches),
        })
    svc = get_service(db)
    return success_response(data=await svc.compare_districts(district1, district2))


@router.get("/matches/{match_id}")
async def get_match(match_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        match = next((m for m in await _phase1_matches() if str(m["id"]) == str(match_id)), None)
        if not match:
            return success_response(message="Match not found")
        return success_response(data=match)
    if not match_id.isdigit():
        return success_response(message="Match not found")
    svc = get_service(db)
    match = await svc.get_match(int(match_id))
    if not match:
        return success_response(message="Match not found")
    return success_response(data=match)


@router.post("/detect")
async def detect_matches(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import cross_district_stats as build_stats

        matches = await _phase1_matches()
        by_type = build_stats(matches)["by_type"]
        return success_response(
            data={
                "matches_found": len(matches),
                "suspect_matches": by_type.get("suspect", 0),
                "vehicle_matches": by_type.get("vehicle", 0),
                "phone_matches": by_type.get("phone", 0),
                "items": matches,
            },
            message="Cross-district detection complete",
        )
    try:
        svc = get_service(db)
        result = await svc.detect_matches()
        return success_response(data=result, message="Cross-district detection complete")
    except Exception as e:
        return success_response(
            data={"matches_found": 0, "suspect_matches": 0, "vehicle_matches": 0, "phone_matches": 0},
            message=str(e)[:200],
        )
