"""Cross-service base URLs (env-overridable for AppSail / local).

Read from the environment on each access so AppSail console changes apply
without relying on import-time snapshots.

``AI_SERVICES_URL`` must be the AI AppSail **origin** only, e.g.
``https://crimematrix-ai-....catalystappsail.in`` — not ``.../api/ai``.
If a trailing ``/api/ai`` is present it is stripped automatically.
"""

from __future__ import annotations

import os
import re


def _strip_suffixes(url: str, suffixes: tuple[str, ...]) -> str:
    u = (url or "").strip().rstrip("/")
    for suf in suffixes:
        if u.lower().endswith(suf.lower()):
            u = u[: -len(suf)].rstrip("/")
    return u


def get_ai_services_url() -> str:
    raw = os.getenv("AI_SERVICES_URL", "http://localhost:8002")
    return _strip_suffixes(raw, ("/api/ai", "/api"))


def get_backend_url() -> str:
    raw = os.getenv("BACKEND_URL", "http://localhost:8000")
    return _strip_suffixes(raw, ("/api/v1", "/api"))


# Back-compat module-level names (prefer getters in new code)
AI_SERVICES_URL = get_ai_services_url()
BACKEND_URL = get_backend_url()
