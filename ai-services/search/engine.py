from typing import List, Dict
from search.semantic import SemanticSearch
from search.hybrid import HybridSearch
from search.similar import SimilarCaseSearch
from search.cross_district import CrossDistrictSearch
from search.expansion import QueryExpansion
from search.rewriting import QueryRewriting
from search.ranking import ResultRanking
from rag.context_builder import RAGContextBuilder
import structlog

logger = structlog.get_logger()


class SearchEngine:
    def __init__(self, provider: str = None, model: str = None):
        self.semantic = SemanticSearch()
        self.hybrid = HybridSearch(self.semantic.vector_store)
        self.similar = SimilarCaseSearch(self.semantic.vector_store)
        self.cross_district = CrossDistrictSearch()
        self.expansion = QueryExpansion(provider, model)
        self.rewriting = QueryRewriting(provider, model)
        self.ranking = ResultRanking(provider, model)
        self.context_builder = RAGContextBuilder()

    async def intelligent_search(self, query: str, top_k: int = 5,
                                  doc_type: str = None,
                                  use_rewrite: bool = True,
                                  use_expand: bool = True,
                                  use_rerank: bool = True) -> dict:
        logger.info("intelligent_search_start", query=query)

        rewritten = query
        if use_rewrite:
            rewritten = await self.rewriting.rewrite(query)
            logger.info("query_rewritten", original=query, rewritten=rewritten)

        expanded_terms = [rewritten]
        if use_expand:
            expanded_terms = await self.expansion.expand(rewritten)
            logger.info("query_expanded", terms=expanded_terms)

        search_query = " ".join(expanded_terms)
        results = self.hybrid.search(search_query, top_k=top_k * 2, doc_type=doc_type)

        if use_rerank and results:
            results = await self.ranking.rerank(query, results, top_k=top_k)
        else:
            results = results[:top_k]

        context = self.context_builder.build(query, results)
        citations = self.context_builder.build_citations(results)

        return {
            "original_query": query,
            "rewritten_query": rewritten,
            "expanded_terms": expanded_terms,
            "results": results,
            "context": context,
            "citations": citations,
            "count": len(results),
        }

    async def find_similar(self, case_id: int, top_k: int = 5) -> dict:
        results = await self.similar.find_similar(case_id, top_k)
        return {"case_id": case_id, "similar_cases": results, "count": len(results)}

    async def cross_district_search(self, query: str, districts: List[str] = None,
                                     top_k: int = 10) -> dict:
        return await self.cross_district.search(query, districts, top_k)

    async def expand_query(self, query: str) -> dict:
        terms = await self.expansion.expand(query)
        return {"original": query, "expanded": terms}

    async def rewrite_query(self, query: str) -> dict:
        rewritten = await self.rewriting.rewrite(query)
        return {"original": query, "rewritten": rewritten}

    async def rerank_results(self, query: str, results: list) -> dict:
        reranked = await self.ranking.rerank(query, results)
        return {"query": query, "results": reranked, "count": len(reranked)}

    def get_stats(self) -> dict:
        return {
            "semantic": self.semantic.get_stats(),
        }
