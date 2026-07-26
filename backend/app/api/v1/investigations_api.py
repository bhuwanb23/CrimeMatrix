from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.investigation_service import InvestigationService
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate, InvestigationResponse, InvestigationListItem
from app.core.response import success_response
from app.db.phase1_store import store_get, store_list, using_phase1_store

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
    if using_phase1_store():
        page = (offset // limit) + 1 if limit else 1
        where = {"status": status} if status else None
        data = await store_list("investigations", page=page, page_size=limit, where=where)
        items = data["items"]
        if search:
            q = search.lower()
            items = [i for i in items if q in str(i.get("title", "")).lower()]
        return success_response(data={"items": items, "total": data.get("total", len(items))})
    svc = get_service(db)
    items = await svc.list_investigations(status=status, search=search, sort_by=sort_by, limit=limit, offset=offset)
    return success_response(data={"items": items, "total": len(items)})


# Static routes BEFORE parameterized routes
@router.get("/recent")
async def get_recent_investigations(
    limit: int = Query(default=3, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    items = await svc.get_recent(limit=limit)
    return success_response(data={"items": items})


@router.get("/stats")
async def investigation_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    stats = await svc.get_stats()
    return success_response(data=stats)


# Parameterized routes AFTER static routes
@router.get("/{investigation_id}")
async def get_investigation(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        inv = await store_get("investigations", investigation_id)
        if not inv:
            return success_response(message="Investigation not found")
        return success_response(data=inv)
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


@router.put("/{investigation_id}/save")
async def toggle_save(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.save_investigation(investigation_id)
    if not result:
        return success_response(message="Investigation not found")
    return success_response(data=result, message=f"Investigation {'saved' if result['status'] == 'saved' else 'resumed'}")
