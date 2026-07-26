#!/usr/bin/env python3
"""Smoke-test CrimeMatrix AI Services on AppSail (Tier A).

Usage:
  python scripts/smoke_appsail.py --base https://<appsail-url>
  python scripts/smoke_appsail.py --base http://localhost:8002
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Optional


def request(
    method: str,
    url: str,
    body: Optional[dict] = None,
    timeout: float = 120.0,
) -> tuple[int, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            try:
                payload = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                payload = raw
            return resp.status, payload
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = raw
        return e.code, payload
    except Exception as e:
        return 0, {"error": str(e)}


def ok_status(status: int) -> bool:
    return 200 <= status < 300


def main() -> int:
    parser = argparse.ArgumentParser(description="AppSail Tier A smoke tests")
    parser.add_argument(
        "--base",
        required=True,
        help="Base URL of ai-services (no trailing slash), e.g. https://host",
    )
    parser.add_argument(
        "--skip-embeddings",
        action="store_true",
        help="Skip embeddings/embed (slow cold start)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=180.0,
        help="Per-request timeout seconds (default 180 for cold start)",
    )
    args = parser.parse_args()
    base = args.base.rstrip("/")
    api = f"{base}/api/ai"

    tests: list[tuple[str, str, str, Optional[dict], float]] = [
        ("GET", f"{api}/health", "health", None, args.timeout),
        ("GET", f"{base}/docs", "docs", None, min(args.timeout, 60)),
        ("GET", f"{api}/models", "models", None, args.timeout),
        ("GET", f"{api}/tools", "tools", None, min(args.timeout, 60)),
        ("GET", f"{api}/agents", "agents", None, min(args.timeout, 60)),
        ("GET", f"{api}/prompts", "prompts", None, min(args.timeout, 60)),
        ("GET", f"{api}/workflows", "workflows", None, min(args.timeout, 60)),
        (
            "POST",
            f"{api}/chat",
            "chat",
            {
                "message": "Reply with exactly: ping-ok",
                "agent_id": "default",
                "session_id": "smoke-test",
                "use_tools": False,
                "language": "en",
            },
            args.timeout,
        ),
        (
            "POST",
            f"{api}/language/normalize",
            "language/normalize",
            {"query": "show me robbery cases in bangalore"},
            min(args.timeout, 60),
        ),
        (
            "POST",
            f"{api}/identity/transliterate",
            "identity/transliterate",
            {"text": "Karthik", "target": "kannada"},
            min(args.timeout, 60),
        ),
    ]
    if not args.skip_embeddings:
        tests.append(
            (
                "POST",
                f"{api}/embeddings/embed",
                "embeddings/embed",
                {"text": "FIR robbery night entry", "domain": "fir"},
                max(args.timeout, 300),
            )
        )

    print(f"Smoke testing: {base}")
    print("-" * 72)
    results: list[tuple[str, bool, int, float, str]] = []

    for method, url, name, body, timeout in tests:
        started = time.time()
        status, payload = request(method, url, body, timeout=timeout)
        elapsed = time.time() - started
        passed = ok_status(status)
        detail = ""
        if name == "docs":
            passed = status == 200
            detail = "swagger"
        elif name == "health" and isinstance(payload, dict):
            detail = json.dumps(payload)[:120]
        elif name == "chat" and isinstance(payload, dict):
            data = payload.get("data") or {}
            detail = str(data.get("response", payload))[:80]
        elif isinstance(payload, dict) and payload.get("error"):
            detail = str(payload.get("error"))[:80]
            if status == 0:
                passed = False
        elif isinstance(payload, dict) and not payload.get("success", True) and name != "docs":
            # some endpoints always wrap success
            if "success" in payload and payload["success"] is False:
                passed = False
                detail = str(payload)[:80]

        mark = "PASS" if passed else "FAIL"
        print(f"{mark:4}  {method:4}  {name:24}  {status:3}  {elapsed:6.1f}s  {detail}")
        results.append((name, passed, status, elapsed, detail))

    print("-" * 72)
    failed = [r for r in results if not r[1]]
    print(f"{len(results) - len(failed)}/{len(results)} passed")

    print("\nTier C (backend-dependent) — expected fail until BACKEND_URL is set:")
    for path in [
        "POST /api/ai/tools/invoke (crime_search, similar_cases, …)",
        "POST /api/ai/search/similar",
        "POST /api/ai/search/cross-district",
        "POST /api/ai/alerts via tools that hit BACKEND_URL",
    ]:
        print(f"  BLOCKED  {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
