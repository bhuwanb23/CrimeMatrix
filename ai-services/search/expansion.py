import json
from core.provider import registry as provider_registry
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
        self._cache: dict = {}

    async def expand(self, query: str) -> list:
        query_lower = query.lower().strip()
        if query_lower in self._cache:
            return self._cache[query_lower]

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
                self._cache[query_lower] = terms
                return terms
        except Exception as e:
            logger.warning("expansion_error", query=query, error=str(e))

        return [query]
