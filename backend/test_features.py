import urllib.request
import json

endpoints = {
    "Crime Pattern Discovery": "/api/v1/patterns/",
    "Crime Trend Analysis": "/api/v1/trends/summary",
    "Crime Hotspot Detection": "/api/v1/hotspots/",
    "Geospatial Crime Maps": "/api/v1/maps/stats",
    "Criminal Network Visualization": "/api/v1/graph/stats",
    "Criminal Timeline Analysis": "/api/v1/criminal-timeline/",
    "Behavioral Profiling": "/api/v1/behavior/stats",
    "Repeat Offender Tracking": "/api/v1/repeat-offenders/stats",
    "MO Fingerprinting": "/api/v1/mo/stats",
    "Predictive Crime Analytics": "/api/v1/predictions/",
    "Early Warning Alerts": "/api/v1/early-warning/stats",
    "High-Risk Suspect Scoring": "/api/v1/suspect-risk/stats",
    "Intelligent Case Prioritization": "/api/v1/priorities/stats",
    "Proactive Intelligence": "/api/v1/proactive/stats",
    "Live FIR Intelligence Suggestions": "/api/v1/fir-intelligence/stats",
    "Cross-District Intelligence Matching": "/api/v1/cross-district/stats",
    "Dynamic Evidence Linking": "/api/v1/evidence-linking/stats",
    "Entity Resolution & Record Merging": "/api/v1/intelligence/summary"
}

results = {}

for name, path in endpoints.items():
    try:
        req = urllib.request.Request(f'http://localhost:8001{path}')
        resp = urllib.request.urlopen(req, timeout=5)
        status = resp.status
        print(f"{name}: {status} OK")
    except urllib.error.HTTPError as e:
        print(f"{name}: {e.code} {e.reason}")
    except Exception as e:
        print(f"{name}: Error {str(e)}")
