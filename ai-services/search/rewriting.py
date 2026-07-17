import json
from core.provider import registry as provider_registry
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
        self._cache: dict = {}

    async def rewrite(self, query: str) -> str:
        query_lower = query.lower().strip()
        if query_lower in self._cache:
            return self._cache[query_lower]

        try:
            provider = provider_registry.get(self.provider_name)
            prompt = REWRITE_PROMPT.format(query=query)
            response = await provider.chat(
                [{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            rewritten = response.strip().strip('"').strip("'")
            self._cache[query_lower] = rewritten
            return rewritten
        except Exception as e:
            logger.warning("rewrite_error", query=query, error=str(e))
            return query
