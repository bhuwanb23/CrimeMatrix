import pytest
from rag.document import Document, DocumentLoader
from rag.chunker import TextChunker
from rag.embeddings import EmbeddingGenerator
from rag.vector_store import VectorStore
from rag.retriever import Retriever
from rag.context_builder import RAGContextBuilder
from rag.citations import CitationManager
from rag.pipeline import RAGPipeline


class TestDocument:
    def test_create(self):
        doc = Document(doc_id="d1", content="Test content", doc_type="fir")
        assert doc.doc_id == "d1"
        assert doc.content == "Test content"

    def test_to_dict(self):
        doc = Document(doc_id="d1", content="Test", doc_type="note", metadata={"key": "val"})
        d = doc.to_dict()
        assert d["doc_id"] == "d1"
        assert d["metadata"]["key"] == "val"


class TestTextChunker:
    def test_small_doc_no_split(self):
        chunker = TextChunker(chunk_size=1000)
        doc = Document("d1", "Short text", "fir")
        chunks = chunker.chunk(doc)
        assert len(chunks) == 1
        assert chunks[0]["content"] == "Short text"

    def test_large_doc_splits(self):
        chunker = TextChunker(chunk_size=50, chunk_overlap=10)
        long_text = "word " * 200
        doc = Document("d1", long_text, "note")
        chunks = chunker.chunk(doc)
        assert len(chunks) > 1

    def test_chunk_metadata(self):
        chunker = TextChunker(chunk_size=1000)
        doc = Document("d1", "text", "fir", metadata={"status": "open"})
        chunks = chunker.chunk(doc)
        assert chunks[0]["doc_id"] == "d1"
        assert chunks[0]["metadata"]["status"] == "open"

    def test_chunk_all(self):
        chunker = TextChunker(chunk_size=1000)
        docs = [
            Document("d1", "Content one", "fir"),
            Document("d2", "Content two", "note"),
        ]
        chunks = chunker.chunk_all(docs)
        assert len(chunks) == 2


class TestEmbeddings:
    def test_fit_and_embed(self):
        emb = EmbeddingGenerator()
        texts = ["crime in bengaluru", "theft case filed", "murder investigation"]
        vectors = emb.embed(texts)
        assert vectors.shape[0] == 3
        assert vectors.shape[1] > 0

    def test_cosine_similarity(self):
        emb = EmbeddingGenerator()
        texts = ["crime report", "crime investigation", "weather forecast"]
        vectors = emb.embed(texts)
        sim_01 = emb.cosine_similarity(vectors[0], vectors[1])
        sim_02 = emb.cosine_similarity(vectors[0], vectors[2])
        assert sim_01 > sim_02

    def test_embed_single(self):
        emb = EmbeddingGenerator()
        vec = emb.embed_single("test query")
        assert len(vec) > 0


class TestVectorStore:
    def test_add_and_search(self):
        vs = VectorStore()
        chunks = [
            {"chunk_id": "c1", "content": "Theft at MG Road", "doc_type": "fir", "source": "fir/1"},
            {"chunk_id": "c2", "content": "Murder in Koramangala", "doc_type": "fir", "source": "fir/2"},
            {"chunk_id": "c3", "content": "Robbery near railway station", "doc_type": "note", "source": "note/1"},
        ]
        vs.add_chunks(chunks)
        results = vs.search("theft robbery", top_k=2)
        assert len(results) > 0
        assert "score" in results[0]

    def test_search_by_type(self):
        vs = VectorStore()
        chunks = [
            {"chunk_id": "c1", "content": "Crime report", "doc_type": "fir", "source": "fir/1"},
            {"chunk_id": "c2", "content": "Investigation note", "doc_type": "note", "source": "note/1"},
        ]
        vs.add_chunks(chunks)
        results = vs.search("crime", doc_type="note")
        for r in results:
            assert r["doc_type"] == "note"

    def test_stats(self):
        vs = VectorStore()
        vs.add_chunks([
            {"chunk_id": "c1", "content": "text", "doc_type": "fir"},
            {"chunk_id": "c2", "content": "text", "doc_type": "note"},
        ])
        stats = vs.get_stats()
        assert stats["total_chunks"] == 2
        assert "fir" in stats["doc_types"]

    def test_empty_search(self):
        vs = VectorStore()
        results = vs.search("query")
        assert results == []

    def test_clear(self):
        vs = VectorStore()
        vs.add_chunks([{"chunk_id": "c1", "content": "text", "doc_type": "fir"}])
        vs.clear()
        assert vs.get_stats()["total_chunks"] == 0


class TestRetriever:
    def test_retrieve(self):
        vs = VectorStore()
        chunks = [
            {"chunk_id": "c1", "content": "Theft case in Bangalore", "doc_type": "fir", "source": "fir/1"},
            {"chunk_id": "c2", "content": "Murder case in Delhi", "doc_type": "fir", "source": "fir/2"},
        ]
        vs.add_chunks(chunks)
        retriever = Retriever(vs)
        results = retriever.retrieve("theft bangalore")
        assert len(results) > 0

    def test_retrieve_with_context(self):
        vs = VectorStore()
        vs.add_chunks([
            {"chunk_id": "c1", "content": "Crime report", "doc_type": "fir", "source": "fir/1"},
        ])
        retriever = Retriever(vs)
        result = retriever.retrieve_with_context("crime")
        assert "context" in result
        assert "results" in result


class TestContextBuilder:
    def test_build(self):
        cb = RAGContextBuilder()
        results = [
            {"content": "Theft report", "doc_type": "fir", "source": "fir/1", "score": 0.9},
        ]
        ctx = cb.build("theft", results)
        assert "Theft report" in ctx
        assert "fir" in ctx

    def test_build_empty(self):
        cb = RAGContextBuilder()
        ctx = cb.build("query", [])
        assert "No relevant" in ctx

    def test_build_citations(self):
        cb = RAGContextBuilder()
        results = [
            {"doc_id": "d1", "doc_type": "fir", "source": "fir/1", "score": 0.85, "content": "text"},
        ]
        citations = cb.build_citations(results)
        assert len(citations) == 1
        assert citations[0]["index"] == 1


class TestCitationManager:
    def test_add_and_get(self):
        cm = CitationManager()
        cm.add_citations("s1", "query", [{"index": 1, "source": "fir/1"}])
        cits = cm.get_citations("s1")
        assert len(cits) == 1

    def test_format(self):
        cm = CitationManager()
        citations = [{"index": 1, "doc_type": "fir", "source": "fir/1", "score": 0.9}]
        formatted = cm.format_citations(citations)
        assert "fir" in formatted

    def test_clear(self):
        cm = CitationManager()
        cm.add_citations("s1", "q", [])
        cm.clear("s1")
        assert cm.get_citations("s1") == []


class TestRAGPipeline:
    def test_search_without_index(self):
        pipeline = RAGPipeline()
        result = pipeline.search("query")
        assert result["count"] == 0

    def test_stats(self):
        pipeline = RAGPipeline()
        stats = pipeline.get_stats()
        assert "total_chunks" in stats

    def test_is_indexed_default(self):
        pipeline = RAGPipeline()
        assert pipeline.is_indexed() is False
