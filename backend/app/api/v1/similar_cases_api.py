from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.similar_case_service import SimilarCaseService
from app.schemas.similar_cases import SimilarCasesResponse, CompareResponse, ComputeRequest, SimilarCaseResult
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return SimilarCaseService(db)


@router.get("/stats")
async def similarity_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    stats = await svc.get_stats()
    return success_response(data=stats)


@router.get("/{case_id}")
async def get_similar_cases(
    case_id: int,
    top_k: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    similar = await svc.get_similar(case_id, top_k)

    results = [SimilarCaseResult(**s) for s in similar]
    return success_response(data={
        "case_id": case_id,
        "similar_cases": [r.model_dump() for r in results],
        "count": len(results),
    })


@router.post("/compute")
async def compute_similarities(data: ComputeRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.compute_similarity(case_id=data.case_id, force=data.force)
    return success_response(data=result, message="Similarity computation complete")


@router.get("/compare/{case_id_1}/{case_id_2}")
async def compare_two_cases(case_id_1: int, case_id_2: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.compare_cases(case_id_1, case_id_2)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)
