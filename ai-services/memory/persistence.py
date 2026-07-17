import httpx
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class MemoryPersistence:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    async def save_session(self, session_id: str, title: str = None, user_id: int = None,
                            model_used: str = None) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                data = {"session_id": session_id}
                if title:
                    data["title"] = title
                if user_id:
                    data["user_id"] = user_id
                if model_used:
                    data["model_used"] = model_used
                resp = await client.post(f"{self.backend_url}/api/v1/memory/sessions", json=data, timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {})
        except Exception as e:
            logger.warning("save_session_error", error=str(e))
        return None

    async def load_session(self, session_id: str) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/memory/sessions/{session_id}", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data")
        except Exception as e:
            logger.warning("load_session_error", error=str(e))
        return None

    async def save_message(self, session_id: str, role: str, content: str, tokens_used: int = 0) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                data = {"session_id": session_id, "role": role, "content": content, "tokens_used": tokens_used}
                resp = await client.post(f"{self.backend_url}/api/v1/memory/messages", json=data, timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("save_message_error", error=str(e))
        return False

    async def load_messages(self, session_id: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/memory/messages/{session_id}", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", [])
        except Exception as e:
            logger.warning("load_messages_error", error=str(e))
        return []

    async def save_summary(self, session_id: str, summary: str, key: str = "compressed") -> bool:
        try:
            async with httpx.AsyncClient() as client:
                data = {"session_id": session_id, "key": key, "value": summary, "summary": summary}
                resp = await client.post(f"{self.backend_url}/api/v1/memory/summary", json=data, timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("save_summary_error", error=str(e))
        return False

    async def load_summary(self, session_id: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/memory/summary/{session_id}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data")
                    return data.get("value") if data else None
        except Exception as e:
            logger.warning("load_summary_error", error=str(e))
        return None

    async def delete_session(self, session_id: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(f"{self.backend_url}/api/v1/memory/sessions/{session_id}", timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("delete_session_error", error=str(e))
        return False

    async def list_sessions(self) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/memory/sessions", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", [])
        except Exception as e:
            logger.warning("list_sessions_error", error=str(e))
        return []
