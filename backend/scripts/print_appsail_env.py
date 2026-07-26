"""Print AppSail-safe console env lines from backend/.env (do not commit output).

AppSail rejects custom env keys starting with CATALYST_ (platform-reserved).
Use CM_* names in the console. Local .env may still use CATALYST_* — this script
reads either and prints only CM_* for paste into AppSail.
"""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from app.db.providers.catalyst_env import (  # noqa: E402
    DEFAULT_ACCOUNTS_DOMAIN,
    DEFAULT_API_DOMAIN,
    DEFAULT_ENVIRONMENT,
    DEFAULT_ORG_ID,
    DEFAULT_PROJECT_ID,
    cm_getenv,
)

BACKEND_URL = "https://crimematrix-backend-50044181811.development.catalystappsail.in"
AI_URL = "https://crimematrix-ai-50044181811.development.catalystappsail.in"

print("=== crimematrix-backend AppSail env (CM_* — paste these; NOT CATALYST_*) ===")
pairs = [
    ("DB_PROVIDER", "catalyst"),
    ("CM_PROJECT_ID", cm_getenv("CM_PROJECT_ID", DEFAULT_PROJECT_ID)),
    ("CM_ORG_ID", cm_getenv("CM_ORG_ID", DEFAULT_ORG_ID)),
    ("CM_ENVIRONMENT", cm_getenv("CM_ENVIRONMENT", DEFAULT_ENVIRONMENT)),
    ("CM_API_DOMAIN", cm_getenv("CM_API_DOMAIN", DEFAULT_API_DOMAIN)),
    ("CM_ACCOUNTS_DOMAIN", cm_getenv("CM_ACCOUNTS_DOMAIN", DEFAULT_ACCOUNTS_DOMAIN)),
    ("CM_CLIENT_ID", cm_getenv("CM_CLIENT_ID", "") or ""),
    ("CM_CLIENT_SECRET", cm_getenv("CM_CLIENT_SECRET", "") or ""),
    ("CM_REFRESH_TOKEN", cm_getenv("CM_REFRESH_TOKEN", "") or ""),
    ("CM_FILE_FOLDER_ID", cm_getenv("CM_FILE_FOLDER_ID", "") or ""),
    ("AI_SERVICES_URL", AI_URL),  # origin only — do NOT append /api/ai
    ("STORAGE_PROVIDER", "catalyst"),
]
missing = []
for k, v in pairs:
    print(f"{k}={v}")
    if k.startswith("CM_") and k in {
        "CM_CLIENT_ID",
        "CM_CLIENT_SECRET",
        "CM_REFRESH_TOKEN",
        "CM_FILE_FOLDER_ID",
    } and not v:
        missing.append(k)

print()
print("=== crimematrix-ai AppSail env (add/update) ===")
print(f"BACKEND_URL={BACKEND_URL}")  # origin only — do NOT append /api/v1

print()
print("Note: Do NOT create CATALYST_* keys in AppSail — they are reserved.")
print("Local backend/.env may keep CATALYST_* ; the app falls back to them.")
print("AI_SERVICES_URL / BACKEND_URL must be host origins (no /api/ai or /api/v1).")
if missing:
    print("WARNING missing values:", ", ".join(missing))
    raise SystemExit(1)
