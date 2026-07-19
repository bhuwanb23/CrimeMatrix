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
    sort_by: str = Query(default="created_at"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    items = await svc.list_investigations(status=status, search=search, sort_by=sort_by, limit=limit, offset=offset)
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


@router.get("/recent")
async def get_recent_investigations(
    limit: int = Query(default=3, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    items = await svc.get_recent(limit=limit)
    return success_response(data={"items": items})


@router.put("/{investigation_id}/save")
async def toggle_save(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.save_investigation(investigation_id)
    if not result:
        return success_response(message="Investigation not found")
    return success_response(data=result, message=f"Investigation {'saved' if result['status'] == 'saved' else 'resumed'}")


@router.get("/stats")
async def investigation_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    stats = await svc.get_stats()
    return success_response(data=stats)
