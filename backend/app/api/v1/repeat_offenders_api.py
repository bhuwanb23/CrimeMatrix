from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.repeat_offender_service import RepeatOffenderService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return RepeatOffenderService(db)


async def _phase1_offenders():
    from app.db.phase1_aggregations import derive_repeat_offenders, fetch_all_safe

    return derive_repeat_offenders(
        await fetch_all_safe("suspects"),
        await fetch_all_safe("criminals"),
        await fetch_all_safe("crimes"),
    )


@router.get("/stats")
async def repeat_offender_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import repeat_offender_stats as build_stats

        return success_response(data=build_stats(await _phase1_offenders()))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_offenders(
    risk_level: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        offenders = await _phase1_offenders()
        if risk_level:
            offenders = [o for o in offenders if o["risk_level"] == risk_level]
        return success_response(data={"items": offenders, "total": len(offenders)})
    svc = get_service(db)
    offenders = await svc.get_offenders(risk_level)
    return success_response(data={"items": offenders, "total": len(offenders)})


@router.get("/rankings")
async def offender_rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        return success_response(data=(await _phase1_offenders())[:limit])
    svc = get_service(db)
    return success_response(data=await svc.get_rankings(limit))


@router.post("/analyze")
async def analyze_offenders(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import repeat_offender_stats as build_stats

        offenders = await _phase1_offenders()
        return success_response(
            data={"offenders_analyzed": len(offenders), **build_stats(offenders), "items": offenders},
            message="Repeat offender analysis complete",
        )
    svc = get_service(db)
    result = await svc.analyze_offenders()
    return success_response(data=result, message="Repeat offender analysis complete")


@router.get("/{offender_id}")
async def get_offender(offender_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        offenders = await _phase1_offenders()
        match = next(
            (o for o in offenders if str(o["id"]) == str(offender_id) or str(o["suspect_id"]) == str(offender_id)),
            None,
        )
        if not match:
            return success_response(message="Offender not found")
        scores = [
            {"name": key, "value": match[key]}
            for key in ("frequency_score", "recency_score", "severity_score", "geographic_score")
        ]
        return success_response(data={**match, "scores": scores})
    if not offender_id.isdigit():
        return success_response(message="Offender not found")
    svc = get_service(db)
    offender = await svc.get_offender(int(offender_id))
    if not offender:
        return success_response(message="Offender not found")
    return success_response(data=offender)
