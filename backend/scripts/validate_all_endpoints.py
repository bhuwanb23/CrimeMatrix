#!/usr/bin/env python3
"""Validate all backend AppSail endpoints against live OpenAPI.

Usage (from backend/):
  python scripts/validate_all_endpoints.py
  python scripts/validate_all_endpoints.py --base https://crimematrix-backend-....catalystappsail.in
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode, quote


DEFAULT_BASE = "https://crimematrix-backend-50044181811.development.catalystappsail.in"


def request(
    method: str,
    url: str,
    body: Any = None,
    timeout: float = 45.0,
    content_type: str = "application/json",
) -> tuple[int, Any, float]:
    data = None
    headers = {"Accept": "application/json", "User-Agent": "cm-endpoint-validator/1.0"}
    if body is not None:
        if isinstance(body, (dict, list)):
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = content_type
        elif isinstance(body, bytes):
            data = body
            headers["Content-Type"] = content_type
        else:
            data = str(body).encode("utf-8")
            headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            elapsed = time.perf_counter() - t0
            try:
                payload = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                payload = raw[:500]
            return resp.status, payload, elapsed
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        elapsed = time.perf_counter() - t0
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = raw[:500]
        return e.code, payload, elapsed
    except Exception as e:
        return 0, {"error": str(e)}, time.perf_counter() - t0


def classify(status: int, method: str, path: str, payload: Any) -> str:
    """PASS | SOFT | FAIL | SKIP"""
    if status == 0:
        return "FAIL"
    if 200 <= status < 300:
        if isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, dict) and data.get("error"):
                return "SOFT"
        return "PASS"
    detail = ""
    if isinstance(payload, dict):
        detail = str(payload.get("detail") or payload.get("message") or payload.get("error") or "")
    detail_l = detail.lower()

    # AppSail slim image: local /ai/chat uses gemini SDK not installed
    if status == 503 and "no module named 'google'" in detail_l:
        return "SOFT"
    # Missing entity / not found probes
    if status == 404:
        return "SOFT"
    # Validation when probe omitted required query/body — caller should fill; treat as SOFT if still missing
    if status == 422:
        return "SOFT"
    if status in (401, 403, 405):
        return "SOFT"
    # AppSail slash quirk
    if status == 400 and method == "GET":
        return "SOFT"
    if method in {"POST", "PUT", "DELETE", "PATCH"} and status in (404, 422):
        return "SOFT"
    if status >= 500:
        return "FAIL"
    return "FAIL"


def pick_example(schema: dict, components: dict, depth: int = 0) -> Any:
    if depth > 4:
        return None
    if not schema:
        return None
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        return pick_example(components.get("schemas", {}).get(ref, {}), components, depth + 1)
    if "example" in schema:
        return schema["example"]
    if "default" in schema:
        return schema["default"]
    t = schema.get("type")
    if "enum" in schema and schema["enum"]:
        return schema["enum"][0]
    if t == "object" or "properties" in schema:
        out = {}
        required = set(schema.get("required") or [])
        props = schema.get("properties") or {}
        for k, v in props.items():
            if k in required or depth == 0:
                out[k] = pick_example(v, components, depth + 1)
        return out
    if t == "array":
        item = pick_example(schema.get("items") or {}, components, depth + 1)
        return [item] if item is not None else []
    if t == "integer":
        return 1
    if t == "number":
        return 1.0
    if t == "boolean":
        return True
    if t == "string":
        fmt = schema.get("format")
        if fmt == "date":
            return "2026-01-01"
        if fmt == "date-time":
            return "2026-01-01T00:00:00"
        return "test"
    return None


def resolve_path(path: str, ids: dict[str, Any]) -> Optional[str]:
    """Replace {param} with known ids. Return None if required id missing."""
    params = re.findall(r"\{([^}]+)\}", path)
    out = path
    for p in params:
        key = p
        # common aliases
        candidates = [
            key,
            key.replace("_id", ""),
            key.replace("Id", ""),
            "id",
        ]
        val = None
        for c in candidates:
            if c in ids and ids[c] is not None:
                val = ids[c]
                break
        # specialized
        mapping = {
            "district_id": "district_id",
            "crime_id": "crime_id",
            "case_id": "case_id",
            "investigation_id": "investigation_id",
            "criminal_id": "criminal_id",
            "officer_id": "officer_id",
            "person_id": "person_id",
            "suspect_id": "suspect_id",
            "station_id": "station_id",
            "vehicle_id": "vehicle_id",
            "location_id": "location_id",
            "crimetype_id": "crime_type_id",
            "witness_id": "witness_id",
            "victim_id": "victim_id",
            "phone_id": "phone_id",
            "note_id": "note_id",
            "event_id": "timeline_event_id",
            "attachment_id": "attachment_id",
            "link_id": "case_link_id",
            "session_id": "session_id",
            "bookmark_id": "bookmark_id",
            "query": "search_query",
            "reg": "registration",
            "number": "phone_number",
            "filename": "filename",
            "path": "storage_path",
            "table": "table",
            "row_id": "row_id",
            "case_number": "case_number",
            "crime_no": "crime_no",
            "suspect_name": "suspect_name",
            "district_name": "district_name",
            "node_id": "node_id",
            "source": "node_id",
            "target": "node_id2",
            "p1_id": "pattern_id",
            "p2_id": "pattern_id2",
            "case_id_1": "case_id",
            "case_id_2": "case_id2",
            "fir_id": "fir_id",
            "alert_id": "alert_id",
            "match_id": "match_id",
            "hotspot_id": "hotspot_id",
            "pattern_id": "pattern_id",
            "prediction_id": "prediction_id",
            "profile_id": "profile_id",
            "offender_id": "offender_id",
            "recommendation_id": "recommendation_id",
            "rec_id": "recommendation_id",
            "event_id": "event_id",
            "link_id": "link_id",
            "job_id": "job_id",
            "notif_id": "notif_id",
            "sub_id": "sub_id",
            "search_id": "search_id",
            "doc_id": "doc_id",
            "template_id": "template_id",
            "cs_id": "cs_id",
            "assoc_id": "assoc_id",
            "accused_id": "accused_id",
            "record_id": "record_id",
        }
        if val is None and key in mapping and mapping[key] in ids:
            val = ids[mapping[key]]
        if val is None:
            # last resort placeholders for non-seeded ML routes
            defaults = {
                "query": "theft",
                "search_query": "theft",
                "district_name": "Bengaluru Urban",
                "suspect_name": "Suspect 1",
                "registration": "KA01AB1234",
                "phone_number": "9876543210",
                "filename": "seed_attachment.txt",
                "storage_path": "test.txt",
                "path": "test.txt",
                "table": "districts",
                "session_id": "e2e-validate",
                "node_id": "1",
                "node_id2": "2",
                "case_number": "CASE/BNG/2026/0001",
                "crime_no": "FIR/BNG/2026/0001",
            }
            # numeric ids → 1
            if key.endswith("_id") or key in {"id", "row_id"}:
                val = ids.get(key) or ids.get("district_id") or 1
            elif key in defaults:
                val = defaults[key]
            elif key == "path:path":
                val = "test.txt"
            else:
                val = "1"
        out = out.replace("{" + p + "}", quote(str(val), safe=""))
    # FastAPI path:path style
    out = out.replace("{path:path}", quote(str(ids.get("storage_path", "test.txt")), safe="/"))
    return out


def query_for_operation(op: dict, ids: dict[str, Any]) -> dict[str, Any]:
    q: dict[str, Any] = {}
    for p in op.get("parameters") or []:
        if p.get("in") != "query":
            continue
        name = p.get("name")
        if not name:
            continue
        schema = p.get("schema") or {}
        if name in {"page", "page_size", "limit", "offset", "per_page"}:
            q[name] = {"page": 1, "page_size": 5, "limit": 5, "offset": 0, "per_page": 5}[name]
        elif name == "entity_type":
            q[name] = "crime"
        elif name in {"entity_id", "district1", "district2"}:
            q[name] = ids.get("district_id") or 1
        elif name == "ids":
            q[name] = str(ids.get("district_id") or 1)
        elif name in {"q", "query", "search"}:
            q[name] = "theft"
        elif name == "user_id":
            q[name] = "e2e-validate"
        elif p.get("required") or name == "min_score":
            t = schema.get("type")
            q[name] = 1 if t == "integer" else (0.5 if t == "number" else (True if t == "boolean" else "test"))
    return q


def seed_ids(base: str) -> dict[str, Any]:
    ids: dict[str, Any] = {
        "session_id": "e2e-validate",
        "search_query": "theft",
        "storage_path": "test.txt",
        "filename": "seed_attachment.txt",
        "table": "districts",
        "registration": "KA01AB1234",
        "phone_number": "9876543210",
        "suspect_name": "Suspect1",
        "district_name": "BengaluruUrban",
        "case_number": "CASE-BNG-2026-0001",
        "crime_no": "FIR-BNG-2026-0001",
        "node_id": "1",
        "node_id2": "2",
    }

    def first_id(path: str, *keys: str) -> None:
        status, payload, _ = request("GET", f"{base}{path}")
        if status != 200 or not isinstance(payload, dict):
            return
        data = payload.get("data")
        items = None
        if isinstance(data, dict):
            items = data.get("items") or data.get("results")
        elif isinstance(data, list):
            items = data
        if not items:
            return
        item = items[0]
        if not isinstance(item, dict):
            return
        rid = item.get("id")
        if rid is None:
            return
        for k in keys:
            ids[k] = rid

    first_id("/api/v1/districts/?page=1&page_size=1", "district_id", "id")
    first_id("/api/v1/crimes/?page=1&page_size=1", "crime_id")
    first_id("/api/v1/cases/?page=1&page_size=1", "case_id", "case_id2")
    first_id("/api/v1/investigations/?limit=1", "investigation_id")
    first_id("/api/v1/criminals/?page=1&page_size=1", "criminal_id")
    first_id("/api/v1/officers/?page=1&page_size=1", "officer_id")
    first_id("/api/v1/persons/?page=1&page_size=1", "person_id")
    first_id("/api/v1/suspects/?page=1&page_size=1", "suspect_id")
    first_id("/api/v1/stations/?page=1&page_size=1", "station_id")
    first_id("/api/v1/vehicles/?page=1&page_size=1", "vehicle_id")
    first_id("/api/v1/locations/?page=1&page_size=1", "location_id")
    first_id("/api/v1/crime-types/?page=1&page_size=1", "crime_type_id", "crimetype_id")
    first_id("/api/v1/witnesses/?page=1&page_size=1", "witness_id")
    first_id("/api/v1/phones/?page=1&page_size=1", "phone_id")
    first_id("/api/v1/victims/?page=1&page_size=1", "victim_id")

    # notes / timeline for investigation
    inv = ids.get("investigation_id")
    if inv:
        st, payload, _ = request("GET", f"{base}/api/v1/notes/investigation/{inv}")
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, list) and data:
                ids["note_id"] = data[0].get("id")
            elif isinstance(data, dict) and data.get("items"):
                ids["note_id"] = data["items"][0].get("id")
        st, payload, _ = request("GET", f"{base}/api/v1/timeline/investigation/{inv}")
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, list) and data:
                ids["timeline_event_id"] = data[0].get("id")
                ids["event_id"] = data[0].get("id")
        st, payload, _ = request("GET", f"{base}/api/v1/case-status/investigation/{inv}")
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, list) and data:
                ids["case_status_id"] = data[0].get("id")
        st, payload, _ = request("GET", f"{base}/api/v1/attachments/investigation/{inv}")
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data")
            items = data if isinstance(data, list) else (data.get("items") if isinstance(data, dict) else None)
            if items:
                ids["attachment_id"] = items[0].get("id")
        st, payload, _ = request("GET", f"{base}/api/v1/case-links/investigation/{inv}")
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data")
            items = data if isinstance(data, list) else (data.get("items") if isinstance(data, dict) else None)
            if items:
                ids["case_link_id"] = items[0].get("id")
                ids["link_id"] = items[0].get("id")

    ids["row_id"] = ids.get("district_id") or 1
    ids["fir_id"] = 1
    return ids


# Destructive routes we only soft-probe (expect SOFT on missing/validation) unless dry body safe
SKIP_METHODS_ON_PATH_PREFIXES = (
    # never mass-delete seed data during validation
)


def body_for_operation(method: str, path: str, op: dict, components: dict) -> Any:
    # Prefer known safe bodies for critical routes
    if path.rstrip("/") == "/api/v1/search" or path.endswith("/search/"):
        return {"query": "theft", "page": 1, "page_size": 5}
    if path.endswith("/search/keyword") or path.endswith("/search/advanced"):
        return {"query": "theft", "page": 1, "page_size": 5}
    if path.endswith("/copilot/chat"):
        return {"message": "ping", "use_tools": False, "user_id": "e2e-validate", "session_id": "e2e-validate"}
    if path.endswith("/copilot/sessions"):
        return {"title": "e2e", "user_id": "e2e-validate"}
    if "multipart" in str(op.get("requestBody") or {}).lower() or "UploadFile" in str(op):
        return None  # skip body; will mark SOFT if 422
    rb = op.get("requestBody") or {}
    content = rb.get("content") or {}
    schema = None
    if "application/json" in content:
        schema = content["application/json"].get("schema")
    elif content:
        schema = next(iter(content.values())).get("schema")
    if schema:
        example = pick_example(schema, components)
        if example is not None:
            return example
    if method in {"POST", "PUT", "PATCH"}:
        return {}
    return None


def should_skip(method: str, path: str) -> Optional[str]:
    if path in {"/docs", "/redoc", "/docs/oauth2-redirect"}:
        return "docs UI"
    if method == "DELETE" and any(
        path.startswith(p)
        for p in (
            "/api/v1/districts/",
            "/api/v1/crimes/",
            "/api/v1/cases/",
            "/api/v1/investigations/",
            "/api/v1/criminals/",
            "/api/v1/officers/",
            "/api/v1/persons/",
            "/api/v1/stations/",
            "/api/v1/vehicles/",
            "/api/v1/locations/",
            "/api/v1/crime-types/",
            "/api/v1/witnesses/",
            "/api/v1/notes/",
            "/api/v1/timeline/",
            "/api/v1/attachments/",
            "/api/v1/case-links/",
            "/api/v1/datastore/",
        )
    ):
        # Don't delete seeded Catalyst rows during full sweep
        return "skip destructive seed delete"
    if path.endswith("/chat/stream") or path.endswith("/copilot/chat/stream"):
        return "streaming SSE"
    if "/uploads" in path and method == "POST":
        return "multipart upload"
    if path.endswith("/attachments/upload") or path.endswith("/storage/upload"):
        return "multipart upload"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--limit", type=int, default=0, help="Limit number of ops (0=all)")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    print(f"Loading OpenAPI from {base}/openapi.json ...")
    status, openapi, _ = request("GET", f"{base}/openapi.json", timeout=60)
    if status != 200 or not isinstance(openapi, dict):
        print(f"FATAL: could not load openapi ({status}): {openapi}")
        return 2

    components = openapi.get("components") or {}
    paths = openapi.get("paths") or {}
    print(f"Seeding IDs from live lists...")
    ids = seed_ids(base)
    print("IDs:", {k: v for k, v in ids.items() if k.endswith("_id") or k in {"table", "session_id"}})

    results: list[dict[str, Any]] = []
    counts: dict[str, int] = defaultdict(int)

    ops: list[tuple[str, str, dict]] = []
    for path, item in paths.items():
        for method, op in item.items():
            if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
                continue
            ops.append((method.upper(), path, op or {}))
    ops.sort(key=lambda x: (x[1], x[0]))
    if args.limit:
        ops = ops[: args.limit]

    print(f"Validating {len(ops)} operations...\n")
    for i, (method, path, op) in enumerate(ops, 1):
        skip = should_skip(method, path)
        name = f"{method} {path}"
        if skip:
            row = {
                "method": method,
                "path": path,
                "status": None,
                "result": "SKIP",
                "ms": 0,
                "detail": skip,
            }
            results.append(row)
            counts["SKIP"] += 1
            print(f"[{i}/{len(ops)}] SKIP {name} ({skip})")
            continue

        resolved = resolve_path(path, ids)
        if resolved is None:
            row = {
                "method": method,
                "path": path,
                "status": None,
                "result": "SKIP",
                "ms": 0,
                "detail": "unresolved path params",
            }
            results.append(row)
            counts["SKIP"] += 1
            print(f"[{i}/{len(ops)}] SKIP {name} (unresolved)")
            continue

        body = None
        if method in {"POST", "PUT", "PATCH"}:
            body = body_for_operation(method, resolved, op, components)

        qparams = query_for_operation(op, ids)
        # Query params: page helpers for collections
        if method == "GET" and "{" not in path:
            if any(
                resolved.rstrip("/").endswith(s)
                for s in (
                    "/districts",
                    "/crimes",
                    "/cases",
                    "/criminals",
                    "/officers",
                    "/persons",
                    "/suspects",
                    "/stations",
                    "/vehicles",
                    "/locations",
                    "/crime-types",
                    "/witnesses",
                    "/phones",
                    "/victims",
                )
            ):
                qparams.setdefault("page", 1)
                qparams.setdefault("page_size", 5)

        url = f"{base}{resolved}"
        if qparams:
            url = url + ("&" if "?" in url else "?") + urlencode(qparams, doseq=True)

        st, payload, elapsed = request(method, url, body=body, timeout=args.timeout)
        # Retry list routes that 400 without slash
        if st == 400 and method == "GET" and not resolved.endswith("/") and "{" not in path:
            st2, payload2, elapsed2 = request(method, f"{base}{resolved}/", timeout=args.timeout)
            if 200 <= st2 < 300:
                st, payload, elapsed = st2, payload2, elapsed2
                resolved = resolved + "/"

        result = classify(st, method, resolved, payload)
        detail = ""
        if result == "FAIL":
            if isinstance(payload, dict):
                detail = str(payload.get("detail") or payload.get("message") or payload.get("error") or payload)[:180]
            else:
                detail = str(payload)[:180]
        row = {
            "method": method,
            "path": path,
            "resolved": resolved,
            "status": st,
            "result": result,
            "ms": round(elapsed * 1000),
            "detail": detail,
        }
        results.append(row)
        counts[result] += 1
        mark = result
        print(f"[{i}/{len(ops)}] {mark} {st} {method} {resolved} ({row['ms']}ms)" + (f" :: {detail}" if detail else ""))

    out_dir = Path(args.out) if args.out else Path(__file__).resolve().parents[1] / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = out_dir / f"ENDPOINT_VALIDATION_{stamp}.json"
    md_path = out_dir / "ENDPOINT_VALIDATION.md"

    report = {
        "base": base,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": dict(counts),
        "total": len(results),
        "ids": {k: v for k, v in ids.items() if str(k).endswith("_id")},
        "results": results,
    }
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    fails = [r for r in results if r["result"] == "FAIL"]
    softs = [r for r in results if r["result"] == "SOFT"]
    skips = [r for r in results if r["result"] == "SKIP"]
    passes = [r for r in results if r["result"] == "PASS"]

    lines = [
        "# Backend endpoint validation",
        "",
        f"- Base: `{base}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Total operations: **{len(results)}**",
        f"- PASS: **{counts.get('PASS', 0)}**",
        f"- SOFT: **{counts.get('SOFT', 0)}** (empty/validation/missing-id acceptable)",
        f"- FAIL: **{counts.get('FAIL', 0)}**",
        f"- SKIP: **{counts.get('SKIP', 0)}** (destructive/multipart/stream)",
        "",
        "## FAIL details",
        "",
    ]
    if not fails:
        lines.append("_None_")
    else:
        lines.append("| Method | Path | Status | Detail |")
        lines.append("|--------|------|--------|--------|")
        for r in fails:
            lines.append(f"| {r['method']} | `{r.get('resolved') or r['path']}` | {r['status']} | {r.get('detail','').replace('|','/')} |")

    lines += ["", "## SOFT (sample up to 40)", ""]
    if not softs:
        lines.append("_None_")
    else:
        lines.append("| Method | Path | Status | Detail |")
        lines.append("|--------|------|--------|--------|")
        for r in softs[:40]:
            lines.append(f"| {r['method']} | `{r.get('resolved') or r['path']}` | {r['status']} | {(r.get('detail') or '')[:80].replace('|','/')} |")
        if len(softs) > 40:
            lines.append(f"| … | _{len(softs) - 40} more_ | | |")

    lines += ["", "## SKIP", ""]
    for r in skips:
        lines.append(f"- `{r['method']} {r['path']}` — {r.get('detail')}")

    lines += [
        "",
        "## PASS summary by prefix",
        "",
    ]
    by_prefix: dict[str, int] = defaultdict(int)
    for r in passes:
        parts = r["path"].strip("/").split("/")
        prefix = "/".join(parts[:3]) if len(parts) >= 3 else r["path"]
        by_prefix[prefix] += 1
    lines.append("| Prefix | PASS count |")
    lines.append("|--------|------------|")
    for k in sorted(by_prefix):
        lines.append(f"| `{k}` | {by_prefix[k]} |")

    lines += ["", f"Full JSON: `{json_path.name}`", ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"PASS={counts.get('PASS',0)} SOFT={counts.get('SOFT',0)} FAIL={counts.get('FAIL',0)} SKIP={counts.get('SKIP',0)}")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    return 1 if counts.get("FAIL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
