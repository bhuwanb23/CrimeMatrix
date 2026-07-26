"""Cross-service base URLs (env-overridable for AppSail / local).

Read from the environment on each access so AppSail console changes apply
without relying on import-time snapshots.
"""

from __future__ import annotations

import os


def get_ai_services_url() -> str:
    return os.getenv("AI_SERVICES_URL", "http://localhost:8002").rstrip("/")


def get_backend_url() -> str:
    return os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")


# Back-compat module-level names (resolved at import; prefer getters in new code)
AI_SERVICES_URL = get_ai_services_url()
BACKEND_URL = get_backend_url()
