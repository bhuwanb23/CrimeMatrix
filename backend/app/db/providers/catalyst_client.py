"""Catalyst Cloud Scale REST client (Data Store + File Store + ZCQL).

Auth: OAuth2 refresh-token self-client (see docs/CATALYST_DATASTORE.md).
DC defaults to India (zoho.in) for Project-Rainfall.
"""

from __future__ import annotations

import os
import time
from typing import Any, Optional

import httpx


class CatalystConfigError(RuntimeError):
    pass


class CatalystClient:
    def __init__(
        self,
        *,
        project_id: Optional[str] = None,
        org_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        refresh_token: Optional[str] = None,
        environment: Optional[str] = None,
        accounts_domain: Optional[str] = None,
        api_domain: Optional[str] = None,
    ):
        self.project_id = project_id or os.getenv("CATALYST_PROJECT_ID", "46575000000013023")
        self.org_id = org_id or os.getenv("CATALYST_ORG_ID", "60079208195")
        self.client_id = client_id or os.getenv("CATALYST_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("CATALYST_CLIENT_SECRET", "")
        self.refresh_token = refresh_token or os.getenv("CATALYST_REFRESH_TOKEN", "")
        self.environment = environment or os.getenv("CATALYST_ENVIRONMENT", "Development")
        self.accounts_domain = accounts_domain or os.getenv(
            "CATALYST_ACCOUNTS_DOMAIN", "https://accounts.zoho.in"
        )
        self.api_domain = api_domain or os.getenv(
            "CATALYST_API_DOMAIN", "https://api.catalyst.zoho.in"
        )
        self._access_token: Optional[str] = os.getenv("CATALYST_ACCESS_TOKEN") or None
        self._token_expires_at = 0.0
        self._http = httpx.Client(timeout=60.0)

    def configured(self) -> bool:
        if self._access_token:
            return True
        return bool(self.client_id and self.client_secret and self.refresh_token)

    def _ensure_token(self) -> str:
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token
        # Prefer short-lived access token from env for one-shot scripts
        env_token = os.getenv("CATALYST_ACCESS_TOKEN")
        if env_token and not (self.client_id and self.refresh_token):
            self._access_token = env_token
            self._token_expires_at = time.time() + 3500
            return env_token
        if not (self.client_id and self.client_secret and self.refresh_token):
            raise CatalystConfigError(
                "Set CATALYST_CLIENT_ID, CATALYST_CLIENT_SECRET, CATALYST_REFRESH_TOKEN "
                "(or CATALYST_ACCESS_TOKEN) to talk to Data Store."
            )
        resp = self._http.post(
            f"{self.accounts_domain}/oauth/v2/token",
            data={
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
            },
        )
        resp.raise_for_status()
        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise CatalystConfigError(f"Token refresh failed: {payload}")
        self._access_token = token
        self._token_expires_at = time.time() + int(payload.get("expires_in", 3600))
        return token

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Zoho-oauthtoken {self._ensure_token()}",
            "CATALYST-ORG": str(self.org_id),
            "Environment": self.environment,
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.api_domain}/baas/v1/project/{self.project_id}{path}"

    def request(self, method: str, path: str, **kwargs) -> Any:
        resp = self._http.request(method, self._url(path), headers=self._headers(), **kwargs)
        if resp.status_code >= 400:
            raise RuntimeError(f"Catalyst API {method} {path} -> {resp.status_code}: {resp.text[:500]}")
        if not resp.content:
            return None
        data = resp.json()
        if isinstance(data, dict) and data.get("status") == "failure":
            raise RuntimeError(f"Catalyst API failure: {data}")
        return data.get("data") if isinstance(data, dict) and "data" in data else data

    # ---- Data Store tables / columns (read + best-effort create) ----

    def list_tables(self) -> list[dict]:
        result = self.request("GET", "/table")
        return result or []

    def get_table(self, table: str) -> dict:
        return self.request("GET", f"/table/{table}")

    def create_table(self, table_name: str) -> dict:
        """Best-effort create. Official docs are console-only; some orgs allow POST."""
        return self.request("POST", "/table", json={"table_name": table_name})

    def list_columns(self, table: str) -> list[dict]:
        result = self.request("GET", f"/table/{table}/column")
        return result or []

    def create_column(self, table: str, column: dict) -> dict:
        """Best-effort create column via POST /column."""
        body = {
            "column_name": column["column_name"],
            "data_type": column["data_type"],
            "is_mandatory": column.get("is_mandatory", False),
            "is_unique": column.get("is_unique", False),
            "search_index_enabled": column.get("search_index_enabled", False),
        }
        if "max_length" in column:
            body["max_length"] = column["max_length"]
        return self.request("POST", f"/table/{table}/column", json=body)

    # ---- Rows ----

    def insert_row(self, table: str, row: dict) -> dict:
        result = self.request("POST", f"/table/{table}/row", json=row)
        if isinstance(result, list) and result:
            return result[0]
        return result or {}

    def insert_rows(self, table: str, rows: list[dict]) -> list[dict]:
        result = self.request("POST", f"/table/{table}/row", json=rows)
        return result or []

    def get_row(self, table: str, row_id: int | str) -> dict:
        return self.request("GET", f"/table/{table}/row/{row_id}")

    def update_row(self, table: str, row: dict) -> dict:
        result = self.request("PUT", f"/table/{table}/row", json=[row] if isinstance(row, dict) else row)
        if isinstance(result, list) and result:
            return result[0]
        return result or {}

    def delete_row(self, table: str, row_id: int | str) -> Any:
        return self.request("DELETE", f"/table/{table}/row/{row_id}")

    def get_paged_rows(
        self,
        table: str,
        *,
        max_rows: int = 100,
        next_token: Optional[str] = None,
    ) -> dict:
        params: dict[str, Any] = {"max_rows": max_rows}
        if next_token:
            params["next_token"] = next_token
        # Raw response (needs more_records / next_token)
        resp = self._http.get(
            self._url(f"/table/{table}/row"),
            headers=self._headers(),
            params=params,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"get_paged_rows failed: {resp.status_code} {resp.text[:400]}")
        return resp.json()

    def list_all_rows(self, table: str, *, page_size: int = 100, limit: int = 5000) -> list[dict]:
        rows: list[dict] = []
        token = None
        while len(rows) < limit:
            payload = self.get_paged_rows(table, max_rows=min(page_size, limit - len(rows)), next_token=token)
            data = payload.get("data") if isinstance(payload, dict) else payload
            if isinstance(data, dict):
                batch = data.get("rows") or data.get("data") or []
                more = data.get("more_records", False)
                token = data.get("next_token")
            elif isinstance(data, list):
                batch = data
                more = False
                token = None
            else:
                batch = []
                more = payload.get("more_records", False) if isinstance(payload, dict) else False
                token = payload.get("next_token") if isinstance(payload, dict) else None
            rows.extend(batch or [])
            if not more or not token:
                break
        return rows[:limit]

    # ---- ZCQL ----

    def zcql(self, query: str) -> list[dict]:
        result = self.request("POST", "/query", json={"query": query})
        # Some DCs use /zcql
        return result or []

    def zcql_execute(self, query: str) -> list[dict]:
        try:
            return self.zcql(query)
        except RuntimeError:
            result = self.request("POST", "/zcql", json={"query": query})
            return result or []

    # ---- File Store ----

    def list_folders(self) -> list[dict]:
        result = self.request("GET", "/folder")
        return result or []

    def create_folder(self, folder_name: str) -> dict:
        return self.request("POST", "/folder", json={"folder_name": folder_name})

    def upload_file(self, folder_id: str | int, filename: str, data: bytes) -> dict:
        headers = self._headers()
        headers.pop("Content-Type", None)
        files = {"code": (filename, data)}
        resp = self._http.post(
            self._url(f"/folder/{folder_id}/file"),
            headers=headers,
            files=files,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"upload_file failed: {resp.status_code} {resp.text[:400]}")
        payload = resp.json()
        return payload.get("data") if isinstance(payload, dict) else payload

    def close(self) -> None:
        self._http.close()
