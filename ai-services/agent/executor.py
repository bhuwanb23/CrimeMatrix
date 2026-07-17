import json
from agent.message import PlanStep, ToolResult
from tools.registry import tool_registry
import structlog
import time

logger = structlog.get_logger()


class Executor:
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries

    async def execute(self, step: PlanStep) -> ToolResult:
        tool_name = step.tool
        if not tool_name:
            return ToolResult(
                tool_name="none",
                params={},
                output="",
                success=True,
            )

        tool = tool_registry.get(tool_name)
        if not tool:
            return ToolResult(
                tool_name=tool_name,
                params=step.params,
                output="",
                success=False,
                error=f"Tool '{tool_name}' not found",
            )

        last_error = None
        for attempt in range(self.max_retries + 1):
            start = time.time()
            try:
                result = await tool.execute(**step.params)
                latency = (time.time() - start) * 1000
                logger.info("tool_executed", tool=tool_name, attempt=attempt, latency_ms=round(latency, 2))
                return ToolResult(
                    tool_name=tool_name,
                    params=step.params,
                    output=result,
                    success=True,
                    latency_ms=round(latency, 2),
                )
            except Exception as e:
                last_error = str(e)
                logger.warning("tool_execution_retry", tool=tool_name, attempt=attempt, error=last_error)

        return ToolResult(
            tool_name=tool_name,
            params=step.params,
            output="",
            success=False,
            latency_ms=0,
            error=last_error,
        )
