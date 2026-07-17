import json
from tools.base import Tool


class RAGSearchTool(Tool):
    def __init__(self):
        self._pipeline = None

    def _get_pipeline(self):
        if self._pipeline is None:
            from rag.pipeline import RAGPipeline
            self._pipeline = RAGPipeline()
        return self._pipeline

    def get_name(self) -> str:
        return "rag_search"

    def get_description(self) -> str:
        return "Search indexed documents (FIRs, investigation notes, evidence) using semantic search."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "top_k": {"type": "integer", "description": "Number of results", "default": 5},
                "doc_type": {"type": "string", "description": "Filter by type: 'fir' or 'note'"},
            },
            "required": ["query"],
        }

    async def execute(self, query: str = "", top_k: int = 5, doc_type: str = None, **kwargs) -> str:
        pipeline = self._get_pipeline()
        result = pipeline.search(query, top_k, doc_type)
        return json.dumps(result, default=str)
