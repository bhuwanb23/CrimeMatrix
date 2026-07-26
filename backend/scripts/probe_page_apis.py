"""Probe every frontend-page API for empty live data."""
from __future__ import annotations

import json
import urllib.error
import urllib.request

BASE = "https://crimematrix-backend-50044181811.development.catalystappsail.in"

# Seed IDs from prior live lists (updated at runtime when possible)
IDS = {
    "crime_id": "46575000000051001",
    "case_id": "46575000000050084",
    "investigation_id": "46575000000051056",
    "suspect_id": "46575000000051043",
    "criminal_id": "46575000000051042",
    "district_id": "46575000000050045",
}

# page -> GETs used by UI (POST detect/generate probed separately as soft)
PAGE_GETS = {
    "dashboard": [
        "/api/v1/statistics",
        "/api/v1/analytics-dashboard/stats",
        "/api/v1/analytics-dashboard/summary",
        "/api/v1/analytics/trends/crimes?period=daily",
        "/api/v1/analytics/trends/resolution",
        "/api/v1/analytics/counts/by-type",
        "/api/v1/analytics/counts/by-district",
        "/api/v1/analytics/counts/by-status",
        "/api/v1/analytics/timeseries/activity",
        "/api/v1/investigations/",
        "/api/v1/recommendations/dashboard",
        "/api/v1/recommendations/all?status=active&limit=20",
        "/api/v1/early-warning/alerts",
        "/api/v1/intelligence-timeline/?limit=8",
    ],
    "cases_search": [
        "/api/v1/crimes/?page=1&page_size=20",
        "/api/v1/search/district/districts",
        "/api/v1/search/suggestions?q=theft",
        "/api/v1/suspects/?page=1&page_size=20",
    ],
    "case_detail": [
        "/api/v1/crimes/{crime_id}",
        "/api/v1/cases/{case_id}",
        "/api/v1/cases/{case_id}/complainant",
        "/api/v1/cases/{case_id}/victims",
        "/api/v1/cases/{case_id}/act-sections",
        "/api/v1/cases/{case_id}/accused",
        "/api/v1/cases/{case_id}/arrest-surrender",
        "/api/v1/cases/{case_id}/chargesheet",
        "/api/v1/similar-cases/{case_id}?top_k=5",
        "/api/v1/fir-intelligence/suggestions/{crime_id}",
    ],
    "analytics": [
        "/api/v1/analytics/stats/overview",
        "/api/v1/analytics-dashboard/alerts",
        "/api/v1/analytics-dashboard/forecasts",
        "/api/v1/analytics-dashboard/high-risk",
        "/api/v1/analytics-dashboard/priority",
        "/api/v1/evaluation/stats",
        "/api/v1/evaluation/results",
        "/api/v1/evaluation/accuracy-trend",
        "/api/v1/evaluation/feedback",
    ],
    "intelligence": [
        "/api/v1/intelligence/summary",
        "/api/v1/trends/daily",
        "/api/v1/trends/seasonal?days=90",
        "/api/v1/hotspots/",
        "/api/v1/hotspots/risk-map",
        "/api/v1/behavior/profiles",
        "/api/v1/behavior/risk-assessment",
        "/api/v1/behavior/stats",
        "/api/v1/repeat-offenders/",
        "/api/v1/repeat-offenders/stats",
        "/api/v1/mo/profiles",
        "/api/v1/mo/stats",
        "/api/v1/cross-district/matches",
        "/api/v1/cross-district/stats",
        "/api/v1/evidence-linking/links",
        "/api/v1/evidence-linking/stats",
    ],
    "patterns_timeline": [
        "/api/v1/patterns/",
        "/api/v1/patterns/stats",
        "/api/v1/criminal-timeline/",
        "/api/v1/criminal-timeline/stats",
        "/api/v1/intelligence-timeline/stats",
    ],
    "predictions": [
        "/api/v1/predictions/stats",
        "/api/v1/predictions/models",
        "/api/v1/predictions/?page=1&page_size=20",
        "/api/v1/predictions/forecast/seasonal?days=365",
    ],
    "early_warning": [
        "/api/v1/early-warning/alerts?status=active",
        "/api/v1/early-warning/stats",
    ],
    "suspect_risk": [
        "/api/v1/suspect-risk/stats",
        "/api/v1/suspect-risk/rankings?limit=20",
        "/api/v1/suspect-risk/scores/{suspect_id}",
        "/api/v1/suspect-risk/factors/{suspect_id}",
        "/api/v1/suspects/{suspect_id}",
        "/api/v1/criminal-timeline/suspect/Suspect1?days=90",
    ],
    "priorities_proactive": [
        "/api/v1/priorities/stats",
        "/api/v1/priorities/rankings?limit=20",
        "/api/v1/priorities/workload",
        "/api/v1/proactive/stats",
        "/api/v1/proactive/activity?limit=20",
    ],
    "graph_maps": [
        "/api/v1/graph/nodes",
        "/api/v1/graph/edges",
        "/api/v1/graph/stats",
        "/api/v1/maps/crime-markers",
        "/api/v1/maps/districts",
        "/api/v1/maps/heatmap?days=30",
        "/api/v1/maps/hotspots",
        "/api/v1/maps/stations",
        "/api/v1/maps/routes",
        "/api/v1/maps/stats",
    ],
    "investigations": [
        "/api/v1/investigations/",
        "/api/v1/investigations/recent?limit=10",
        "/api/v1/investigations/{investigation_id}",
        "/api/v1/notes/investigation/{investigation_id}",
        "/api/v1/timeline/investigation/{investigation_id}",
        "/api/v1/attachments/investigation/{investigation_id}",
        "/api/v1/priorities/rankings?limit=10",
    ],
    "reports_settings": [
        "/api/v1/reports/templates",
        "/api/v1/reports/queue",
        "/api/v1/config",
        "/api/v1/criminals/?page=1&page_size=20",
        "/api/v1/officers/?page=1&page_size=20",
        "/api/v1/stations/?page=1&page_size=20",
        "/api/v1/persons/?page=1&page_size=20",
        "/api/v1/vehicles/?page=1&page_size=20",
        "/api/v1/locations/?page=1&page_size=20",
    ],
}

