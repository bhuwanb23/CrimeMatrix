from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

RESPONDER_SYSTEM_PROMPT = """You are CrimeMatrix, a friendly AI assistant for the Karnataka State Police.

Rules:
- Respond naturally and conversationally, like a helpful colleague
- If there are tool results, present the findings clearly and concisely
- If there are no tool results, just answer the question directly
- Never mention "tools", "execution results", "reasoning chain", or technical details
- Never say "The tool indicated..." or "The execution results show..."
- Match the tone of the user — if they're casual, be casual; if formal, be professional
- Use bullet points or sections only when the answer is genuinely complex
- For simple questions, give simple answers
- Be helpful, not verbose"""


class ResponseGenerator:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model

    async def generate(self, query: str, context: str) -> str:
        messages = [
            {"role": "system", "content": RESPONDER_SYSTEM_PROMPT},
            {"role": "user", "content": f"User asked: {query}\n\nContext from investigation tools:\n{context}\n\nProvide a natural, helpful response:"},
        ]

        try:
            provider = provider_registry.get(self.provider_name)
            response = await provider.chat(messages, model=self.model_name)
            return response
        except Exception as e:
            logger.error("responder_error", error=str(e))
            return f"Based on the analysis: {context[:1000]}"
