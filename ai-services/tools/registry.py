from typing import Dict, Optional
from tools.base import Tool
import structlog

logger = structlog.get_logger()


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        name = tool.get_name()
        self._tools[name] = tool
        logger.info("tool_registered", name=name)

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_all(self) -> list:
        return [t.to_schema() for t in self._tools.values()]

    def list_names(self) -> list:
        return list(self._tools.keys())

    async def invoke(self, name: str, **kwargs) -> str:
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found. Available: {self.list_names()}")
        return await tool.execute(**kwargs)


tool_registry = ToolRegistry()
