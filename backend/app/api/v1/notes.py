from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse
from app.core.response import success_response

router = APIRouter()


@router.get("/investigation/{investigation_id}")
async def list_notes(investigation_id: int, db: AsyncSession = Depends(get_db)):
    repo = NoteRepository(db)
    notes = await repo.get_by_investigation(investigation_id)
    return success_response(data=[NoteResponse.model_validate(n).model_dump() for n in notes])


@router.post("/")
async def create_note(data: NoteCreate, db: AsyncSession = Depends(get_db)):
    repo = NoteRepository(db)
    note = await repo.create(data.model_dump())
    return success_response(data=NoteResponse.model_validate(note).model_dump(), message="Note created")


@router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    repo = NoteRepository(db)
    deleted = await repo.delete(note_id)
    return success_response(message="Note deleted" if deleted else "Note not found")
