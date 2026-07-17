from rag.vector_store import VectorStore
from rag.retriever import Retriever
from rag.document import DocumentLoader
from rag.chunker import TextChunker
from rag.context_builder import RAGContextBuilder
from rag.citations import CitationManager
import structlog

logger = structlog.get_logger()


class RAGPipeline:
    def __init__(self, backend_url: str = None):
        self.vector_store = VectorStore()
        self.loader = DocumentLoader(backend_url)
        self.chunker = TextChunker()
        self.retriever = Retriever(self.vector_store, self.loader, self.chunker)
        self.context_builder = RAGContextBuilder()
        self.citations = CitationManager()
        self._indexed = False

    async def index(self, limit_per_type: int = 50) -> int:
        count = await self.retriever.index_documents(limit_per_type)
        self._indexed = count > 0
        logger.info("rag_indexed", chunks=count)
        return count

    def search(self, query: str, top_k: int = 5, doc_type: str = None) -> dict:
        results = self.retriever.retrieve(query, top_k, doc_type)
        context = self.context_builder.build(query, results)
        citation_list = self.context_builder.build_citations(results)
        return {
            "query": query,
            "context": context,
            "results": results,
            "citations": citation_list,
            "count": len(results),
        }

    def search_and_cite(self, query: str, session_id: str = "default",
                        top_k: int = 5) -> dict:
        result = self.search(query, top_k)
        self.citations.add_citations(session_id, query, result["citations"])
        return result

    def get_stats(self) -> dict:
        return self.vector_store.get_stats()

    def is_indexed(self) -> bool:
        return self._indexed
