from typing import List, Dict
from rag.vector_store import VectorStore
from rag.document import DocumentLoader
from rag.chunker import TextChunker
import structlog

logger = structlog.get_logger()


class Retriever:
    def __init__(self, vector_store: VectorStore, loader: DocumentLoader = None,
                 chunker: TextChunker = None):
        self.vector_store = vector_store
        self.loader = loader or DocumentLoader()
        self.chunker = chunker or TextChunker()

    async def index_documents(self, limit_per_type: int = 50) -> int:
        docs = await self.loader.load_all(limit_per_type)
        if not docs:
            return 0
        chunks = self.chunker.chunk_all(docs)
        self.vector_store.add_chunks(chunks)
        return len(chunks)

    def retrieve(self, query: str, top_k: int = 5, doc_type: str = None) -> List[dict]:
        return self.vector_store.search(query, top_k, doc_type)

    def retrieve_with_context(self, query: str, top_k: int = 5) -> dict:
        results = self.retrieve(query, top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results),
            "sources": list(set(r.get("source", "") for r in results if r.get("source"))),
        }
