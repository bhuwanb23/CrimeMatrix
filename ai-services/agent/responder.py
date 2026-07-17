from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

RESPONDER_SYSTEM_PROMPT = """You are a criminal intelligence copilot for the Karnataka State Police.

Given the user's query and the execution results from various tools, provide a clear, professional response.

Rules:
- Be concise and factual
- Highlight key findings from tool results
- If a tool failed, mention it and suggest alternatives
- Use professional law enforcement language
- Structure your response with clear sections if the answer is complex
- Never invent data — only reference what the tools returned
"""


class ResponseGenerator:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model

    async def generate(self, query: str, context: str) -> str:
        messages = [
            {"role": "system", "content": RESPONDER_SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\n\nProvide a clear response to the user's query."},
        ]

        try:
            provider = provider_registry.get(self.provider_name)
            response = await provider.chat(messages, model=self.model_name)
            return response
        except Exception as e:
            logger.error("responder_error", error=str(e))
            return f"Based on the analysis: {context[:1000]}"
