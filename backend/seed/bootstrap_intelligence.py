"""Post-seed intelligence bootstrap.

Calls detect/batch/build endpoints so AI/ML pages have computed data.
Requires the backend API to be running (default http://localhost:8000).

Usage:
    python -m seed --bootstrap
    # or after seed:
    from seed.bootstrap_intelligence import run_bootstrap
    await run_bootstrap()
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BACKEND_URL = os.getenv("CRIMEMATRIX_API_URL", "http://localhost:8000/api/v1")

# (label, method, path, optional json body)
BOOTSTRAP_STEPS: list[tuple[str, str, str, dict[str, Any] | None]] = [
    ("patterns.detect", "POST", "/patterns/detect", {}),
    ("mo.batch_fingerprint", "POST", "/mo/batch-fingerprint", {}),
    ("cross_district.detect", "POST", "/cross-district/detect", {}),
    ("suspect_risk.batch_score", "POST", "/suspect-risk/batch-score", {}),
    ("priorities.batch_score", "POST", "/priorities/batch-score", {}),
    ("evidence_linking.detect", "POST", "/evidence-linking/detect", {}),
    ("early_warning.detect", "POST", "/early-warning/detect", {}),
    ("proactive.scan", "POST", "/proactive/scan", {}),
    ("graph.build_from_crimes", "POST", "/graph/build-from-crimes", {}),
    ("predictions.forecast", "POST", "/predictions/forecast", {}),
    ("hotspots.detect", "POST", "/hotspots/detect", {}),
    ("evaluation.run", "POST", "/evaluation/run", {}),
]


async def run_bootstrap(base_url: str | None = None) -> dict[str, str]:
    """Best-effort bootstrap. Returns {step: ok|error message}."""
    url = (base_url or BACKEND_URL).rstrip("/")
    results: dict[str, str] = {}

    async with httpx.AsyncClient(timeout=120.0) as client:
        # Health check
        try:
            health = await client.get(url.replace("/api/v1", "") + "/api/v1/health")
            if health.status_code >= 400:
                # try alternate
                health = await client.get(f"{url}/health")
        except Exception as exc:
            print(f"  [bootstrap] Backend not reachable at {url}: {exc}")
            print("  Start the API first: uvicorn main:app --port 8000 --reload")
            return {"_error": str(exc)}

        for label, method, path, body in BOOTSTRAP_STEPS:
            full = f"{url}{path}"
            try:
                if method == "POST":
                    resp = await client.post(full, json=body if body is not None else {})
                else:
                    resp = await client.get(full)
                if resp.status_code < 400:
                    results[label] = "ok"
                    print(f"  [bootstrap] {label} OK ({resp.status_code})")
                else:
                    msg = f"HTTP {resp.status_code}"
                    try:
                        msg = f"HTTP {resp.status_code}: {resp.text[:120]}"
                    except Exception:
                        pass
                    results[label] = msg
                    print(f"  [bootstrap] {label} FAIL — {msg}")
            except Exception as exc:
                results[label] = str(exc)
                print(f"  [bootstrap] {label} FAIL — {exc}")

    return results
