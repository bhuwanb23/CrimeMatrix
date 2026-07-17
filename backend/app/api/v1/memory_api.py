from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import select, delete
from app.db.session import get_db
from app.models.chat import ChatSession, ChatMessage, ConversationMemory
from app.core.response import success_response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter()


class SessionCreate(BaseModel):
    session_id: str
    title: Optional[str] = None
    user_id: Optional[int] = None
    model_used: Optional[str] = None


class MessageCreate(BaseModel):
    session_id: str
    role: str
    content: str
    tokens_used: int = 0


class SummaryCreate(BaseModel):
    session_id: str
    key: str = "compressed"
    value: str
    summary: Optional[str] = None


@router.post("/sessions")
async def create_session(data: SessionCreate, db: AsyncSession = Depends(get_db)):
    existing = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == data.session_id)
    )).scalar_one_or_none()

    if existing:
        return success_response(data={"id": existing.id, "session_id": existing.session_id})

    session = ChatSession(
        session_id=data.session_id,
        user_id=data.user_id,
        title=data.title,
        model_used=data.model_used,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return success_response(data={"id": session.id, "session_id": session.session_id})


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if not session:
        return success_response(data=None)
    return success_response(data={
        "id": session.id, "session_id": session.session_id,
        "title": session.title, "user_id": session.user_id,
        "model_used": session.model_used, "status": session.status,
    })


@router.get("/sessions")
async def list_sessions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChatSession).order_by(ChatSession.created_at.desc()))
    sessions = [
        {"id": s.id, "session_id": s.session_id, "title": s.title, "status": s.status}
        for s in result.scalars().all()
    ]
    return success_response(data=sessions)


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if session:
        await db.execute(delete(ChatMessage).where(ChatMessage.session_id == session_id))
        await db.execute(delete(ConversationMemory).where(ConversationMemory.session_id == session_id))
        await db.delete(session)
        await db.commit()
    return success_response(message="Deleted")


@router.post("/messages")
async def save_message(data: MessageCreate, db: AsyncSession = Depends(get_db)):
    msg = ChatMessage(
        session_id=data.session_id,
        role=data.role,
        content=data.content,
        tokens_used=data.tokens_used,
    )
    db.add(msg)
    await db.commit()
    return success_response(data={"id": msg.id})


@router.get("/messages/{session_id}")
async def load_messages(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)
    )
    messages = [
        {"id": m.id, "role": m.role, "content": m.content, "tokens_used": m.tokens_used}
        for m in result.scalars().all()
    ]
    return success_response(data=messages)


@router.post("/summary")
async def save_summary(data: SummaryCreate, db: AsyncSession = Depends(get_db)):
    existing = (await db.execute(
        select(ConversationMemory).where(
            ConversationMemory.session_id == data.session_id,
            ConversationMemory.key == data.key,
        )
    )).scalar_one_or_none()

    if existing:
        existing.value = data.value
        existing.summary = data.summary
    else:
        mem = ConversationMemory(
            session_id=data.session_id,
            key=data.key,
            value=data.value,
            summary=data.summary,
        )
        db.add(mem)
    await db.commit()
    return success_response(message="Summary saved")


@router.get("/summary/{session_id}")
async def load_summary(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ConversationMemory).where(ConversationMemory.session_id == session_id)
    )
    mem = result.scalars().first()
    if mem:
        return success_response(data={"key": mem.key, "value": mem.value, "summary": mem.summary})
    return success_response(data=None)
