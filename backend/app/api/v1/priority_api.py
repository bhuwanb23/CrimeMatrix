from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.priority_service import PriorityService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return PriorityService(db)


async def _phase1_priorities():
    from app.db.phase1_aggregations import derive_priority_scores, fetch_all_safe, resolve_names

    investigations = await fetch_all_safe("investigations")
    district_names = await resolve_names("districts")
    return investigations, derive_priority_scores(investigations, district_names)


@router.get("/stats")
async def priority_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import priority_stats as build_stats

        _, scores = await _phase1_priorities()
        return success_response(data=build_stats(scores))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_priorities(
    investigation_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        _, scores = await _phase1_priorities()
        if investigation_id:
            scores = [s for s in scores if str(s["investigation_id"]) == str(investigation_id)]
        return success_response(data={"items": scores, "total": len(scores)})
    svc = get_service(db)
    priorities = await svc.get_priorities(investigation_id)
    return success_response(data={"items": priorities, "total": len(priorities)})


@router.get("/rankings")
async def rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        _, scores = await _phase1_priorities()
        return success_response(data=[
            {
                "investigation_id": s["investigation_id"],
                "title": s["title"],
                "overall_score": s["overall_score"],
                "priority_level": s["priority_level"],
                "district": s["district"],
                "progress": s["progress"],
            }
            for s in scores[:limit]
        ])
    svc = get_service(db)
    return success_response(data=await svc.get_rankings(limit))


@router.get("/explain/{investigation_id}")
async def explain(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        _, scores = await _phase1_priorities()
        match = next((s for s in scores if str(s["investigation_id"]) == str(investigation_id)), None)
        explanations = match["explanations"] if match else []
        return success_response(data={"items": explanations, "total": len(explanations)})
    svc = get_service(db)
    explanations = await svc.get_explain(investigation_id)
    return success_response(data={"items": explanations, "total": len(explanations)})


@router.get("/history/{investigation_id}")
async def history(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        _, scores = await _phase1_priorities()
        match = next((s for s in scores if str(s["investigation_id"]) == str(investigation_id)), None)
        items = (
            [{
                "score": match["overall_score"],
                "level": match["priority_level"],
                "scored_at": match["scored_at"],
                "change": 0,
            }]
            if match
            else []
        )
        return success_response(data={"items": items, "total": len(items)})
    svc = get_service(db)
    h = await svc.get_history(investigation_id)
    return success_response(data={"items": h, "total": len(h)})


@router.get("/workload")
async def workload(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import priority_workload

        investigations, _ = await _phase1_priorities()
        return success_response(data=priority_workload(investigations))
    svc = get_service(db)
    return success_response(data=await svc.get_workload())


@router.post("/score/{investigation_id}")
async def score(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        _, scores = await _phase1_priorities()
        match = next((s for s in scores if str(s["investigation_id"]) == str(investigation_id)), None)
        if not match:
            return success_response(message="Investigation not found")
        return success_response(data=match, message="Priority score generated")
    svc = get_service(db)
    result = await svc.score_investigation(investigation_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Priority score generated")


@router.post("/batch-score")
async def batch_score(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import priority_stats as build_stats

        _, scores = await _phase1_priorities()
        return success_response(
            data={"investigations_scored": len(scores), **build_stats(scores), "items": scores},
            message="Batch scoring complete",
        )
    svc = get_service(db)
    result = await svc.batch_score()
    return success_response(data=result, message="Batch scoring complete")
