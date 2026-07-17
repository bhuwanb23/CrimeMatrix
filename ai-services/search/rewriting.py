import json
from core.provider import registry as provider_registry
from storage.cache_provider import MemoryCacheProvider
import structlog

logger = structlog.get_logger()

REWRITE_PROMPT = """Rewrite the following user query into a clean, search-optimized query.
Remove filler words, extract key terms, preserve meaning.
Return ONLY the rewritten query text, nothing else.

User query: {query}
Rewritten:"""


class QueryRewriting:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model
        self._cache = MemoryCacheProvider(max_size=5000)

    async def rewrite(self, query: str) -> str:
        query_lower = query.lower().strip()
        cached = await self._cache.get(f"rewrite:{query_lower}")
        if cached is not None:
            return cached

        try:
            provider = provider_registry.get(self.provider_name)
            prompt = REWRITE_PROMPT.format(query=query)
            response = await provider.chat(
                [{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            rewritten = response.strip().strip('"').strip("'")
            await self._cache.set(f"rewrite:{query_lower}", rewritten, ttl_seconds=3600)
            return rewritten
        except Exception as e:
            logger.warning("rewrite_error", query=query, error=str(e))
            return query
