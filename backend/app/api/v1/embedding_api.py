from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.embeddings.persistence import VectorPersistence
from app.core.response import success_response
from fastapi import Query

router = APIRouter()


class EmbeddingSaveRequest(BaseModel):
    domain: str
    item_id: str
    content: str
    vector: list
    metadata: Optional[dict] = None
    source: str = "unknown"


@router.post("/save")
async def save_embedding(data: EmbeddingSaveRequest, db: AsyncSession = Depends(get_db)):
    persistence = VectorPersistence(db)
    doc_id = await persistence.save_embedding(
        data.domain, data.item_id, data.content, data.vector, data.metadata, data.source
    )
    return success_response(data={"doc_id": doc_id})


@router.get("/load")
async def load_embeddings(domain: str = None, db: AsyncSession = Depends(get_db)):
    persistence = VectorPersistence(db)
    if domain:
        chunks = await persistence.get_chunks_by_domain(domain)
    else:
        chunks = await persistence.get_all_chunks()
    return success_response(data=chunks)


@router.delete("/{doc_id}")
async def delete_embedding(doc_id: int, db: AsyncSession = Depends(get_db)):
    persistence = VectorPersistence(db)
    deleted = await persistence.delete_document(doc_id)
    return success_response(message="Deleted" if deleted else "Not found")


@router.get("/count")
async def count_embeddings(domain: str = None, db: AsyncSession = Depends(get_db)):
    persistence = VectorPersistence(db)
    count = await persistence.count(domain)
    return success_response(data={"count": count})
