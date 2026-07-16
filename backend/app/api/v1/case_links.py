from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.case_link_repo import CaseLinkRepository
from app.schemas.case_link import CaseLinkCreate, CaseLinkResponse
from app.core.response import success_response

router = APIRouter()


@router.get("/investigation/{investigation_id}")
async def list_links(investigation_id: int, db: AsyncSession = Depends(get_db)):
    repo = CaseLinkRepository(db)
    links = await repo.get_by_investigation(investigation_id)
    return success_response(data=[CaseLinkResponse.model_validate(l).model_dump() for l in links])


@router.post("/")
async def create_link(data: CaseLinkCreate, db: AsyncSession = Depends(get_db)):
    repo = CaseLinkRepository(db)
    link = await repo.create(data.model_dump())
    return success_response(data=CaseLinkResponse.model_validate(link).model_dump(), message="Link created")


@router.delete("/{link_id}")
async def delete_link(link_id: int, db: AsyncSession = Depends(get_db)):
    repo = CaseLinkRepository(db)
    deleted = await repo.delete(link_id)
    return success_response(message="Link deleted" if deleted else "Link not found")
