from typing import List, Optional
from rag.vector_store import VectorStore
import structlog

logger = structlog.get_logger()


class SemanticSearch:
    def __init__(self, vector_store: VectorStore = None):
        self.vector_store = vector_store or VectorStore()

    def search(self, query: str, top_k: int = 5, doc_type: str = None) -> List[dict]:
        return self.vector_store.search(query, top_k, doc_type)

    def index(self, chunks: List[dict]):
        self.vector_store.add_chunks(chunks)

    def get_stats(self) -> dict:
        return self.vector_store.get_stats()
