from typing import Dict, List, Any, Optional
from datetime import datetime
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class Document:
    def __init__(self, doc_id: str, content: str, doc_type: str,
                 metadata: dict = None, source: str = ""):
        self.doc_id = doc_id
        self.content = content
        self.doc_type = doc_type
        self.metadata = metadata or {}
        self.source = source
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "content": self.content,
            "doc_type": self.doc_type,
            "metadata": self.metadata,
            "source": self.source,
        }


class DocumentLoader:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    async def load_firs(self, limit: int = 50) -> List[Document]:
        docs = []
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/crimes/", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {}).get("items", resp.json().get("data", []))
                    if isinstance(data, list):
                        for item in data[:limit]:
                            content = f"FIR: {item.get('title', '')}\n{item.get('description', '')}"
                            docs.append(Document(
                                doc_id=f"fir_{item.get('id', 0)}",
                                content=content,
                                doc_type="fir",
                                metadata={"status": item.get("status"), "priority": item.get("priority")},
                                source=f"crime/{item.get('id')}",
                            ))
        except Exception as e:
            logger.warning("load_firs_error", error=str(e))
        return docs

    async def load_investigation_notes(self, limit: int = 50) -> List[Document]:
        docs = []
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/notes/", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {}).get("items", resp.json().get("data", []))
                    if isinstance(data, list):
                        for item in data[:limit]:
                            content = f"Investigation Note: {item.get('content', '')}"
                            docs.append(Document(
                                doc_id=f"note_{item.get('id', 0)}",
                                content=content,
                                doc_type="note",
                                metadata={"investigation_id": item.get("investigation_id")},
                                source=f"note/{item.get('id')}",
                            ))
        except Exception as e:
            logger.warning("load_notes_error", error=str(e))
        return docs

    async def load_all(self, limit_per_type: int = 50) -> List[Document]:
        firs = await self.load_firs(limit_per_type)
        notes = await self.load_investigation_notes(limit_per_type)
        logger.info("documents_loaded", firs=len(firs), notes=len(notes))
        return firs + notes
