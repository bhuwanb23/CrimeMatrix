from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.case_status_repo import CaseStatusRepository
from app.schemas.case_status import CaseStatusCreate, CaseStatusResponse
from app.core.response import success_response

router = APIRouter()


@router.get("/investigation/{investigation_id}")
async def list_status_logs(investigation_id: int, db: AsyncSession = Depends(get_db)):
    repo = CaseStatusRepository(db)
    logs = await repo.get_by_investigation(investigation_id)
    return success_response(data=[CaseStatusResponse.model_validate(l).model_dump() for l in logs])


@router.post("/")
async def create_status_log(data: CaseStatusCreate, db: AsyncSession = Depends(get_db)):
    repo = CaseStatusRepository(db)
    log = await repo.create(data.model_dump())
    return success_response(data=CaseStatusResponse.model_validate(log).model_dump(), message="Status updated")
