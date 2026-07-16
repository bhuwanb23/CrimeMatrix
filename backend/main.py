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
    await init_db()
    logger.info("database_initialized")

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
        allow_origins=["*"],
        allow_credentials=True,
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
