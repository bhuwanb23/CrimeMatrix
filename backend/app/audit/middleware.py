import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, audit_stores=None):
        super().__init__(app)
        self.stores = audit_stores or {}

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent", "")

        response = await call_next(request)

        duration_ms = (time.time() - start) * 1000
        path = str(request.url.path)

        if path.startswith("/api/v1/"):
            if "request_logs" in self.stores:
                self.stores["request_logs"].log(
                    method=request.method,
                    path=path,
                    status_code=response.status_code,
                    duration_ms=duration_ms,
                    client_ip=client_ip,
                    user_agent=user_agent,
                )
            if "api_logs" in self.stores:
                self.stores["api_logs"].log(
                    method=request.method,
                    path=path,
                    status_code=response.status_code,
                    duration_ms=duration_ms,
                    client_ip=client_ip,
                )
            if "metrics" in self.stores:
                self.stores["metrics"].increment("http_requests_total")
                self.stores["metrics"].increment(f"http_requests_{request.method.lower()}")
                self.stores["metrics"].observe("http_request_duration_ms", duration_ms)
                self.stores["metrics"].set_gauge("http_last_request_duration_ms", round(duration_ms, 2))

        return response
