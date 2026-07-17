import json
from tools.base import Tool


class EmbeddingSearchTool(Tool):
    def __init__(self):
        self._service = None

    def _get_service(self):
        if self._service is None:
            from embeddings.service import EmbeddingService
            self._service = EmbeddingService()
        return self._service

    def get_name(self) -> str:
        return "embedding_search"

    def get_description(self) -> str:
        return "Search by embedding similarity across FIRs, evidence, reports, MO fingerprints, and criminal profiles."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query text"},
                "domain": {"type": "string", "description": "Domain: 'fir', 'evidence', 'report', 'mo_fingerprint', 'profile'", "default": "fir"},
                "top_k": {"type": "integer", "description": "Number of results", "default": 5},
            },
            "required": ["query"],
        }

    async def execute(self, query: str = "", domain: str = "fir", top_k: int = 5, **kwargs) -> str:
        service = self._get_service()
        results = await service.search(query, domain, top_k)
        return json.dumps(results, default=str)
