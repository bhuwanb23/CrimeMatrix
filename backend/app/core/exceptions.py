from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


class ValidationError(Exception):
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details
        self.status_code = 422


class AIServiceError(Exception):
    def __init__(self, message: str, provider: str = "unknown"):
        self.message = message
        self.provider = provider
        self.status_code = 503


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message, "data": None},
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message, "data": exc.details},
    )


async def ai_service_error_handler(request: Request, exc: AIServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": f"AI service error ({exc.provider}): {exc.message}",
            "data": None,
        },
    )


async def general_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "data": None},
    )
