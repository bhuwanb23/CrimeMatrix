from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.victim_repo import VictimRepository
from app.services.victim_service import VictimService
from app.schemas.victim import VictimCreate, VictimResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response
from app.db.phase1_store import store_create, store_get, store_list, using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return VictimService(VictimRepository(db))


@router.get("/", )
async def list_victims(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("victims", page=page, page_size=page_size)
        data["items"] = [
            {
                "id": i.get("id"),
                "title": i.get("name") or "",
                "name": i.get("name"),
                "case_id": i.get("case_id"),
                "status": "active",
            }
            for i in data["items"]
        ]
        return {"success": True, "data": data, "message": "Success"}
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{victim_id}")
async def get_victim(victim_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        victim = await store_get("victims", victim_id)
        if not victim:
            return success_response(message="Victim not found")
        return success_response(data=victim)
    svc = get_service(db)
    victim = await svc.get_by_id(victim_id)
    if not victim:
        return success_response(message="Victim not found")
    return success_response(data=VictimResponse.model_validate(victim).model_dump())


@router.post("/")
async def create_victim(data: VictimCreate, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        payload = data.model_dump()
        # Catalyst victims require case_id + name
        if not payload.get("case_id"):
            cases = await store_list("cases", page=1, page_size=1)
            if cases["items"]:
                payload["case_id"] = cases["items"][0].get("id")
        payload.setdefault("name", payload.get("statement") or f"Victim-{payload.get('case_id') or 'unknown'}")
        # Drop SQLAlchemy-only fields Catalyst schema doesn't have
        for drop in ("person_id", "statement", "injury_type"):
            payload.pop(drop, None)
        try:
            victim = await store_create("victims", payload)
            return success_response(data=victim, message="Victim created")
        except Exception as e:
            return success_response(message=str(e)[:200])
    svc = get_service(db)
    victim = await svc.create(data.model_dump())
    return success_response(data=VictimResponse.model_validate(victim).model_dump(), message="Victim created")


@router.delete("/{victim_id}")
async def delete_victim(victim_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(victim_id)
    return success_response(message="Victim deleted" if deleted else "Victim not found")
