import json
from typing import Dict, List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.embeddings.models import EmbeddingDocument, EmbeddingChunk
from datetime import datetime
import structlog

logger = structlog.get_logger()


class VectorPersistence:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_document(self, domain: str, title: str, content: str,
                             metadata: dict = None, source: str = "unknown") -> int:
        doc = EmbeddingDocument(
            domain=domain, title=title, content=content,
            metadata_json=json.dumps(metadata or {}), source=source,
        )
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc.id

    async def save_chunk(self, document_id: int, chunk_index: int, content: str,
                          vector: list, metadata: dict = None) -> int:
        chunk = EmbeddingChunk(
            document_id=document_id, chunk_index=chunk_index, content=content,
            vector_json=json.dumps(vector), metadata_json=json.dumps(metadata or {}),
        )
        self.db.add(chunk)
        await self.db.commit()
        await self.db.refresh(chunk)
        return chunk.id

    async def save_embedding(self, domain: str, item_id: str, content: str,
                              vector: list, metadata: dict = None, source: str = "unknown") -> int:
        doc_id = await self.save_document(domain, item_id, content, metadata, source)
        await self.save_chunk(doc_id, 0, content, vector, metadata)
        return doc_id

    async def update_embedding(self, doc_id: int, content: str = None, vector: list = None,
                                metadata: dict = None, source: str = None):
        doc = (await self.db.execute(
            select(EmbeddingDocument).where(EmbeddingDocument.id == doc_id)
        )).scalar_one_or_none()
        if doc:
            if content is not None:
                doc.content = content
            if metadata is not None:
                doc.metadata_json = json.dumps(metadata)
            if source is not None:
                doc.source = source
            doc.updated_at = datetime.now()

            if vector is not None:
                chunk = (await self.db.execute(
                    select(EmbeddingChunk).where(EmbeddingChunk.document_id == doc_id)
                )).scalars().first()
                if chunk:
                    chunk.vector_json = json.dumps(vector)
                    chunk.updated_at = datetime.now()

            await self.db.commit()

    async def get_document(self, doc_id: int) -> Optional[Dict]:
        result = await self.db.execute(
            select(EmbeddingDocument).where(EmbeddingDocument.id == doc_id)
        )
        doc = result.scalar_one_or_none()
        if doc:
            return {
                "id": doc.id, "domain": doc.domain, "title": doc.title,
                "content": doc.content, "source": doc.source,
                "metadata": json.loads(doc.metadata_json) if doc.metadata_json else {},
                "created_at": str(doc.created_at) if doc.created_at else None,
                "updated_at": str(doc.updated_at) if doc.updated_at else None,
            }
        return None

    async def get_chunks_by_domain(self, domain: str) -> List[Dict]:
        result = await self.db.execute(
            select(EmbeddingChunk, EmbeddingDocument).join(
                EmbeddingDocument, EmbeddingChunk.document_id == EmbeddingDocument.id
            ).where(EmbeddingDocument.domain == domain)
        )
        chunks = []
        for chunk, doc in result.all():
            chunks.append({
                "chunk_id": chunk.id, "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index, "content": chunk.content,
                "vector": json.loads(chunk.vector_json),
                "metadata": json.loads(chunk.metadata_json) if chunk.metadata_json else {},
                "domain": doc.domain, "title": doc.title, "source": doc.source,
            })
        return chunks

    async def get_all_chunks(self) -> List[Dict]:
        result = await self.db.execute(
            select(EmbeddingChunk, EmbeddingDocument).join(
                EmbeddingDocument, EmbeddingChunk.document_id == EmbeddingDocument.id
            )
        )
        chunks = []
        for chunk, doc in result.all():
            chunks.append({
                "chunk_id": chunk.id, "document_id": chunk.document_id,
                "content": chunk.content,
                "vector": json.loads(chunk.vector_json),
                "metadata": json.loads(chunk.metadata_json) if chunk.metadata_json else {},
                "domain": doc.domain, "source": doc.source,
            })
        return chunks

    async def delete_document(self, doc_id: int) -> bool:
        await self.db.execute(delete(EmbeddingChunk).where(EmbeddingChunk.document_id == doc_id))
        result = await self.db.execute(delete(EmbeddingDocument).where(EmbeddingDocument.id == doc_id))
        await self.db.commit()
        return result.rowcount > 0

    async def count(self, domain: str = None) -> int:
        if domain:
            result = await self.db.execute(
                select(EmbeddingDocument).where(EmbeddingDocument.domain == domain)
            )
        else:
            result = await self.db.execute(select(EmbeddingDocument))
        return len(result.scalars().all())

    async def clear(self, domain: str = None):
        if domain:
            docs = await self.db.execute(
                select(EmbeddingDocument.id).where(EmbeddingDocument.domain == domain)
            )
            doc_ids = [d[0] for d in docs.all()]
            for doc_id in doc_ids:
                await self.db.execute(delete(EmbeddingChunk).where(EmbeddingChunk.document_id == doc_id))
            await self.db.execute(delete(EmbeddingDocument).where(EmbeddingDocument.domain == domain))
        else:
            await self.db.execute(delete(EmbeddingChunk))
            await self.db.execute(delete(EmbeddingDocument))
        await self.db.commit()
