from typing import Dict, Any, Optional
from datetime import datetime


class UserPreferences:
    DEFAULTS = {
        "language": "en",
        "response_style": "concise",
        "preferred_tools": [],
        "timezone": "Asia/Kolkata",
        "context_window": 50,
        "auto_compress": True,
    }

    def __init__(self):
        self._prefs: Dict[str, Dict[str, Any]] = {}

    def get(self, user_id: str) -> Dict[str, Any]:
        return self._prefs.get(user_id, dict(self.DEFAULTS))

    def set(self, user_id: str, key: str, value: Any):
        if user_id not in self._prefs:
            self._prefs[user_id] = dict(self.DEFAULTS)
        self._prefs[user_id][key] = value
        self._prefs[user_id]["updated_at"] = datetime.now().isoformat()

    def get_all(self, user_id: str) -> Dict[str, Any]:
        return self.get(user_id)

    def update(self, user_id: str, updates: Dict[str, Any]):
        if user_id not in self._prefs:
            self._prefs[user_id] = dict(self.DEFAULTS)
        self._prefs[user_id].update(updates)
        self._prefs[user_id]["updated_at"] = datetime.now().isoformat()

    def delete(self, user_id: str):
        self._prefs.pop(user_id, None)

    def format_for_system_prompt(self, user_id: str) -> str:
        prefs = self.get(user_id)
        lines = [f"User preferences:"]
        for k, v in prefs.items():
            if v and k != "updated_at":
                lines.append(f"- {k}: {v}")
        return "\n".join(lines) if len(lines) > 1 else ""
