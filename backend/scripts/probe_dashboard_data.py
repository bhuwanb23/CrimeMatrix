"""Probe live backend payloads that the frontend dashboard consumes."""
from __future__ import annotations

import json
import urllib.request

BASE = "https://crimematrix-backend-50044181811.development.catalystappsail.in"

PATHS = [
    "/api/v1/statistics",
    "/api/v1/analytics-dashboard/stats",
    "/api/v1/analytics-dashboard/summary",
    "/api/v1/analytics/stats/overview",
    "/api/v1/analytics/counts/by-type",
    "/api/v1/analytics/counts/by-status",
    "/api/v1/analytics/counts/by-district",
    "/api/v1/analytics/timeseries/activity",
    "/api/v1/analytics/trends/crimes?period=daily",
    "/api/v1/analytics/trends/resolution",
    "/api/v1/investigations/",
    "/api/v1/districts/?page=1&page_size=3",
    "/api/v1/crimes/?page=1&page_size=3",
    "/api/v1/recommendations/all?status=active&limit=5",
    "/api/v1/early-warning/alerts?status=active",
    "/api/v1/intelligence-timeline/?limit=8",
    "/api/v1/recommendations/dashboard",
]


def summarize(data):
    if isinstance(data, dict):
        # look for numeric totals / empty lists
        totals = {}
        for k, v in data.items():
            if isinstance(v, (int, float)):
                totals[k] = v
            elif isinstance(v, list):
                totals[k] = f"list:{len(v)}"
            elif isinstance(v, dict):
                totals[k] = f"dict:{len(v)}"
        return json.dumps(totals)[:300], json.dumps(data)[:280]
    if isinstance(data, list):
        return f"list:{len(data)}", json.dumps(data[:1])[:280]
    return repr(data), ""


def main():
    empty = []
    ok = []
    for path in PATHS:
        try:
            with urllib.request.urlopen(BASE + path, timeout=45) as resp:
                payload = json.loads(resp.read().decode())
            data = payload.get("data")
            summary, sample = summarize(data)
            # heuristic: empty if all numeric zeros and lists empty
            is_empty = False
            if data in (None, [], {}):
                is_empty = True
            elif isinstance(data, dict):
                # Nested overview (dashboard summary)
                overview = data.get("overview") if isinstance(data.get("overview"), dict) else None
                if overview and any(isinstance(v, (int, float)) and v > 0 for v in overview.values()):
                    is_empty = False
                else:
                    nums = [v for v in data.values() if isinstance(v, (int, float))]
                    lists = [v for v in data.values() if isinstance(v, list)]
                    dicts = [v for v in data.values() if isinstance(v, dict)]
                    nested_nums = []
                    for d in dicts:
                        nested_nums.extend(v for v in d.values() if isinstance(v, (int, float)))
                    all_nums = nums + nested_nums
                    if all_nums and all(v == 0 for v in all_nums) and all(len(v) == 0 for v in lists):
                        is_empty = True
                    if not all_nums and lists and all(len(v) == 0 for v in lists):
                        is_empty = True
                    if "items" in data and isinstance(data["items"], list) and len(data["items"]) == 0:
                        if data.get("total", 0) == 0:
                            is_empty = True
                    if "recommendations" in data and isinstance(data["recommendations"], list):
                        is_empty = len(data["recommendations"]) == 0 and data.get("total_count", 0) == 0
                    if "entries" in data and isinstance(data["entries"], list):
                        is_empty = len(data["entries"]) == 0 and data.get("total_count", 0) == 0
                    # totals block with any positive counts
                    totals = data.get("totals")
                    if isinstance(totals, dict) and any(int(v or 0) > 0 for v in totals.values()):
                        is_empty = False
            elif isinstance(data, list) and len(data) == 0:
                is_empty = True

            tag = "EMPTY" if is_empty else "HAS"
            print(f"{tag} {path}")
            print(f"  summary={summary}")
            print(f"  sample={sample}")
            (empty if is_empty else ok).append(path)
        except Exception as e:
            print(f"ERR  {path} {e}")
            empty.append(path)

    print("\n=== SUMMARY ===")
    print(f"HAS_DATA={len(ok)} EMPTY_OR_ERR={len(empty)}")
    for p in empty:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
