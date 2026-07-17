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
import structlog

logger = structlog.get_logger()

config = get_config()


def create_app() -> FastAPI:
    setup_ai_logging(config.log_level)

    app = FastAPI(
        title=config.app_name,
        version=config.version,
        description="CrimeMatrix AI Platform — Agent-based AI service with reasoning loop",
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
    from tools.builtins.calculator import CalculatorTool
    from tools.builtins.web_fetch import WebFetchTool
    from tools.crime.search import CrimeSearchTool
    from tools.crime.detail import CrimeDetailTool
    from tools.crime.list import CrimeListTool
    from tools.crime.stats import CrimeStatsTool
    from tools.graph.traverse import GraphTraverseTool
    from tools.graph.shortest import GraphShortestPathTool
    from tools.graph.neighbors import GraphNeighborsTool
    from tools.analytics.counts import AnalyticsCountsTool
    from tools.analytics.trends import AnalyticsTrendsTool
    from tools.investigation.notes import InvestigationNotesTool
    from tools.investigation.timeline import InvestigationTimelineTool
    from tools.investigation.status import CaseStatusTool
    from tools.report.generate import ReportGenerateTool
    from tools.rag.search import RAGSearchTool
    from tools.search.intelligent import SearchIntelligentTool
    from tools.identity.match import IdentityMatchTool
    from tools.knowledge.graph import KnowledgeGraphTool

    for tool_cls in [
        CalculatorTool, WebFetchTool,
        CrimeSearchTool, CrimeDetailTool, CrimeListTool, CrimeStatsTool,
        GraphTraverseTool, GraphShortestPathTool, GraphNeighborsTool,
        AnalyticsCountsTool, AnalyticsTrendsTool,
        InvestigationNotesTool, InvestigationTimelineTool, CaseStatusTool,
        ReportGenerateTool, RAGSearchTool, SearchIntelligentTool, IdentityMatchTool,
        KnowledgeGraphTool,
    ]:
        tool_registry.register(tool_cls())

    logger.info("tools_registered", count=len(tool_registry.list_all()))

    app.include_router(router, prefix="/api/ai")

    @app.on_event("startup")
    async def startup():
        logger.info("ai_services_startup", port=config.port, version="3.0.0")
        healthy = await ollama.health_check()
        logger.info("ollama_health", healthy=healthy)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, reload=True)
