import json
from tools.base import Tool


class SearchIntelligentTool(Tool):
    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from search.engine import SearchEngine
            self._engine = SearchEngine(provider="ollama", model="llama3.2:1b")
        return self._engine

    def get_name(self) -> str:
        return "search_intelligent"

    def get_description(self) -> str:
        return "Intelligent search with query rewriting, expansion, hybrid scoring, and LLM reranking. Best for complex crime queries."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query in natural language"},
                "top_k": {"type": "integer", "description": "Number of results", "default": 5},
                "doc_type": {"type": "string", "description": "Filter: 'fir' or 'note'"},
            },
            "required": ["query"],
        }

    async def execute(self, query: str = "", top_k: int = 5, doc_type: str = None, **kwargs) -> str:
        engine = self._get_engine()
        result = await engine.intelligent_search(query, top_k, doc_type)
        return json.dumps(result, default=str)
