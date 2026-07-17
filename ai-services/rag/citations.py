from typing import Dict, List, Optional
from datetime import datetime


class CitationManager:
    def __init__(self):
        self._citations: Dict[str, List[dict]] = {}

    def add_citations(self, session_id: str, query: str, citations: list):
        if session_id not in self._citations:
            self._citations[session_id] = []
        self._citations[session_id].append({
            "query": query,
            "citations": citations,
            "timestamp": datetime.now().isoformat(),
        })

    def get_citations(self, session_id: str) -> List[dict]:
        return self._citations.get(session_id, [])

    def format_citations(self, citations: list) -> str:
        if not citations:
            return ""
        lines = ["## Sources & Citations"]
        for c in citations:
            lines.append(f"[{c['index']}] {c['doc_type'].title()} — {c['source']} (score: {c['score']})")
        return "\n".join(lines)

    def clear(self, session_id: str):
        self._citations.pop(session_id, None)
