from app.audit.request_logs import RequestLogStore
from app.audit.api_logs import APILogStore
from app.audit.metrics import MetricsEngine

# Singleton instances shared between middleware and API
request_logs = RequestLogStore()
api_logs = APILogStore()
metrics = MetricsEngine()
