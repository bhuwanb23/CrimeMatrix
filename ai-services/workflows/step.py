from typing import Dict, Any, Callable, List, Optional
import time
import structlog

logger = structlog.get_logger()


class WorkflowStep:
    def __init__(self, name: str, func: Callable, description: str = "",
                 depends_on: List[str] = None, parallel: bool = False,
                 timeout: float = 30.0, retries: int = 0):
        self.name = name
        self.func = func
        self.description = description
        self.depends_on = depends_on or []
        self.parallel = parallel
        self.timeout = timeout
        self.retries = retries
        self.status = "pending"
        self.result = None
        self.error = None
        self.duration_ms = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "depends_on": self.depends_on,
            "parallel": self.parallel,
            "status": self.status,
            "duration_ms": self.duration_ms,
        }