POSTS = [
    ("POST", "/api/v1/search/", {"query": "theft"}),
    ("POST", "/api/v1/search/semantic", {"query": "robbery"}),
    ("POST", "/api/v1/hotspots/detect", {}),
    ("POST", "/api/v1/patterns/detect", {}),
    ("POST", "/api/v1/cross-district/detect", {}),
    ("POST", "/api/v1/evidence-linking/detect", {}),
    ("POST", "/api/v1/early-warning/detect", {}),
    ("POST", "/api/v1/predictions/forecast", {"days": 7}),
    ("POST", "/api/v1/graph/build-from-crimes", {}),
    ("POST", "/api/v1/proactive/scan", {}),
    ("POST", "/api/v1/suspect-risk/batch-score", {}),
    ("POST", "/api/v1/priorities/batch-score", {}),
    ("POST", "/api/v1/repeat-offenders/analyze", {}),
]


def resolve(path: str) -> str:
    out = path
    for k, v in IDS.items():
        out = out.replace("{" + k + "}", str(v))
    return out


def is_empty(data) -> bool:
    if data in (None, [], {}):
        return True
    if isinstance(data, list):
        return len(data) == 0
    if not isinstance(data, dict):
        return False
    if "items" in data and isinstance(data["items"], list):
        return len(data["items"]) == 0 and int(data.get("total") or 0) == 0
    if "recommendations" in data and isinstance(data["recommendations"], list):
        return len(data["recommendations"]) == 0
    if "entries" in data and isinstance(data["entries"], list):
        return len(data["entries"]) == 0 and int(data.get("total_count") or 0) == 0
    if "overview" in data and isinstance(data["overview"], dict):
        return not any(isinstance(v, (int, float)) and v > 0 for v in data["overview"].values())
    if "totals" in data and isinstance(data["totals"], dict):
        if any(int(v or 0) > 0 for v in data["totals"].values()):
            return False
    # numeric-only zeros
    nums = [v for v in data.values() if isinstance(v, (int, float))]
    lists = [v for v in data.values() if isinstance(v, list)]
    dicts = [v for v in data.values() if isinstance(v, dict)]
    nested = []
    for d in dicts:
        nested.extend(x for x in d.values() if isinstance(x, (int, float)))
    all_nums = nums + nested
    if all_nums and all(v == 0 for v in all_nums) and all(len(v) == 0 for v in lists):
        return True
    if not all_nums and lists and all(len(v) == 0 for v in lists) and not dicts:
        return True
    # markers/features geojson
    if "features" in data and isinstance(data["features"], list):
        return len(data["features"]) == 0
    if "markers" in data and isinstance(data["markers"], list):
        return len(data["markers"]) == 0
    if "nodes" in data and isinstance(data["nodes"], list):
        return len(data["nodes"]) == 0
    if "edges" in data and isinstance(data["edges"], list) and "nodes" not in data:
        return len(data["edges"]) == 0
    return False


