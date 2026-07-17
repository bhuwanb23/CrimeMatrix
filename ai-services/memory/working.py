from typing import Dict, Any, Optional


class WorkingMemory:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._order: list = []

    def set(self, key: str, value: Any):
        self._store[key] = value
        if key not in self._order:
            self._order.append(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def delete(self, key: str):
        self._store.pop(key, None)
        if key in self._order:
            self._order.remove(key)

    def clear(self):
        self._store.clear()
        self._order.clear()

    def get_all(self) -> Dict[str, Any]:
        return dict(self._store)

    def keys(self) -> list:
        return list(self._order)

    def format_for_context(self) -> str:
        if not self._store:
            return ""
        lines = ["Working Memory:"]
        for k, v in self._store.items():
            val_str = str(v)[:500]
            lines.append(f"- {k}: {val_str}")
        return "\n".join(lines)
