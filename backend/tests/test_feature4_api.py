"""
Feature 4 — AI Analytics & Prediction: API Integration Tests
Full end-to-end API testing against running servers.
"""
import requests
import sys

BASE = "http://localhost:8001/api/v1"
AI_BASE = "http://localhost:8002/api/ai"
results = []


def test(name, method, url, data=None):
    try:
        if method == "GET":
            r = requests.get(url, timeout=15)
        elif method == "POST":
            r = requests.post(url, json=data or {}, timeout=15)
        elif method == "PUT":
            r = requests.put(url, json=data or {}, timeout=15)
        else:
            r = requests.delete(url, timeout=15)
        status = "PASS" if r.status_code == 200 else f"FAIL ({r.status_code})"
        results.append((name, status))
        print(f"  [{status.split(' ')[0]}] {name}")
    except Exception as e:
        results.append((name, f"ERROR: {str(e)[:50]}"))
        print(f"  [ERROR] {name}: {str(e)[:50]}")


print("=" * 70)
print("FEATURE 4 — AI ANALYTICS & PREDICTION: API INTEGRATION TESTS")
print("=" * 70)

# ============================================================
# Phase 1: AI Analytics Dashboard
# ============================================================
print("\n--- Phase 1: AI Analytics Dashboard ---")
test("P1: Dashboard Summary", "GET", f"{BASE}/analytics-dashboard/summary")
test("P1: Dashboard Alerts", "GET", f"{BASE}/analytics-dashboard/alerts")
test("P1: Dashboard Forecasts", "GET", f"{BASE}/analytics-dashboard/forecasts")
test("P1: Dashboard High-Risk", "GET", f"{BASE}/analytics-dashboard/high-risk")
test("P1: Dashboard Priority", "GET", f"{BASE}/analytics-dashboard/priority")
test("P1: Dashboard Stats", "GET", f"{BASE}/analytics-dashboard/stats")

# ============================================================
# Phase 2: Predictive Crime Analytics
# ============================================================
print("\n--- Phase 2: Predictive Crime Analytics ---")
test("P2: Prediction Stats", "GET", f"{BASE}/predictions/stats")
test("P2: List Predictions", "GET", f"{BASE}/predictions/")
test("P2: Generate Forecast", "POST", f"{BASE}/predictions/forecast", {"periods": 30})
test("P2: Prediction Models", "GET", f"{BASE}/predictions/models")

# ============================================================
# Phase 3: Early Warning Alerts
# ============================================================
print("\n--- Phase 3: Early Warning Alerts ---")
test("P3: Early Warning Stats", "GET", f"{BASE}/early-warning/stats")
test("P3: List Alerts", "GET", f"{BASE}/early-warning/alerts")
test("P3: Detect Alerts", "POST", f"{BASE}/early-warning/detect")
test("P3: Alert Rules", "GET", f"{BASE}/early-warning/rules")
test("P3: Alert Timeline", "GET", f"{BASE}/early-warning/timeline?days=30")

# ============================================================
# Phase 4: High-Risk Suspect Scoring
# ============================================================
print("\n--- Phase 4: High-Risk Suspect Scoring ---")
test("P4: Risk Stats", "GET", f"{BASE}/suspect-risk/stats")
test("P4: Risk Rankings", "GET", f"{BASE}/suspect-risk/rankings?limit=5")
test("P4: Risk Scores", "GET", f"{BASE}/suspect-risk/scores")

# ============================================================
# Phase 5: Crime Forecasting
# ============================================================
print("\n--- Phase 5: Crime Forecasting ---")
test("P5: Forecast Stats", "GET", f"{BASE}/predictions/forecast/stats")
test("P5: Seasonal Patterns", "GET", f"{BASE}/predictions/forecast/seasonal?days=365")
test("P5: Forecast History", "GET", f"{BASE}/predictions/forecast/history")

# ============================================================
# Phase 6: Intelligent Case Prioritization
# ============================================================
print("\n--- Phase 6: Case Prioritization ---")
test("P6: Priority Stats", "GET", f"{BASE}/priorities/stats")
test("P6: Priority Rankings", "GET", f"{BASE}/priorities/rankings?limit=5")
test("P6: Priority Workload", "GET", f"{BASE}/priorities/workload")

# ============================================================
# Phase 7: Explainable Predictions
# ============================================================
print("\n--- Phase 7: Explainable Predictions ---")
test("P7: Explain Prediction", "POST", f"{BASE}/predictions/explain/1")
test("P7: Get Explanation", "GET", f"{BASE}/predictions/explain/1")
test("P7: Get Sources", "GET", f"{BASE}/predictions/sources/1")
test("P7: Confidence Breakdown", "GET", f"{BASE}/predictions/confidence/1")

# ============================================================
# Phase 8: Continuous Model Evaluation
# ============================================================
print("\n--- Phase 8: Model Evaluation ---")
test("P8: Evaluation Stats", "GET", f"{BASE}/evaluation/stats")
test("P8: Run Evaluation", "POST", f"{BASE}/evaluation/run")
test("P8: Accuracy Trend", "GET", f"{BASE}/evaluation/accuracy-trend")
test("P8: Drift Analysis", "GET", f"{BASE}/evaluation/drift")
test("P8: Evaluation Results", "GET", f"{BASE}/evaluation/results")

# ============================================================
# Phase 9: AI Copilot Integration
# ============================================================
print("\n--- Phase 9: AI Copilot Integration ---")
test("P9: AI Tools Count", "GET", f"{AI_BASE}/tools")
test("P9: AI Health", "GET", f"{AI_BASE}/health")

# ============================================================
# Regression Tests
# ============================================================
print("\n--- Regression: Core APIs ---")
test("REG: Health", "GET", f"{BASE}/health")
test("REG: Intelligence", "GET", f"{BASE}/intelligence/summary")
test("REG: Crimes", "GET", f"{BASE}/crimes/?page=1&page_size=5")
test("REG: Patterns", "GET", f"{BASE}/patterns/stats")
test("REG: Trends", "GET", f"{BASE}/trends/summary")
test("REG: Hotspots", "GET", f"{BASE}/hotspots/stats")
test("REG: Maps", "GET", f"{BASE}/maps/stats")
test("REG: Graph", "GET", f"{BASE}/graph/stats")
test("REG: Timeline", "GET", f"{BASE}/criminal-timeline/stats")
test("REG: Behavior", "GET", f"{BASE}/behavior/stats")
test("REG: MO", "GET", f"{BASE}/mo/stats")
test("REG: Similar Cases", "GET", f"{BASE}/similar-cases/stats")
test("REG: Recommendations", "GET", f"{BASE}/recommendations/dashboard")
test("REG: Investigations", "GET", f"{BASE}/investigations/")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 70)
print("FEATURE 4 VALIDATION SUMMARY")
print("=" * 70)

passed = sum(1 for _, s in results if "PASS" in s)
failed = sum(1 for _, s in results if "FAIL" in s or "ERROR" in s)
total = len(results)

print(f"Total Tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Pass Rate: {round(passed/total*100, 1)}%")

if failed == 0:
    print("\n*** ALL FEATURE 4 TESTS PASSED ***")
else:
    print(f"\n{failed} FAILED TESTS:")
    for name, status in results:
        if "FAIL" in status or "ERROR" in status:
            print(f"  - {name}: {status}")

print("=" * 70)