def summarize(data) -> str:
    try:
        if isinstance(data, list):
            return f"list:{len(data)}"
        if isinstance(data, dict):
            bits = {}
            for k, v in list(data.items())[:10]:
                if isinstance(v, list):
                    bits[k] = f"list:{len(v)}"
                elif isinstance(v, dict):
                    bits[k] = f"dict:{len(v)}"
                elif isinstance(v, (int, float, str, bool)) or v is None:
                    bits[k] = v
            return json.dumps(bits)[:220]
        return repr(data)[:120]
    except Exception:
        return "?"


def request(method: str, path: str, body=None):
    url = BASE + path
    data = None
    headers = {"User-Agent": "page-probe"}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "text/plain;charset=UTF-8"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", "replace")
            try:
                payload = json.loads(raw)
            except Exception:
                return resp.status, raw[:200], False
            return resp.status, payload, False
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except Exception:
            payload = raw[:200]
        return e.code, payload, True
    except Exception as e:
        return 0, str(e), True


def main():
    # refresh seed ids
    for path, key, nest in [
        ("/api/v1/crimes/?page=1&page_size=1", "crime_id", True),
        ("/api/v1/cases/?page=1&page_size=1", "case_id", True),
        ("/api/v1/investigations/", "investigation_id", True),
        ("/api/v1/suspects/?page=1&page_size=1", "suspect_id", True),
    ]:
        st, payload, _ = request("GET", path)
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data")
            items = None
            if isinstance(data, dict) and isinstance(data.get("items"), list):
                items = data["items"]
            elif isinstance(data, list):
                items = data
            if items:
                IDS[key] = items[0].get("id")

    print("IDS", IDS)
    empty = []
    has = []
    errors = []

    for page, paths in PAGE_GETS.items():
        print(f"\n=== {page} ===")
        for path in paths:
            resolved = resolve(path)
            st, payload, err = request("GET", resolved)
            if err or st >= 400 or st == 0:
                print(f"ERR  {st} GET {resolved} {str(payload)[:120]}")
                errors.append((page, "GET", resolved, st))
                continue
            data = payload.get("data") if isinstance(payload, dict) else payload
            empty_flag = is_empty(data)
            tag = "EMPTY" if empty_flag else "HAS"
            print(f"{tag} {st} GET {resolved} :: {summarize(data)}")
            (empty if empty_flag else has).append((page, "GET", resolved))

    print("\n=== POSTS ===")
    for method, path, body in POSTS:
        st, payload, err = request(method, path, body)
        if err or st >= 400 or st == 0:
            print(f"ERR  {st} {method} {path} {str(payload)[:120]}")
            errors.append(("post", method, path, st))
            continue
        data = payload.get("data") if isinstance(payload, dict) else payload
        empty_flag = is_empty(data)
        # detect endpoints that return {matches_found:0} still count as soft-empty for UX
        if isinstance(data, dict):
            if data.get("matches_found") == 0 and data.get("links_found") == 0:
                empty_flag = True
            if "alerts" in data and isinstance(data["alerts"], list) and len(data["alerts"]) == 0:
                empty_flag = True
            if "patterns" in data and isinstance(data["patterns"], list) and len(data["patterns"]) == 0:
                empty_flag = True
            if "hotspots" in data and isinstance(data["hotspots"], list) and len(data["hotspots"]) == 0:
                empty_flag = True
        tag = "EMPTY" if empty_flag else "HAS"
        print(f"{tag} {st} {method} {path} :: {summarize(data)}")
        (empty if empty_flag else has).append(("post", method, path))

    print("\n=== SUMMARY ===")
    print(f"HAS={len(has)} EMPTY={len(empty)} ERR={len(errors)}")
    print("EMPTY:")
    for row in empty:
        print(" ", row)
    print("ERR:")
    for row in errors:
        print(" ", row)


if __name__ == "__main__":
    main()
