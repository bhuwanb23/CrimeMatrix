from typing import Optional
from datetime import datetime


class Message:
    def __init__(self, role: str, content: str, name: str = None, metadata: dict = None):
        self.role = role
        self.content = content
        self.name = name
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        d = {"role": self.role, "content": self.content}
        if self.name:
            d["name"] = self.name
        return d

    @classmethod
    def system(cls, content: str) -> "Message":
        return cls(role="system", content=content)

    @classmethod
    def user(cls, content: str) -> "Message":
        return cls(role="user", content=content)

    @classmethod
    def assistant(cls, content: str) -> "Message":
        return cls(role="assistant", content=content)

    @classmethod
    def tool(cls, content: str, name: str) -> "Message":
        return cls(role="tool", content=content, name=name)


class ConversationContext:
    def __init__(self, session_id: str = None, max_messages: int = 50):
        self.session_id = session_id
        self.messages: list[Message] = []
        self.max_messages = max_messages
        self.metadata: dict = {}

    def add(self, message: Message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages_for_llm(self) -> list[dict]:
        return [m.to_dict() for m in self.messages]

    def clear(self):
        self.messages.clear()

    def get_last_assistant(self) -> Optional[str]:
        for msg in reversed(self.messages):
            if msg.role == "assistant":
                return msg.content
        return None
