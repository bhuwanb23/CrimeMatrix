from fastapi import APIRouter
from app.core.response import success_response
from app.core.validation import ChatRequest
from app.core.exceptions import AIServiceError
from config import get_settings
import structlog

router = APIRouter()
logger = structlog.get_logger()


@router.post("/chat")
async def chat(request: ChatRequest):
    settings = get_settings()
    provider_name = request.provider or settings.default_ai_provider

    try:
        if provider_name == "gemini":
            from app.ai.gemini import GeminiProvider
            provider = GeminiProvider(api_key=settings.gemini_api_key)
        elif provider_name == "openai":
            from app.ai.openai_provider import OpenAIProvider
            provider = OpenAIProvider(api_key=settings.openai_api_key)
        elif provider_name == "ollama":
            from app.ai.ollama import OllamaProvider
            provider = OllamaProvider(base_url=settings.ollama_base_url)
        else:
            raise AIServiceError(f"Unknown provider: {provider_name}", provider_name)

        response = await provider.chat(request.message, request.context)

        return success_response(
            data={
                "response": response,
                "provider": provider_name,
                "model": "default",
            }
        )
    except AIServiceError:
        raise
    except Exception as e:
        logger.error("chat_error", provider=provider_name, error=str(e))
        raise AIServiceError(str(e), provider_name)


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    from fastapi.responses import StreamingResponse
    from app.core.exceptions import AIServiceError
    from config import get_settings

    settings = get_settings()
    provider_name = request.provider or settings.default_ai_provider

    try:
        if provider_name == "gemini":
            from app.ai.gemini import GeminiProvider
            provider = GeminiProvider(api_key=settings.gemini_api_key)
        elif provider_name == "openai":
            from app.ai.openai_provider import OpenAIProvider
            provider = OpenAIProvider(api_key=settings.openai_api_key)
        elif provider_name == "ollama":
            from app.ai.ollama import OllamaProvider
            provider = OllamaProvider(base_url=settings.ollama_base_url)
        else:
            raise AIServiceError(f"Unknown provider: {provider_name}", provider_name)

        async def generate():
            async for chunk in provider.stream(request.message, request.context):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
    except AIServiceError:
        raise
    except Exception as e:
        logger.error("stream_error", provider=provider_name, error=str(e))
        raise AIServiceError(str(e), provider_name)
