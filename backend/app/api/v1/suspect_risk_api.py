from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.suspect_risk_service import SuspectRiskService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return SuspectRiskService(db)


async def _phase1_scores():
    from app.db.phase1_aggregations import derive_suspect_scores, fetch_all_safe

    return derive_suspect_scores(await fetch_all_safe("suspects"))


@router.get("/stats")
async def suspect_risk_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import suspect_risk_stats as build_stats

        return success_response(data=build_stats(await _phase1_scores()))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/scores")
async def list_scores(
    suspect_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        scores = await _phase1_scores()
        if suspect_id:
            scores = [s for s in scores if str(s["suspect_id"]) == str(suspect_id)]
        return success_response(data={"items": scores, "total": len(scores)})
    svc = get_service(db)
    scores = await svc.get_scores(suspect_id)
    return success_response(data={"items": scores, "total": len(scores)})


@router.get("/rankings")
async def rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        scores = await _phase1_scores()
        return success_response(data=[
            {
                "suspect_id": s["suspect_id"],
                "name": s["name"],
                "overall_score": s["overall_score"],
                "risk_level": s["risk_level"],
                "district": s["district"],
            }
            for s in scores[:limit]
        ])
    svc = get_service(db)
    return success_response(data=await svc.get_rankings(limit))


@router.get("/scores/{suspect_id}")
async def get_score(suspect_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        scores = await _phase1_scores()
        match = next((s for s in scores if str(s["suspect_id"]) == str(suspect_id)), None)
        if not match:
            return success_response(message="No risk score found")
        return success_response(data=match)
    svc = get_service(db)
    scores = await svc.get_scores(suspect_id)
    if not scores:
        return success_response(message="No risk score found")
    return success_response(data=scores[0])


@router.get("/history/{suspect_id}")
async def get_history(suspect_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        scores = await _phase1_scores()
        match = next((s for s in scores if str(s["suspect_id"]) == str(suspect_id)), None)
        history = (
            [{
                "score": match["overall_score"],
                "risk_level": match["risk_level"],
                "scored_at": match["scored_at"],
                "change": 0,
            }]
            if match
            else []
        )
        return success_response(data={"items": history, "total": len(history)})
    svc = get_service(db)
    history = await svc.get_history(suspect_id)
    return success_response(data={"items": history, "total": len(history)})


@router.get("/factors/{suspect_id}")
async def get_factors(suspect_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import suspect_risk_factors

        scores = await _phase1_scores()
        match = next((s for s in scores if str(s["suspect_id"]) == str(suspect_id)), None)
        factors = suspect_risk_factors(match) if match else []
        return success_response(data={"items": factors, "total": len(factors)})
    svc = get_service(db)
    factors = await svc.get_factors(suspect_id)
    return success_response(data={"items": factors, "total": len(factors)})


@router.post("/score/{suspect_id}")
async def score_suspect(suspect_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        scores = await _phase1_scores()
        match = next((s for s in scores if str(s["suspect_id"]) == str(suspect_id)), None)
        if not match:
            return success_response(message="Suspect not found")
        return success_response(data=match, message="Risk score generated")
    svc = get_service(db)
    result = await svc.score_suspect(suspect_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Risk score generated")


@router.post("/batch-score")
async def batch_score(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import suspect_risk_stats as build_stats

        scores = await _phase1_scores()
        return success_response(
            data={"suspects_scored": len(scores), "errors": 0, **build_stats(scores), "items": scores},
            message="Batch scoring complete",
        )
    svc = get_service(db)
    result = await svc.batch_score()
    return success_response(data=result, message="Batch scoring complete")
