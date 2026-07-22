from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.fir_analysis_service import FIRAnalysisService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return FIRAnalysisService(db)


@router.get("/stats")
async def fir_intelligence_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.post("/analyze/{fir_id}")
async def analyze_fir(fir_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.analyze_fir(fir_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="FIR analyzed")


@router.get("/suggestions/{fir_id}")
async def get_suggestions(fir_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    suggestions = await svc.get_suggestions(fir_id)
    return success_response(data={"items": suggestions, "total": len(suggestions)})


@router.get("/history/{fir_id}")
async def get_history(fir_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    history = await svc.get_history(fir_id)
    return success_response(data={"items": history, "total": len(history)})
