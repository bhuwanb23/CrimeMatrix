from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.evidence_linking_service import EvidenceLinkingService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return EvidenceLinkingService(db)


@router.get("/stats")
async def evidence_linking_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/links")
async def list_links(
    link_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    links = await svc.get_links(link_type)
    return success_response(data={"items": links, "total": len(links)})


@router.get("/links/{link_id}")
async def get_link(link_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    link = await svc.get_link(link_id)
    if not link:
        return success_response(message="Link not found")
    return success_response(data=link)


@router.get("/relationships")
async def list_relationships(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    relationships = await svc.get_relationships()
    return success_response(data={"items": relationships, "total": len(relationships)})


@router.post("/detect")
async def detect_links(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.detect_links()
    return success_response(data=result, message="Evidence linking complete")
