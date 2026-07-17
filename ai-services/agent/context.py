from agent.message import Plan, PlanStep, ToolResult
from typing import List


class ContextBuilder:
    def build(self, query: str, plan: Plan, results: List[ToolResult]) -> str:
        parts = []
        parts.append(f"## User Query\n{query}\n")

        if plan.steps:
            parts.append("## Execution Plan & Results\n")
            for i, (step, result) in enumerate(zip(plan.steps, results)):
                status = "✅" if result.success else "❌"
                parts.append(f"### Step {i+1}: {step.goal}")
                parts.append(f"- Tool: {step.tool or 'reasoning'}")
                parts.append(f"- Status: {status}")
                if step.params:
                    parts.append(f"- Params: {step.params}")
                if result.output:
                    output = result.output[:2000]
                    parts.append(f"- Output: {output}")
                if result.error:
                    parts.append(f"- Error: {result.error}")
                parts.append("")

        return "\n".join(parts)

    def build_for_streaming(self, step: PlanStep, result: ToolResult) -> str:
        status = "✅" if result.success else "❌"
        parts = [f"Step: {step.goal} [{status}]"]
        if result.output:
            parts.append(f"Result: {result.output[:500]}")
        return "\n".join(parts)
