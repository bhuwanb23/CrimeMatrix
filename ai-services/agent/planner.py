import json
from typing import List
from agent.message import Plan, PlanStep
from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

PLANNER_SYSTEM_PROMPT = """You are a planning engine for a criminal intelligence copilot. Given a user query and available tools, decompose the query into ordered steps.

Return ONLY a JSON array of steps. Each step:
{
  "id": "step_1",
  "goal": "What this step accomplishes",
  "tool": "tool_name_or_null",
  "params": {"param": "value"},
  "depends_on": []
}

Rules:
- If the query doesn't need tools (greeting, opinion, explanation), return an empty array []
- Use null for tool if step is just reasoning/analysis
- Set depends_on to step IDs that must complete first
- Keep steps minimal — one tool call per step
- Return ONLY the JSON array, nothing else

Example for "Calculate 15*23 and then add 50":
[
  {"id": "step_1", "goal": "Calculate 15 * 23", "tool": "calculator", "params": {"expression": "15 * 23"}, "depends_on": []},
  {"id": "step_2", "goal": "Add 50 to the result", "tool": "calculator", "params": {"expression": "345 + 50"}, "depends_on": []}
]
"""


class Planner:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model

    async def plan(self, query: str, available_tools: list) -> Plan:
        tools_desc = "\n".join([
            f"- {t['name']}: {t['description']}" for t in available_tools
        ])

        messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Available tools:\n{tools_desc}\n\nUser query: {query}\n\nReturn the plan as JSON array:"},
        ]

        try:
            provider = provider_registry.get(self.provider_name)
            response = await provider.chat(messages, model=self.model_name)
            response = response.strip()

            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]

            steps_data = json.loads(response)
            if not isinstance(steps_data, list):
                steps_data = []

            steps = []
            for s in steps_data:
                steps.append(PlanStep(
                    id=s.get("id", f"step_{len(steps)+1}"),
                    goal=s.get("goal", ""),
                    tool=s.get("tool"),
                    params=s.get("params", {}),
                    depends_on=s.get("depends_on", []),
                ))

            plan = Plan(query=query, steps=steps)
            logger.info("plan_created", query=query[:100], steps=len(steps))
            return plan

        except Exception as e:
            logger.error("planner_error", error=str(e))
            return Plan(query=query, steps=[
                PlanStep(id="step_1", goal=query, tool=None, params={})
            ])
