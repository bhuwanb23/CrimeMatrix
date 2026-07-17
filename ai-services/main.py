import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router
from core.provider import registry as provider_registry
from core.providers.ollama import OllamaProvider
from core.providers.openai_provider import OpenAIProvider
from core.providers.gemini import GeminiProvider
from core.logging import setup_ai_logging
from config import get_config
from tools.registry import tool_registry
from tools.builtins.calculator import CalculatorTool
from tools.builtins.web_fetch import WebFetchTool
import structlog

logger = structlog.get_logger()

config = get_config()


def create_app() -> FastAPI:
    setup_ai_logging(config.log_level)

    app = FastAPI(
        title=config.app_name,
        version=config.version,
        description="CrimeMatrix AI Platform — Agent-based AI service",
        docs_url="/docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register providers
    ollama = OllamaProvider(
        base_url=config.ollama.base_url,
        default_model=config.ollama.default_model,
    )
    provider_registry.register(ollama, default=True)

    openai = OpenAIProvider(
        api_key=config.openai.api_key,
        default_model=config.openai.default_model,
    )
    if config.openai.api_key:
        provider_registry.register(openai)

    gemini = GeminiProvider(
        api_key=config.gemini.api_key,
        default_model=config.gemini.default_model,
    )
    if config.gemini.api_key:
        provider_registry.register(gemini)

    # Register tools
    tool_registry.register(CalculatorTool())
    tool_registry.register(WebFetchTool())

    app.include_router(router, prefix="/api/ai")

    @app.on_event("startup")
    async def startup():
        logger.info("ai_services_startup", port=config.port)
        healthy = await ollama.health_check()
        logger.info("ollama_health", healthy=healthy)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, reload=True)
