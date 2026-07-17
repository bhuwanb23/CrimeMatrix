class AIServiceError(Exception):
    def __init__(self, message: str, code: str = "AI_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class ProviderError(AIServiceError):
    def __init__(self, message: str, provider: str = None):
        super().__init__(message, code="PROVIDER_ERROR", status_code=502)
        self.provider = provider


class ToolError(AIServiceError):
    def __init__(self, message: str, tool_name: str = None):
        super().__init__(message, code="TOOL_ERROR", status_code=400)
        self.tool_name = tool_name


class TokenLimitError(AIServiceError):
    def __init__(self, message: str = "Token limit exceeded"):
        super().__init__(message, code="TOKEN_LIMIT", status_code=400)


class RateLimitError(AIServiceError):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT", status_code=429)
