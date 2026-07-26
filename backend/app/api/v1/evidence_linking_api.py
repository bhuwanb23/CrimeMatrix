from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.evidence_linking_service import EvidenceLinkingService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return EvidenceLinkingService(db)


async def _phase1_links():
    from app.db.phase1_aggregations import derive_evidence_links, fetch_all_safe

    return derive_evidence_links(
        await fetch_all_safe("evidence"),
        await fetch_all_safe("crimes"),
    )


@router.get("/stats")
async def evidence_linking_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import evidence_linking_stats as build_stats

        return success_response(data=build_stats(await _phase1_links()))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/links")
async def list_links(
    link_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        links = await _phase1_links()
        if link_type:
            links = [link for link in links if link["link_type"] == link_type]
        return success_response(data={"items": links, "total": len(links)})
    svc = get_service(db)
    links = await svc.get_links(link_type)
    return success_response(data={"items": links, "total": len(links)})


@router.get("/relationships")
async def list_relationships(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import evidence_relationships

        relationships = evidence_relationships(await _phase1_links())
        return success_response(data={"items": relationships, "total": len(relationships)})
    svc = get_service(db)
    relationships = await svc.get_relationships()
    return success_response(data={"items": relationships, "total": len(relationships)})


@router.get("/links/{link_id}")
async def get_link(link_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        match = next((link for link in await _phase1_links() if str(link["id"]) == str(link_id)), None)
        if not match:
            return success_response(message="Link not found")
        return success_response(data=match)
    if not link_id.isdigit():
        return success_response(message="Link not found")
    svc = get_service(db)
    link = await svc.get_link(int(link_id))
    if not link:
        return success_response(message="Link not found")
    return success_response(data=link)


@router.post("/detect")
async def detect_links(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        links = await _phase1_links()
        return success_response(
            data={"links_found": len(links), "items": links},
            message="Evidence linking complete",
        )
    try:
        svc = get_service(db)
        result = await svc.detect_links()
        return success_response(data=result, message="Evidence linking complete")
    except Exception as e:
        return success_response(
            data={"links_found": 0},
            message=str(e)[:200],
        )
