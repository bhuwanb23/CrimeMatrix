import pytest
from unittest.mock import AsyncMock, patch
from search.semantic import SemanticSearch
from search.hybrid import HybridSearch
from search.similar import SimilarCaseSearch
from search.cross_district import CrossDistrictSearch
from search.expansion import QueryExpansion
from search.rewriting import QueryRewriting
from search.ranking import ResultRanking
from search.engine import SearchEngine
from rag.vector_store import VectorStore


def _make_vector_store():
    vs = VectorStore()
    chunks = [
        {"chunk_id": "c1", "content": "Theft at MG Road Bengaluru", "doc_type": "fir", "source": "fir/1"},
        {"chunk_id": "c2", "content": "Murder in Koramangala", "doc_type": "fir", "source": "fir/2"},
        {"chunk_id": "c3", "content": "Robbery near railway station", "doc_type": "note", "source": "note/1"},
        {"chunk_id": "c4", "content": "Theft suspect identified in Bangalore South", "doc_type": "note", "source": "note/2"},
        {"chunk_id": "c5", "content": "Vehicle stolen from parking lot", "doc_type": "fir", "source": "fir/3"},
    ]
    vs.add_chunks(chunks)
    return vs


class TestSemanticSearch:
    def test_search(self):
        ss = SemanticSearch(_make_vector_store())
        results = ss.search("theft bengaluru", top_k=3)
        assert len(results) > 0
        assert results[0]["score"] > 0

    def test_search_by_type(self):
        ss = SemanticSearch(_make_vector_store())
        results = ss.search("crime", doc_type="note")
        for r in results:
            assert r["doc_type"] == "note"

    def test_stats(self):
        ss = SemanticSearch(_make_vector_store())
        stats = ss.get_stats()
        assert stats["total_chunks"] == 5


class TestHybridSearch:
    def test_hybrid_search(self):
        hs = HybridSearch(_make_vector_store())
        results = hs.search("theft stealing", top_k=3)
        assert len(results) > 0
        assert "keyword_score" in results[0]
        assert "semantic_score" in results[0]

    def test_hybrid_scores_combined(self):
        hs = HybridSearch(_make_vector_store(), weight_keyword=0.5, weight_semantic=0.5)
        results = hs.search("theft", top_k=5)
        for r in results:
            expected = 0.5 * r["keyword_score"] + 0.5 * r["semantic_score"]
            assert abs(r["score"] - expected) < 0.01

    def test_empty_search(self):
        hs = HybridSearch(VectorStore())
        results = hs.search("query")
        assert results == []


class TestQueryExpansion:
    @pytest.mark.asyncio
    async def test_expand(self):
        with patch("search.expansion.provider_registry") as mock_reg:
            mock_provider = AsyncMock()
            mock_provider.chat.return_value = '["theft", "larceny", "stealing", "burglary"]'
            mock_reg.get.return_value = mock_provider
            exp = QueryExpansion()
            terms = await exp.expand("theft")
            assert "theft" in terms
            assert len(terms) >= 2

    @pytest.mark.asyncio
    async def test_expand_cached(self):
        with patch("search.expansion.provider_registry") as mock_reg:
            mock_provider = AsyncMock()
            mock_provider.chat.return_value = '["test", "query"]'
            mock_reg.get.return_value = mock_provider
            exp = QueryExpansion()
            r1 = await exp.expand("test")
            r2 = await exp.expand("test")
            assert r1 == r2
            mock_provider.chat.assert_called_once()


class TestQueryRewriting:
    @pytest.mark.asyncio
    async def test_rewrite(self):
        with patch("search.rewriting.provider_registry") as mock_reg:
            mock_provider = AsyncMock()
            mock_provider.chat.return_value = "crime theft Bengaluru"
            mock_reg.get.return_value = mock_provider
            rw = QueryRewriting()
            result = await rw.rewrite("what crimes involving theft happened in Bengaluru?")
            assert result == "crime theft Bengaluru"


class TestResultRanking:
    @pytest.mark.asyncio
    async def test_rerank(self):
        with patch("search.ranking.provider_registry") as mock_reg:
            mock_provider = AsyncMock()
            mock_provider.chat.return_value = "[10, 5, 2]"
            mock_reg.get.return_value = mock_provider
            rr = ResultRanking()
            results = [
                {"content": "Theft at MG Road", "score": 0.8},
                {"content": "Murder case", "score": 0.5},
                {"content": "Weather report", "score": 0.1},
            ]
            reranked = await rr.rerank("theft", results)
            assert reranked[0]["llm_score"] == 10

    @pytest.mark.asyncio
    async def test_rerank_empty(self):
        rr = ResultRanking()
        result = await rr.rerank("query", [])
        assert result == []


class TestSimilarCaseSearch:
    @pytest.mark.asyncio
    async def test_find_similar_no_backend(self):
        scs = SimilarCaseSearch(_make_vector_store(), backend_url="http://localhost:99999")
        results = await scs.find_similar(1)
        assert results == []


class TestCrossDistrictSearch:
    @pytest.mark.asyncio
    async def test_search_no_backend(self):
        cds = CrossDistrictSearch(backend_url="http://localhost:99999")
        result = await cds.search("theft", ["Bengaluru"])
        assert result["total_results"] == 0


class TestSearchEngine:
    def test_stats(self):
        engine = SearchEngine()
        stats = engine.get_stats()
        assert "semantic" in stats

    def test_semantic_index(self):
        engine = SearchEngine()
        chunks = [
            {"chunk_id": "c1", "content": "Test crime", "doc_type": "fir", "source": "fir/1"},
        ]
        engine.semantic.index(chunks)
        results = engine.semantic.search("crime")
        assert len(results) > 0
