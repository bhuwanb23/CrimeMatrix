from typing import Dict, List, Optional
from datetime import datetime


class SessionMemory:
    def __init__(self, session_id: str, max_messages: int = 50):
        self.session_id = session_id
        self.messages: List[dict] = []
        self.summary: str = ""
        self.summary_boundary: int = 0
        self.max_messages = max_messages
        self.metadata: Dict = {}
        self.created_at = datetime.now().isoformat()

    def add_message(self, role: str, content: str, metadata: dict = None):
        self.messages.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        })

    def get_messages(self) -> List[dict]:
        return [{"role": m["role"], "content": m["content"]} for m in self.messages]

    def get_context(self, max_tokens: int = 2000) -> List[dict]:
        result = []
        if self.summary:
            result.append({"role": "system", "content": f"Previous conversation summary:\n{self.summary}"})
        for m in self.messages:
            result.append({"role": m["role"], "content": m["content"]})
        return result

    def set_summary(self, summary: str, boundary: int):
        self.summary = summary
        self.summary_boundary = boundary

    def get_unsummarized_messages(self) -> List[dict]:
        return self.messages[self.summary_boundary:]

    def needs_compression(self) -> bool:
        return len(self.messages) > self.max_messages

    def clear(self):
        self.messages.clear()
        self.summary = ""
        self.summary_boundary = 0

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "message_count": len(self.messages),
            "has_summary": bool(self.summary),
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
