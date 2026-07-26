from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.router import router as v1_router
from app.core.exceptions import (
    AppError, app_error_handler,
    ValidationError, validation_error_handler,
    AIServiceError, ai_service_error_handler,
    general_error_handler,
)
from app.core.logging import setup_logging, get_logger
from app.audit.middleware import AuditMiddleware
from app.audit.stores import request_logs, api_logs, metrics
from config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger = get_logger()
    logger.info("app_startup", env=settings.app_env)

    # Initialize database
    from app.db.session import init_db
    from app.db.providers import get_db_provider_name, init_data_provider

    provider_name = get_db_provider_name()
    if provider_name in {"catalyst", "catalyst_local"}:
        await init_data_provider()
        logger.info("phase1_datastore_initialized", provider=provider_name)
    # Keep SQLAlchemy schema for non-Phase-1 routes / local default
    await init_db()
    logger.info("database_initialized", provider=provider_name)

    yield

    logger.info("app_shutdown")


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="KSP Crime Intelligence Copilot API",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://crimematrix-frontend-nvjwdioh.onslate.in",
        ],
        allow_origin_regex=r"https://.*\.onslate\.in",
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        AuditMiddleware,
        audit_stores={
            "request_logs": request_logs,
            "api_logs": api_logs,
            "metrics": metrics,
        },
    )

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(AIServiceError, ai_service_error_handler)
    app.add_exception_handler(Exception, general_error_handler)

    app.include_router(v1_router)

    return app


app = create_app()
