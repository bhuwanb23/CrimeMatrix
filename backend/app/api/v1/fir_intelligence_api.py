from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.fir_analysis_service import FIRAnalysisService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return FIRAnalysisService(db)


async def _phase1_suggestions(fir_id):
    from app.db.phase1_aggregations import derive_fir_suggestions, geo_context

    return derive_fir_suggestions(await geo_context(), fir_id)


@router.get("/stats")
async def fir_intelligence_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all_safe

        crimes = await fetch_all_safe("crimes")
        return success_response(
            data={"total_suggestions": len(crimes) * 2, "total_analyses": len(crimes)}
        )
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.post("/analyze/{fir_id}")
async def analyze_fir(fir_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        suggestions = await _phase1_suggestions(fir_id)
        if not suggestions:
            return success_response(message="FIR not found")
        return success_response(
            data={
                "fir_id": fir_id,
                "suggestions": suggestions,
                "suggestions_count": len(suggestions),
            },
            message="FIR analyzed",
        )
    svc = get_service(db)
    result = await svc.analyze_fir(fir_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="FIR analyzed")


@router.get("/suggestions/{fir_id}")
async def get_suggestions(fir_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        suggestions = await _phase1_suggestions(fir_id)
        return success_response(data={"items": suggestions, "total": len(suggestions)})
    svc = get_service(db)
    suggestions = await svc.get_suggestions(fir_id)
    return success_response(data={"items": suggestions, "total": len(suggestions)})


@router.get("/history/{fir_id}")
async def get_history(fir_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fir_analysis_history

        history = await fir_analysis_history(fir_id)
        return success_response(data={"items": history, "total": len(history)})
    svc = get_service(db)
    history = await svc.get_history(fir_id)
    return success_response(data={"items": history, "total": len(history)})
