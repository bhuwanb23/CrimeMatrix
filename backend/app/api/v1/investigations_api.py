from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.investigation_service import InvestigationService
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate, InvestigationResponse, InvestigationListItem
from app.core.response import success_response
from app.db.phase1_store import store_create, store_delete, store_get, store_list, store_update, using_phase1_store

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
    if using_phase1_store():
        data = await store_list("investigations", page=1, page_size=limit)
        return success_response(data={"items": data["items"]})
    svc = get_service(db)
    items = await svc.get_recent(limit=limit)
    return success_response(data={"items": items})


@router.get("/stats")
async def investigation_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("investigations", page=1, page_size=100)
        items = data["items"]
        by_status: dict[str, int] = {}
        for i in items:
            st = str(i.get("status") or "unknown")
            by_status[st] = by_status.get(st, 0) + 1
        return success_response(
            data={"total": data.get("total", len(items)), "by_status": by_status}
        )
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
    if using_phase1_store():
        payload = data.model_dump()
        # tolerate missing district column on live schema
        try:
            inv = await store_create("investigations", payload)
        except Exception:
            payload.pop("district", None)
            inv = await store_create("investigations", payload)
        return success_response(data=inv, message="Investigation created")
    svc = get_service(db)
    inv = await svc.create_investigation(data.model_dump())
    return success_response(data=inv, message="Investigation created")


@router.put("/{investigation_id}")
async def update_investigation(
    investigation_id: int, data: InvestigationUpdate, db: AsyncSession = Depends(get_db)
):
    if using_phase1_store():
        fields = data.model_dump(exclude_unset=True)
        try:
            inv = await store_update("investigations", investigation_id, fields)
        except Exception:
            fields.pop("district", None)
            inv = await store_update("investigations", investigation_id, fields)
        if not inv:
            return success_response(message="Investigation not found")
        return success_response(data=inv, message="Investigation updated")
    svc = get_service(db)
    inv = await svc.update_investigation(investigation_id, data.model_dump(exclude_unset=True))
    if not inv:
        return success_response(message="Investigation not found")
    return success_response(data=inv, message="Investigation updated")


@router.delete("/{investigation_id}")
async def delete_investigation(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        deleted = await store_delete("investigations", investigation_id)
        return success_response(message="Investigation deleted" if deleted else "Investigation not found")
    svc = get_service(db)
    deleted = await svc.delete_investigation(investigation_id)
    return success_response(message="Investigation deleted" if deleted else "Investigation not found")


@router.put("/{investigation_id}/save")
async def toggle_save(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        inv = await store_get("investigations", investigation_id)
        if not inv:
            return success_response(message="Investigation not found")
        new_status = "saved" if inv.get("status") != "saved" else "active"
        updated = await store_update("investigations", investigation_id, {"status": new_status})
        return success_response(
            data=updated,
            message=f"Investigation {'saved' if new_status == 'saved' else 'resumed'}",
        )
    svc = get_service(db)
    result = await svc.save_investigation(investigation_id)
    if not result:
        return success_response(message="Investigation not found")
    return success_response(data=result, message=f"Investigation {'saved' if result['status'] == 'saved' else 'resumed'}")
