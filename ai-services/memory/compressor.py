from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

COMPRESS_PROMPT = """Summarize the following conversation into a concise summary. 
Capture key topics, decisions, tool results, and important facts mentioned.
Keep it under 300 words. Be factual, not creative.

Conversation:
{conversation}

Summary:"""


class ContextCompressor:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model

    async def compress(self, messages: list) -> tuple:
        if len(messages) <= 4:
            return "", messages

        half = len(messages) // 2
        old_messages = messages[:half]
        kept_messages = messages[half:]

        conversation_text = "\n".join([
            f"{m.get('role', 'unknown')}: {m.get('content', '')[:200]}" for m in old_messages
        ])

        try:
            provider = provider_registry.get(self.provider_name)
            prompt = COMPRESS_PROMPT.format(conversation=conversation_text[:3000])
            summary = await provider.chat(
                [{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            logger.info("context_compressed", old_count=len(old_messages), kept_count=len(kept_messages))
            return summary.strip(), kept_messages
        except Exception as e:
            logger.error("compression_error", error=str(e))
            return f"[Previous {len(old_messages)} messages omitted]", kept_messages
