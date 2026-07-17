from typing import Dict, List, Optional
from datetime import datetime


class MemoryStore:
    def __init__(self, max_entries: int = 1000):
        self._entries: Dict[str, List[dict]] = {}
        self._max = max_entries

    def add(self, session_id: str, key: str, value: str, metadata: dict = None):
        if session_id not in self._entries:
            self._entries[session_id] = []
        self._entries[session_id].append({
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        })
        if len(self._entries[session_id]) > self._max:
            self._entries[session_id] = self._entries[session_id][-self._max:]

    def search(self, session_id: str, query: str, limit: int = 10) -> List[dict]:
        entries = self._entries.get(session_id, [])
        query_lower = query.lower()
        matches = [e for e in entries if query_lower in e["value"].lower() or query_lower in e["key"].lower()]
        return matches[-limit:]

    def get_recent(self, session_id: str, limit: int = 10) -> List[dict]:
        return list(reversed(self._entries.get(session_id, [])))[:limit]

    def clear(self, session_id: str):
        self._entries.pop(session_id, None)


memory_store = MemoryStore()
