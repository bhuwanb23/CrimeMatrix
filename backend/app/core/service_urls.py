"""Cross-service base URLs (env-overridable for AppSail / local)."""

from __future__ import annotations

import os

# Backend listens on 8000 locally; AI services on 8002.
AI_SERVICES_URL = os.getenv("AI_SERVICES_URL", "http://localhost:8002").rstrip("/")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
