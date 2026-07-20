from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.suspect_risk_service import SuspectRiskService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return SuspectRiskService(db)


@router.get("/stats")
async def suspect_risk_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/scores")
async def list_scores(
    suspect_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    scores = await svc.get_scores(suspect_id)
    return success_response(data={"items": scores, "total": len(scores)})


@router.get("/scores/{suspect_id}")
async def get_score(suspect_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    scores = await svc.get_scores(suspect_id)
    if not scores:
        return success_response(message="No risk score found")
    return success_response(data=scores[0])


@router.get("/history/{suspect_id}")
async def get_history(suspect_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    history = await svc.get_history(suspect_id)
    return success_response(data={"items": history, "total": len(history)})


@router.get("/factors/{suspect_id}")
async def get_factors(suspect_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    factors = await svc.get_factors(suspect_id)
    return success_response(data={"items": factors, "total": len(factors)})


@router.get("/rankings")
async def rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_rankings(limit))


@router.post("/score/{suspect_id}")
async def score_suspect(suspect_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.score_suspect(suspect_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Risk score generated")


@router.post("/batch-score")
async def batch_score(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.batch_score()
    return success_response(data=result, message="Batch scoring complete")
