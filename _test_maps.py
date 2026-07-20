import requests
import sys

BASE = "http://localhost:8001/api/v1"
results = []

def test(name, method, url, data=None):
    try:
        if method == "GET":
            r = requests.get(url, timeout=10)
        elif method == "POST":
            r = requests.post(url, json=data, timeout=10)
        else:
            r = requests.delete(url, timeout=10)
        status = "PASS" if r.status_code == 200 else f"FAIL ({r.status_code})"
        results.append((name, status))
        print(f"  {status}: {name}")
        if r.status_code == 200:
            d = r.json().get("data", {})
            if isinstance(d, dict) and "features" in d:
                print(f"        Features: {len(d['features'])}")
            elif isinstance(d, dict) and "points" in d:
                print(f"        Points: {len(d['points'])}")
            elif isinstance(d, dict) and "routes" in d:
                print(f"        Routes: {len(d['routes'])}")
    except Exception as e:
        results.append((name, f"ERROR: {str(e)[:50]}"))
        print(f"  ERROR: {name} - {str(e)[:50]}")

print("=" * 60)
print("FEATURE 4 PHASE 5 — GEOSPATIAL MAPS VALIDATION")
print("=" * 60)

print("\n--- Map APIs ---")
test("Map Stats", "GET", f"{BASE}/maps/stats")
test("Crime Markers", "GET", f"{BASE}/maps/crime-markers?days=30")
test("District GeoJSON", "GET", f"{BASE}/maps/districts")
test("Heatmap Data", "GET", f"{BASE}/maps/heatmap?days=30")
test("Hotspot Markers", "GET", f"{BASE}/maps/hotspots")
test("Station Markers", "GET", f"{BASE}/maps/stations")
test("Route Data", "GET", f"{BASE}/maps/routes")

print("\n--- Other Feature APIs (Regression) ---")
test("Intelligence Summary", "GET", f"{BASE}/intelligence/summary")
test("Trend Summary", "GET", f"{BASE}/trends/summary")
test("Hotspot Stats", "GET", f"{BASE}/hotspots/stats")
test("Pattern Stats", "GET", f"{BASE}/patterns/stats")
test("Similar Cases Stats", "GET", f"{BASE}/similar-cases/stats")
test("Recommendations", "GET", f"{BASE}/recommendations/dashboard")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
failed = sum(1 for _, s in results if "FAIL" in s or "ERROR" in s)
print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
if failed == 0:
    print("ALL TESTS PASSED!")
else:
    print("SOME TESTS FAILED:")
    for name, status in results:
        if "FAIL" in status or "ERROR" in status:
            print(f"  - {name}: {status}")
