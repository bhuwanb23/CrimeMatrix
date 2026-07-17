import json
from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

RANK_PROMPT = """You are a search relevance judge. Score each result 0-10 based on relevance to the query.
Return ONLY a JSON array of integers, one per result, in order.

Query: {query}

Results:
{results}

Scores (one integer per result, 0-10):"""


class ResultRanking:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model

    async def rerank(self, query: str, results: list, top_k: int = None) -> list:
        if not results:
            return []

        if len(results) <= 1:
            return results

        results_text = "\n".join([
            f"[{i+1}] {r.get('content', '')[:200]}" for i, r in enumerate(results)
        ])

        try:
            provider = provider_registry.get(self.provider_name)
            prompt = RANK_PROMPT.format(query=query, results=results_text)
            response = await provider.chat(
                [{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            scores = json.loads(response)

            if isinstance(scores, list) and len(scores) == len(results):
                for i, score in enumerate(scores):
                    results[i]["llm_score"] = int(score)
                results.sort(key=lambda x: x.get("llm_score", 0), reverse=True)
                logger.info("reranked", query=query[:50], results=len(results))
        except Exception as e:
            logger.warning("rerank_error", error=str(e))

        if top_k:
            results = results[:top_k]
        return results
