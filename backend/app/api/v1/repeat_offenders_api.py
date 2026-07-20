from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.repeat_offender_service import RepeatOffenderService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return RepeatOffenderService(db)


@router.get("/stats")
async def repeat_offender_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_offenders(
    risk_level: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    offenders = await svc.get_offenders(risk_level)
    return success_response(data={"items": offenders, "total": len(offenders)})


@router.get("/rankings")
async def offender_rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_rankings(limit))


@router.post("/analyze")
async def analyze_offenders(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.analyze_offenders()
    return success_response(data=result, message="Repeat offender analysis complete")


@router.get("/{offender_id}")
async def get_offender(offender_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    offender = await svc.get_offender(offender_id)
    if not offender:
        return success_response(message="Offender not found")
    return success_response(data=offender)
