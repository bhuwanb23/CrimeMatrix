"""Print AppSail console env lines from backend/.env (do not commit output)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

BACKEND_URL = "https://crimematrix-backend-50044181811.development.catalystappsail.in"
AI_URL = "https://crimematrix-ai-50044181811.development.catalystappsail.in"

print("=== crimematrix-backend AppSail env ===")
pairs = [
    ("DB_PROVIDER", "catalyst"),
    ("CATALYST_PROJECT_ID", os.getenv("CATALYST_PROJECT_ID", "46575000000013023")),
    ("CATALYST_ORG_ID", os.getenv("CATALYST_ORG_ID", "60079208195")),
    ("CATALYST_ENVIRONMENT", os.getenv("CATALYST_ENVIRONMENT", "Development")),
    ("CATALYST_API_DOMAIN", os.getenv("CATALYST_API_DOMAIN", "https://api.catalyst.zoho.in")),
    ("CATALYST_ACCOUNTS_DOMAIN", os.getenv("CATALYST_ACCOUNTS_DOMAIN", "https://accounts.zoho.in")),
    ("CATALYST_CLIENT_ID", os.getenv("CATALYST_CLIENT_ID", "")),
    ("CATALYST_CLIENT_SECRET", os.getenv("CATALYST_CLIENT_SECRET", "")),
    ("CATALYST_REFRESH_TOKEN", os.getenv("CATALYST_REFRESH_TOKEN", "")),
    ("CATALYST_FILE_FOLDER_ID", os.getenv("CATALYST_FILE_FOLDER_ID", "")),
    ("AI_SERVICES_URL", AI_URL),
    ("STORAGE_PROVIDER", "catalyst"),
]
for k, v in pairs:
    print(f"{k}={v}")

print()
print("=== crimematrix-ai AppSail env (add/update) ===")
print(f"BACKEND_URL={BACKEND_URL}")
