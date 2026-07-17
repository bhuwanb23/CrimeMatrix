from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class PlanStep:
    id: str
    goal: str
    tool: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    status: str = "pending"
    result: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "goal": self.goal,
            "tool": self.tool,
            "params": self.params,
            "depends_on": self.depends_on,
            "status": self.status,
            "result": self.result,
        }


@dataclass
class Plan:
    query: str
    steps: List[PlanStep] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "created"

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "steps": [s.to_dict() for s in self.steps],
            "status": self.status,
            "created_at": self.created_at,
        }


@dataclass
class ToolResult:
    tool_name: str
    params: dict
    output: str
    success: bool
    latency_ms: float = 0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "tool": self.tool_name,
            "params": self.params,
            "output": self.output,
            "success": self.success,
            "latency_ms": self.latency_ms,
            "error": self.error,
        }


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
        self.traces: list[dict] = []

    def add(self, message: Message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def add_trace(self, trace: dict):
        self.traces.append(trace)

    def get_messages_for_llm(self) -> list[dict]:
        return [m.to_dict() for m in self.messages]

    def clear(self):
        self.messages.clear()
        self.traces.clear()

    def get_last_assistant(self) -> Optional[str]:
        for msg in reversed(self.messages):
            if msg.role == "assistant":
                return msg.content
        return None

    def get_full_trace(self) -> list[dict]:
        return self.traces
