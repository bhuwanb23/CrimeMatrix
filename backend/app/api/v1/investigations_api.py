from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.investigation_service import InvestigationService
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate, InvestigationResponse, InvestigationListItem
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return InvestigationService(db)


@router.get("/")
async def list_investigations(
    status: str = Query(default=None),
    search: str = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    items = await svc.list_investigations(status=status, search=search, limit=limit, offset=offset)
    return success_response(data={"items": items, "total": len(items)})


@router.get("/{investigation_id}")
async def get_investigation(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    inv = await svc.get_investigation(investigation_id)
    if not inv:
        return success_response(message="Investigation not found")
    return success_response(data=inv)


@router.post("/")
async def create_investigation(data: InvestigationCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    inv = await svc.create_investigation(data.model_dump())
    return success_response(data=inv, message="Investigation created")


@router.put("/{investigation_id}")
async def update_investigation(
    investigation_id: int, data: InvestigationUpdate, db: AsyncSession = Depends(get_db)
):
    svc = get_service(db)
    inv = await svc.update_investigation(investigation_id, data.model_dump(exclude_unset=True))
    if not inv:
        return success_response(message="Investigation not found")
    return success_response(data=inv, message="Investigation updated")


@router.delete("/{investigation_id}")
async def delete_investigation(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete_investigation(investigation_id)
    return success_response(message="Investigation deleted" if deleted else "Investigation not found")
