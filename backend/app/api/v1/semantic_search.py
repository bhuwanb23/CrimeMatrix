from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import httpx
from app.core.response import success_response
from fastapi import APIRouter

router = APIRouter()

AI_SERVICES_URL = "http://localhost:8002"
BACKEND_URL = "http://localhost:8000"


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    doc_type: Optional[str] = None


@router.post("")
async def semantic_search(data: SemanticSearchRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{AI_SERVICES_URL}/api/ai/search/intelligent",
                json={"query": data.query, "top_k": data.top_k, "doc_type": data.doc_type},
                timeout=30.0,
            )
            if resp.status_code == 200:
                return success_response(data=resp.json().get("data", {}))
    except Exception as e:
        pass

    # Fallback to keyword search
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BACKEND_URL}/api/v1/search/",
                json={"query": data.query, "page": 1, "page_size": data.top_k},
                timeout=10.0,
            )
            if resp.status_code == 200:
                return success_response(data=resp.json().get("data", {}))
    except Exception:
        pass

    return success_response(data={"results": [], "total": 0, "note": "Semantic search not available"})


@router.post("/index")
async def index_documents():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{AI_SERVICES_URL}/api/ai/rag/index", timeout=30.0)
            if resp.status_code == 200:
                return success_response(data=resp.json().get("data", {}))
    except Exception as e:
        return success_response(data={"error": str(e)})
    return success_response(data={"error": "Failed to index"})


@router.get("/stats")
async def semantic_stats():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{AI_SERVICES_URL}/api/ai/search/stats", timeout=10.0)
            if resp.status_code == 200:
                return success_response(data=resp.json().get("data", {}))
    except Exception:
        pass
    return success_response(data={"semantic": {"total_chunks": 0}})
