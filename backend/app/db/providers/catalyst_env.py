"""CrimeMatrix Catalyst credential env keys.

AppSail console rejects custom variables whose names start with ``CATALYST_``
(platform-reserved). Use ``CM_*`` on AppSail. Local ``backend/.env`` may still
use the older ``CATALYST_*`` names — readers accept either (``CM_*`` wins).
"""

from __future__ import annotations

import os
from typing import Optional


# AppSail-safe name -> legacy local name (optional fallback)
_ENV_ALIASES: dict[str, str] = {
    "CM_PROJECT_ID": "CATALYST_PROJECT_ID",
    "CM_ORG_ID": "CATALYST_ORG_ID",
    "CM_ENVIRONMENT": "CATALYST_ENVIRONMENT",
    "CM_API_DOMAIN": "CATALYST_API_DOMAIN",
    "CM_ACCOUNTS_DOMAIN": "CATALYST_ACCOUNTS_DOMAIN",
    "CM_CLIENT_ID": "CATALYST_CLIENT_ID",
    "CM_CLIENT_SECRET": "CATALYST_CLIENT_SECRET",
    "CM_REFRESH_TOKEN": "CATALYST_REFRESH_TOKEN",
    "CM_ACCESS_TOKEN": "CATALYST_ACCESS_TOKEN",
    "CM_FILE_FOLDER": "CATALYST_FILE_FOLDER",
    "CM_FILE_FOLDER_ID": "CATALYST_FILE_FOLDER_ID",
}


def cm_getenv(cm_key: str, default: Optional[str] = None) -> Optional[str]:
    """Read ``CM_*`` first, then legacy ``CATALYST_*``."""
    val = os.getenv(cm_key)
    if val is not None and str(val).strip() != "":
        return val.strip()
    legacy = _ENV_ALIASES.get(cm_key)
    if legacy:
        val = os.getenv(legacy)
        if val is not None and str(val).strip() != "":
            return val.strip()
    return default


# Defaults for Project-Rainfall (IN DC)
DEFAULT_PROJECT_ID = "46575000000013023"
DEFAULT_ORG_ID = "60079208195"
DEFAULT_ENVIRONMENT = "Development"
DEFAULT_API_DOMAIN = "https://api.catalyst.zoho.in"
DEFAULT_ACCOUNTS_DOMAIN = "https://accounts.zoho.in"
DEFAULT_FILE_FOLDER = "cm_uploads"

# Keys to set in AppSail console (never use CATALYST_* there)
APPSAIL_ENV_KEYS: list[str] = [
    "DB_PROVIDER",
    "CM_PROJECT_ID",
    "CM_ORG_ID",
    "CM_ENVIRONMENT",
    "CM_API_DOMAIN",
    "CM_ACCOUNTS_DOMAIN",
    "CM_CLIENT_ID",
    "CM_CLIENT_SECRET",
    "CM_REFRESH_TOKEN",
    "CM_FILE_FOLDER_ID",
    "AI_SERVICES_URL",
    "STORAGE_PROVIDER",
]
