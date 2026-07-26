#!/usr/bin/env python3
"""Full endpoint validation for CrimeMatrix AI Services on AppSail.

Usage:
  python scripts/validate_all_endpoints.py --base https://crimematrix-ai-....catalystappsail.in
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Optional


BASE_DEFAULT = "https://crimematrix-ai-50044181811.development.catalystappsail.in"

# Endpoints that need CrimeMatrix backend (BACKEND_URL) — expected fail on AppSail-only
BACKEND_DEPENDENT = {
    "POST /rag/index",
    "POST /search/similar",
    "POST /search/cross-district",
    "POST /knowledge/build",
    "POST /tools/invoke:crime_search",
    "POST /tools/invoke:similar_cases",
    "POST /memory/investigation",
}


def request(
    method: str,
    url: str,
    body: Optional[dict] = None,
    timeout: float = 90.0,
) -> tuple[int, Any, float]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            try:
                payload = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                payload = raw[:200]
            return resp.status, payload, time.time() - started
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = raw[:200]
        return e.code, payload, time.time() - started
    except Exception as e:
        return 0, {"error": str(e)}, time.time() - started


def ok(status: int, payload: Any) -> bool:
    if not (200 <= status < 300):
        return False
    if isinstance(payload, dict) and payload.get("success") is False:
        return False
    return True


def evidence() -> list:
    return [
        {"claim": "Suspect seen near scene", "type": "witness", "strength": 0.7, "supports": True},
        {"claim": "Phone ping at location", "type": "digital", "strength": 0.8, "supports": True},
    ]


def build_cases(api: str) -> list[dict]:
    """Return list of test case dicts: name, method, path, body, timeout, tier."""
    cases = [
        # Core
        ("GET /docs", "GET", "/docs", None, 30, "A"),
        ("GET /health", "GET", "/api/ai/health", None, 60, "A"),
        ("GET /models", "GET", "/api/ai/models", None, 60, "A"),
        ("GET /agents", "GET", "/api/ai/agents", None, 30, "A"),
        ("GET /agents/default", "GET", "/api/ai/agents/default", None, 30, "A"),
        ("GET /sessions", "GET", "/api/ai/sessions", None, 30, "A"),
        ("GET /tools", "GET", "/api/ai/tools", None, 30, "A"),
        ("GET /tools/calculator", "GET", "/api/ai/tools/calculator", None, 30, "A"),
        ("GET /prompts", "GET", "/api/ai/prompts", None, 30, "A"),
        ("GET /tokens", "GET", "/api/ai/tokens", None, 30, "A"),
        ("GET /workflows", "GET", "/api/ai/workflows", None, 30, "A"),
        ("GET /workflows/investigation", "GET", "/api/ai/workflows/investigation", None, 30, "B"),
        ("GET /workflows/investigation/steps", "GET", "/api/ai/workflows/investigation/steps", None, 30, "B"),
        (
            "POST /chat",
            "POST",
            "/api/ai/chat",
            {
                "message": "Say only: validation-ok",
                "agent_id": "default",
                "session_id": "full-validate",
                "use_tools": False,
                "language": "en",
            },
            120,
            "A",
        ),
        (
            "POST /tools/invoke:calculator",
            "POST",
            "/api/ai/tools/invoke",
            {"tool": "calculator", "params": {"expression": "2+2"}},
            30,
            "A",
        ),
        # Memory
        ("GET /memory/sessions/full-validate/history", "GET", "/api/ai/memory/sessions/full-validate/history", None, 30, "B"),
        ("GET /memory/sessions/full-validate/summary", "GET", "/api/ai/memory/sessions/full-validate/summary", None, 60, "B"),
        ("GET /memory/preferences/validate-user", "GET", "/api/ai/memory/preferences/validate-user", None, 30, "B"),
        (
            "PUT /memory/preferences/validate-user",
            "PUT",
            "/api/ai/memory/preferences/validate-user",
            {"key": "lang", "value": "en"},
            30,
            "B",
        ),
        ("GET /memory/working", "GET", "/api/ai/memory/working", None, 30, "B"),
        (
            "POST /memory/investigation",
            "POST",
            "/api/ai/memory/investigation",
            {"investigation_id": 1},
            30,
            "C",
        ),
        ("DELETE /sessions/full-validate-del", "DELETE", "/api/ai/sessions/full-validate-del", None, 30, "B"),
        ("GET /sessions/full-validate/trace", "GET", "/api/ai/sessions/full-validate/trace", None, 30, "B"),
        # RAG
        ("POST /rag/index", "POST", "/api/ai/rag/index", None, 60, "C"),
        ("POST /rag/search", "POST", "/api/ai/rag/search", {"query": "robbery", "top_k": 3}, 30, "B"),
        ("GET /rag/stats", "GET", "/api/ai/rag/stats", None, 30, "B"),
        ("GET /rag/citations/full-validate", "GET", "/api/ai/rag/citations/full-validate", None, 30, "B"),
        # Search
        (
            "POST /search/expand",
            "POST",
            "/api/ai/search/expand",
            {"query": "robbery bangalore"},
            90,
            "B",
        ),
        (
            "POST /search/rewrite",
            "POST",
            "/api/ai/search/rewrite",
            {"query": "robbery bangalore"},
            90,
            "B",
        ),
        (
            "POST /search/rerank",
            "POST",
            "/api/ai/search/rerank",
            {"query": "robbery", "results": [{"id": "1", "text": "night robbery case"}]},
            90,
            "B",
        ),
        (
            "POST /search/intelligent",
            "POST",
            "/api/ai/search/intelligent",
            {"query": "robbery", "top_k": 3, "use_rewrite": False, "use_expand": False, "use_rerank": False},
            90,
            "B",
        ),
        ("POST /search/similar", "POST", "/api/ai/search/similar", {"case_id": 1, "top_k": 3}, 60, "C"),
        (
            "POST /search/cross-district",
            "POST",
            "/api/ai/search/cross-district",
            {"query": "robbery", "districts": ["Bengaluru"], "top_k": 5},
            60,
            "C",
        ),
        ("GET /search/stats", "GET", "/api/ai/search/stats", None, 30, "B"),
        # Identity
        ("POST /identity/match", "POST", "/api/ai/identity/match", {"name1": "Karthik", "name2": "Karthick"}, 30, "A"),
        (
            "POST /identity/match/batch",
            "POST",
            "/api/ai/identity/match/batch",
            {"name1": "Ravi", "name2": "Ravee"},
            30,
            "B",
        ),
        (
            "POST /identity/transliterate",
            "POST",
            "/api/ai/identity/transliterate",
            {"text": "Karthik", "target": "kannada"},
            30,
            "A",
        ),
        (
            "POST /identity/duplicates",
            "POST",
            "/api/ai/identity/duplicates",
            {"records": [{"id": "1", "name": "Ravi"}, {"id": "2", "name": "Ravee"}], "id_key": "id"},
            30,
            "B",
        ),
        (
            "POST /identity/resolve",
            "POST",
            "/api/ai/identity/resolve",
            {"mention": "Ravi", "candidates": [{"id": "1", "name": "Ravi Kumar"}, {"id": "2", "name": "Ravee"}]},
            30,
            "B",
        ),
        (
            "POST /identity/merge",
            "POST",
            "/api/ai/identity/merge",
            {"primary": {"id": "1", "name": "Ravi"}, "secondary": {"id": "2", "name": "Ravee"}, "entity_type": "person"},
            30,
            "B",
        ),
        (
            "POST /identity/aliases",
            "POST",
            "/api/ai/identity/aliases",
            {"name": "Ravi", "all_names": ["Ravi", "Ravee", "Ravi Kumar"]},
            30,
            "B",
        ),
        ("GET /identity/stats", "GET", "/api/ai/identity/stats", None, 30, "B"),
        # Knowledge
        ("POST /knowledge/build", "POST", "/api/ai/knowledge/build", None, 60, "C"),
        (
            "POST /knowledge/query",
            "POST",
            "/api/ai/knowledge/query",
            {"query_type": "search", "node_id": "test"},
            30,
            "B",
        ),
        (
            "POST /knowledge/network",
            "POST",
            "/api/ai/knowledge/network",
            {"query_type": "clusters"},
            30,
            "B",
        ),
        (
            "POST /knowledge/discover",
            "POST",
            "/api/ai/knowledge/discover",
            {"query_type": "importance", "node_id": "n1"},
            30,
            "B",
        ),
        (
            "POST /knowledge/timeline",
            "POST",
            "/api/ai/knowledge/timeline",
            {"query_type": "bursts"},
            30,
            "B",
        ),
        (
            "POST /knowledge/analyze",
            "POST",
            "/api/ai/knowledge/analyze",
            {"query_type": "centrality"},
            30,
            "B",
        ),
        ("GET /knowledge/stats", "GET", "/api/ai/knowledge/stats", None, 30, "B"),
        # Reasoning
        (
            "POST /reasoning/chain",
            "POST",
            "/api/ai/reasoning/chain",
            {"hypothesis": "Suspect involved", "evidence": evidence()},
            30,
            "B",
        ),
        (
            "POST /reasoning/evidence",
            "POST",
            "/api/ai/reasoning/evidence",
            {"evidence": evidence(), "hypothesis": "Suspect involved"},
            30,
            "B",
        ),
        (
            "POST /reasoning/confidence",
            "POST",
            "/api/ai/reasoning/confidence",
            {"chain": {"steps": [], "hypothesis": "x"}},
            30,
            "B",
        ),
        (
            "POST /reasoning/analyze",
            "POST",
            "/api/ai/reasoning/analyze",
            {"hypothesis": "Suspect involved in robbery", "evidence": evidence()},
            120,
            "B",
        ),
        (
            "POST /reasoning/explain",
            "POST",
            "/api/ai/reasoning/explain",
            {"hypothesis": "Suspect involved", "evidence": evidence()},
            120,
            "B",
        ),
        # Predict
        (
            "POST /predict/forecast",
            "POST",
            "/api/ai/predict/forecast",
            {"historical": [{"count": 1}, {"count": 2}, {"count": 3}, {"count": 5}, {"count": 4}], "periods_ahead": 1},
            30,
            "B",
        ),
        (
            "POST /predict/hotspots",
            "POST",
            "/api/ai/predict/hotspots",
            {"crimes": [{"lat": 12.97, "lng": 77.59, "type": "robbery"}], "top_n": 3},
            30,
            "B",
        ),
        (
            "POST /predict/recidivism",
            "POST",
            "/api/ai/predict/recidivism",
            {"profile": {"prior_arrests": 2, "age": 30}},
            30,
            "B",
        ),
        (
            "POST /predict/risk",
            "POST",
            "/api/ai/predict/risk",
            {"profile": {"prior_arrests": 1, "violence": True}},
            30,
            "B",
        ),
        (
            "POST /predict/mo-similarity",
            "POST",
            "/api/ai/predict/mo-similarity",
            {"mo1": "night entry two wheeler", "mo2": "night break-in scooter"},
            30,
            "B",
        ),
        (
            "POST /predict/cases",
            "POST",
            "/api/ai/predict/cases",
            {"case": {"type": "robbery"}, "all_cases": [{"id": "1", "type": "robbery"}]},
            30,
            "B",
        ),
        ("GET /predict/stats", "GET", "/api/ai/predict/stats", None, 30, "B"),
        # Language
        ("POST /language/stt", "POST", "/api/ai/language/stt", {"audio_text": "hello", "language": "en"}, 30, "B"),
        ("POST /language/tts", "POST", "/api/ai/language/tts", {"text": "hello", "language": "en"}, 30, "B"),
        (
            "POST /language/translate",
            "POST",
            "/api/ai/language/translate",
            {"text": "hello", "source_lang": "en", "target_lang": "kn"},
            30,
            "B",
        ),
        (
            "POST /language/kanglish",
            "POST",
            "/api/ai/language/kanglish",
            {"text": "nanna hesaru ravi", "target": "english"},
            30,
            "A",
        ),
        (
            "POST /language/normalize",
            "POST",
            "/api/ai/language/normalize",
            {"query": "show robbery cases in bangalore"},
            30,
            "A",
        ),
        ("GET /language/stats", "GET", "/api/ai/language/stats", None, 30, "B"),
        # Embeddings
        (
            "POST /embeddings/embed",
            "POST",
            "/api/ai/embeddings/embed",
            {"text": "FIR robbery night entry", "domain": "fir", "item_id": "t1"},
            60,
            "A",
        ),
        (
            "POST /embeddings/batch",
            "POST",
            "/api/ai/embeddings/batch",
            {"texts": ["a", "b"], "domain": "fir"},
            60,
            "B",
        ),
        (
            "POST /embeddings/search",
            "POST",
            "/api/ai/embeddings/search",
            {"query": "robbery", "domain": "fir", "top_k": 3},
            60,
            "B",
        ),
        ("GET /embeddings/stats", "GET", "/api/ai/embeddings/stats", None, 30, "B"),
        # Workflows
        (
            "POST /workflows/run",
            "POST",
            "/api/ai/workflows/run",
            {"workflow": "investigation", "inputs": {"query": "test"}},
            180,
            "B",
        ),
        # Models registry
        ("GET /models/registry", "GET", "/api/ai/models/registry", None, 30, "B"),
        ("GET /models/registry/conversation", "GET", "/api/ai/models/registry/conversation", None, 30, "B"),
        ("GET /models/config", "GET", "/api/ai/models/config", None, 30, "B"),
        (
            "POST /models/registry",
            "POST",
            "/api/ai/models/registry",
            {"name": "test-model", "model_type": "conversation", "provider": "openrouter", "model_name": "meta-llama/llama-3.1-8b-instruct"},
            30,
            "B",
        ),
        # Monitor
        ("GET /monitor/latency", "GET", "/api/ai/monitor/latency", None, 30, "B"),
        ("GET /monitor/tokens", "GET", "/api/ai/monitor/tokens", None, 30, "B"),
        ("GET /monitor/hallucination", "GET", "/api/ai/monitor/hallucination", None, 30, "B"),
        ("GET /monitor/tools", "GET", "/api/ai/monitor/tools", None, 30, "B"),
        ("GET /monitor/accuracy", "GET", "/api/ai/monitor/accuracy", None, 30, "B"),
        ("GET /monitor/confidence", "GET", "/api/ai/monitor/confidence", None, 30, "B"),
        ("GET /monitor/cost", "GET", "/api/ai/monitor/cost", None, 30, "B"),
        (
            "POST /monitor/feedback",
            "POST",
            "/api/ai/monitor/feedback",
            {"rating": 5, "query": "validation ping", "response": "ok", "session_id": "full-validate", "comment": "ok"},
            30,
            "B",
        ),
        ("GET /monitor/feedback", "GET", "/api/ai/monitor/feedback", None, 30, "B"),
        ("GET /monitor/dashboard", "GET", "/api/ai/monitor/dashboard", None, 30, "B"),
        ("GET /monitor/summary", "GET", "/api/ai/monitor/summary", None, 30, "B"),
        # Backend-dependent tool samples
        (
            "POST /tools/invoke:crime_search",
            "POST",
            "/api/ai/tools/invoke",
            {"tool": "crime_search", "params": {"query": "robbery"}},
            30,
            "C",
        ),
        (
            "POST /tools/invoke:similar_cases",
            "POST",
            "/api/ai/tools/invoke",
            {"tool": "similar_cases", "params": {"case_id": "1"}},
            30,
            "C",
        ),
    ]

    # Fix paths for docs which is not under /api/ai
    out = []
    for name, method, path, body, timeout, tier in cases:
        if path == "/docs":
            url_path = "/docs"
        else:
            url_path = path
        out.append(
            {
                "name": name,
                "method": method,
                "path": url_path,
                "body": body,
                "timeout": timeout,
                "tier": tier,
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=BASE_DEFAULT)
    parser.add_argument("--skip-llm-heavy", action="store_true", help="Skip long LLM calls")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    cases = build_cases(base)
    if args.skip_llm_heavy:
        skip = {"POST /chat", "POST /reasoning/analyze", "POST /reasoning/explain", "POST /workflows/run",
                "POST /search/expand", "POST /search/rewrite", "POST /search/rerank", "POST /search/intelligent"}
        cases = [c for c in cases if c["name"] not in skip]

    # After embed, add similarity using returned vector
    print(f"Full validation against: {base}")
    print("=" * 88)

    results = []
    embed_vec = None

    for case in cases:
        url = f"{base}{case['path']}"
        # special: embeddings similarity needs a vector from prior embed
        body = case["body"]
        status, payload, elapsed = request(case["method"], url, body, timeout=case["timeout"])

        if case["name"] == "POST /embeddings/embed" and ok(status, payload):
            try:
                embed_vec = payload["data"]["embedding"]
            except Exception:
                embed_vec = None

        # Inject similarity test dynamically after embed
        passed = ok(status, payload)
        expected_backend = case["name"] in BACKEND_DEPENDENT or case["tier"] == "C"

        if expected_backend and not passed:
            mark = "BLOCK"
            outcome = "expected (needs backend)"
        elif passed:
            mark = "PASS"
            outcome = ""
        else:
            mark = "FAIL"
            detail = payload
            if isinstance(payload, dict):
                detail = payload.get("detail") or payload.get("error") or payload.get("data") or payload
            outcome = str(detail)[:100]

        print(f"{mark:5} T{case['tier']} {case['method']:6} {case['name'][:42]:42} {status:3} {elapsed:6.1f}s {outcome}")
        results.append(
            {
                "name": case["name"],
                "tier": case["tier"],
                "mark": mark,
                "status": status,
                "elapsed": elapsed,
                "outcome": outcome,
            }
        )

        if case["name"] == "POST /embeddings/embed" and embed_vec and len(embed_vec) >= 2:
            # run similarity immediately
            sim_body = {"embedding1": embed_vec[: min(32, len(embed_vec))], "embedding2": embed_vec[: min(32, len(embed_vec))]}
            # pad if needed - similarity needs same length full vectors
            sim_body = {"embedding1": embed_vec, "embedding2": embed_vec}
            st, pl, el = request("POST", f"{base}/api/ai/embeddings/similarity", sim_body, 30)
            p = ok(st, pl)
            mk = "PASS" if p else "FAIL"
            out = "" if p else str(pl)[:80]
            print(f"{mk:5} TB {'POST':6} {'POST /embeddings/similarity':42} {st:3} {el:6.1f}s {out}")
            results.append({"name": "POST /embeddings/similarity", "tier": "B", "mark": mk, "status": st, "elapsed": el, "outcome": out})

    print("=" * 88)
    passed = sum(1 for r in results if r["mark"] == "PASS")
    blocked = sum(1 for r in results if r["mark"] == "BLOCK")
    failed = sum(1 for r in results if r["mark"] == "FAIL")
    print(f"PASS={passed}  BLOCK(backend)={blocked}  FAIL={failed}  TOTAL={len(results)}")

    fails = [r for r in results if r["mark"] == "FAIL"]
    if fails:
        print("\nUnexpected failures:")
        for r in fails:
            print(f"  - {r['name']}: {r['status']} {r['outcome']}")

    # Write report
    report_path = "docs/APPSAIL_VALIDATION_REPORT.md"
    try:
        lines = [
            "# AppSail full endpoint validation",
            "",
            f"**Base URL:** `{base}`",
            f"**When:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"| PASS | BLOCK (backend) | FAIL | TOTAL |",
            f"|------|-----------------|------|-------|",
            f"| {passed} | {blocked} | {failed} | {len(results)} |",
            "",
            "| Result | Tier | Endpoint | Status | Time | Notes |",
            "|--------|------|----------|--------|------|-------|",
        ]
        for r in results:
            notes = (r["outcome"] or "").replace("|", "/")
            lines.append(f"| {r['mark']} | {r['tier']} | `{r['name']}` | {r['status']} | {r['elapsed']:.1f}s | {notes} |")
        lines.append("")
        lines.append("## Interpretation")
        lines.append("")
        lines.append("- **PASS** — works on AppSail alone (OpenRouter + in-process logic).")
        lines.append("- **BLOCK** — needs `BACKEND_URL` (CrimeMatrix backend not deployed yet).")
        lines.append("- **FAIL** — unexpected; investigate.")
        open(report_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"\nReport written: ai-services/{report_path}")
    except Exception as e:
        print(f"Could not write report: {e}")

    return 1 if failed else 0


if __name__ == "__main__":
    # Ensure we run from ai-services for report path
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.exit(main())
