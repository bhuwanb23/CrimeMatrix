from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.priority_service import PriorityService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return PriorityService(db)


@router.get("/stats")
async def priority_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_priorities(
    investigation_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    priorities = await svc.get_priorities(investigation_id)
    return success_response(data={"items": priorities, "total": len(priorities)})


@router.get("/rankings")
async def rankings(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_rankings(limit))


@router.get("/explain/{investigation_id}")
async def explain(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    explanations = await svc.get_explain(investigation_id)
    return success_response(data={"items": explanations, "total": len(explanations)})


@router.get("/history/{investigation_id}")
async def history(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    h = await svc.get_history(investigation_id)
    return success_response(data={"items": h, "total": len(h)})


@router.get("/workload")
async def workload(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_workload())


@router.post("/score/{investigation_id}")
async def score(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.score_investigation(investigation_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Priority score generated")


@router.post("/batch-score")
async def batch_score(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.batch_score()
    return success_response(data=result, message="Batch scoring complete")
