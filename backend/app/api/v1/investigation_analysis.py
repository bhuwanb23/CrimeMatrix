from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.investigation_analysis_service import InvestigationAnalysisService
from app.core.response import success_response

router = APIRouter()


class AnalyzeRequest(BaseModel):
    analysis_type: str = "summary"
    question: Optional[str] = None


def get_service(db: AsyncSession):
    return InvestigationAnalysisService(db)


@router.post("/{investigation_id}/analyze")
async def analyze_investigation(
    investigation_id: int,
    data: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.analyze(
        investigation_id=investigation_id,
        analysis_type=data.analysis_type,
        question=data.question,
    )
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)
