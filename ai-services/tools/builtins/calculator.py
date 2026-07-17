import json
from tools.base import Tool


class CalculatorTool(Tool):
    def get_name(self) -> str:
        return "calculator"

    def get_description(self) -> str:
        return "Perform mathematical calculations. Supports basic arithmetic, min/max, round."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')",
                }
            },
            "required": ["expression"],
        }

    async def execute(self, expression: str = "", **kwargs) -> str:
        try:
            allowed = set("0123456789+-*/.() ")
            if not all(c in allowed for c in expression):
                return json.dumps({"error": "Invalid characters in expression"})
            result = eval(expression)
            return json.dumps({"expression": expression, "result": result})
        except Exception as e:
            return json.dumps({"error": str(e)})
