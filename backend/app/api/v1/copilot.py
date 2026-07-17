import httpx
import uuid
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.chat import ChatSession, ChatMessage, ConversationMemory
from app.core.response import success_response
from fastapi import Depends

router = APIRouter()

AI_SERVICES_URL = "http://localhost:8002"


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: str = "default"
    use_tools: bool = True
    source: str = "all"


class SessionCreate(BaseModel):
    title: Optional[str] = None
    user_id: str = "default"


class TitleUpdate(BaseModel):
    title: str


@router.post("/chat")
async def copilot_chat(data: ChatRequest, db: AsyncSession = Depends(get_db)):
    session_id = data.session_id or uuid.uuid4().hex[:12]

    # Ensure session exists in DB
    existing = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if not existing:
        session = ChatSession(session_id=session_id, user_id=int(data.user_id) if data.user_id.isdigit() else None)
        db.add(session)
        await db.commit()

    # Save user message to DB
    user_msg = ChatMessage(session_id=session_id, role="user", content=data.message)
    db.add(user_msg)
    await db.commit()

    # Call AI Services agent
    try:
        async with httpx.AsyncClient() as client:
            ai_response = await client.post(
                f"{AI_SERVICES_URL}/api/ai/chat",
                json={
                    "message": data.message,
                    "session_id": session_id,
                    "user_id": data.user_id,
                    "use_tools": data.use_tools,
                },
                timeout=120.0,
            )
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                response_text = ai_data.get("data", {}).get("response", "I could not process that request.")
                reasoning_trace = ai_data.get("data", {}).get("reasoning_trace", [])
                steps = ai_data.get("data", {}).get("steps", 0)
            else:
                response_text = "AI service temporarily unavailable. Please try again."
                reasoning_trace = []
                steps = 0
    except Exception as e:
        response_text = f"Connection error: {str(e)[:100]}"
        reasoning_trace = []
        steps = 0

    # Save assistant message to DB
    assistant_msg = ChatMessage(session_id=session_id, role="assistant", content=response_text)
    db.add(assistant_msg)

    # Auto-generate title from first message
    if existing and not existing.title:
        existing.title = data.message[:100]

    await db.commit()

    return success_response(data={
        "session_id": session_id,
        "response": response_text,
        "reasoning_trace": reasoning_trace,
        "steps": steps,
    })


@router.post("/chat/stream")
async def copilot_chat_stream(data: ChatRequest, db: AsyncSession = Depends(get_db)):
    session_id = data.session_id or uuid.uuid4().hex[:12]

    # Ensure session exists
    existing = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if not existing:
        session = ChatSession(session_id=session_id, user_id=int(data.user_id) if data.user_id.isdigit() else None)
        db.add(session)
        await db.commit()

    # Save user message
    user_msg = ChatMessage(session_id=session_id, role="user", content=data.message)
    db.add(user_msg)
    await db.commit()

    async def generate():
        full_response = []
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{AI_SERVICES_URL}/api/ai/chat/stream",
                    json={
                        "message": data.message,
                        "session_id": session_id,
                        "user_id": data.user_id,
                        "use_tools": data.use_tools,
                    },
                    timeout=120.0,
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk_data = line[6:]
                            if chunk_data.strip() == "[DONE]":
                                break
                            try:
                                chunk = json.loads(chunk_data)
                                if chunk.get("type") == "message" and chunk.get("content"):
                                    full_response.append(chunk["content"])
                                    yield f"data: {json.dumps({'content': chunk['content'], 'done': False})}\n\n"
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            yield f"data: {json.dumps({'content': f'Error: {str(e)[:100]}', 'done': True})}\n\n"
            return

        # Save assistant response to DB
        final_response = "".join(full_response)
        assistant_msg = ChatMessage(session_id=session_id, role="assistant", content=final_response)
        db.add(assistant_msg)
        await db.commit()

        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/sessions")
async def list_sessions(user_id: str = "default", db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatSession).where(ChatSession.user_id == int(user_id) if user_id.isdigit() else True)
        .order_by(ChatSession.created_at.desc())
    )
    sessions = [
        {
            "id": s.id,
            "session_id": s.session_id,
            "title": s.title or "New Conversation",
            "status": s.status,
            "created_at": str(s.created_at) if s.created_at else None,
        }
        for s in result.scalars().all()
    ]
    return success_response(data=sessions)


@router.post("/sessions")
async def create_session(data: SessionCreate, db: AsyncSession = Depends(get_db)):
    session_id = uuid.uuid4().hex[:12]
    session = ChatSession(
        session_id=session_id,
        user_id=int(data.user_id) if data.user_id.isdigit() else None,
        title=data.title,
    )
    db.add(session)
    await db.commit()
    return success_response(data={"session_id": session_id, "title": data.title})


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages_result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)
    )
    messages = [
        {"id": m.id, "role": m.role, "content": m.content, "created_at": str(m.created_at) if m.created_at else None}
        for m in messages_result.scalars().all()
    ]

    return success_response(data={
        "session_id": session.session_id,
        "title": session.title,
        "messages": messages,
    })


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if session:
        await db.execute(select(ChatMessage).where(ChatMessage.session_id == session_id))
        from sqlalchemy import delete
        await db.execute(delete(ChatMessage).where(ChatMessage.session_id == session_id))
        await db.execute(delete(ConversationMemory).where(ConversationMemory.session_id == session_id))
        await db.delete(session)
        await db.commit()
    return success_response(message="Deleted")


@router.put("/sessions/{session_id}/title")
async def update_title(session_id: str, data: TitleUpdate, db: AsyncSession = Depends(get_db)):
    session = (await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )).scalar_one_or_none()
    if session:
        session.title = data.title
        await db.commit()
    return success_response(message="Updated")
