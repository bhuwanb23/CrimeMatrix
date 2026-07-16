from config import get_settings
from app.ai.gemini import GeminiProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.ollama import OllamaProvider


def get_ai_provider(provider_name: str = None):
    settings = get_settings()
    name = provider_name or settings.default_ai_provider

    if name == "gemini":
        return GeminiProvider(api_key=settings.gemini_api_key)
    elif name == "openai":
        return OpenAIProvider(api_key=settings.openai_api_key)
    elif name == "ollama":
        return OllamaProvider(base_url=settings.ollama_base_url)
    else:
        raise ValueError(f"Unknown provider: {name}")
