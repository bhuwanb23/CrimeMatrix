import json
from core.provider import registry as provider_registry
from storage.cache_provider import MemoryCacheProvider
import structlog

logger = structlog.get_logger()

EXPANSION_PROMPT = """Expand the following search query with 3-5 related terms, synonyms, or broader concepts.
Return ONLY a JSON array of strings. Include the original term.

Example: "theft" → ["theft", "larceny", "shoplifting", "stealing", "burglary"]

Query: {query}
Expanded:"""


class QueryExpansion:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model
        self._cache = MemoryCacheProvider(max_size=5000)

    async def expand(self, query: str) -> list:
        query_lower = query.lower().strip()
        cached = await self._cache.get(f"expand:{query_lower}")
        if cached is not None:
            return cached

        try:
            provider = provider_registry.get(self.provider_name)
            prompt = EXPANSION_PROMPT.format(query=query)
            response = await provider.chat(
                [{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            terms = json.loads(response)
            if isinstance(terms, list):
                await self._cache.set(f"expand:{query_lower}", terms, ttl_seconds=3600)
                return terms
        except Exception as e:
            logger.warning("expansion_error", query=query, error=str(e))

        return [query]
