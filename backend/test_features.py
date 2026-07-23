import urllib.request
import json

endpoints = {
    "Crime Pattern Discovery": "/api/v1/patterns/",
    "Crime Trend Analysis": "/api/v1/trends/",
    "Crime Hotspot Detection": "/api/v1/hotspots/",
    "Geospatial Crime Maps": "/api/v1/maps/",
    "Criminal Network Visualization": "/api/v1/graph/",
    "Criminal Timeline Analysis": "/api/v1/criminal-timeline/",
    "Behavioral Profiling": "/api/v1/behavior/",
    "Repeat Offender Tracking": "/api/v1/repeat-offenders/",
    "MO Fingerprinting": "/api/v1/mo/",
    "Predictive Crime Analytics": "/api/v1/predictions/",
    "Early Warning Alerts": "/api/v1/early-warning/",
    "High-Risk Suspect Scoring": "/api/v1/suspect-risk/",
    "Intelligent Case Prioritization": "/api/v1/priorities/",
    "Proactive Intelligence": "/api/v1/proactive/",
    "Live FIR Intelligence Suggestions": "/api/v1/fir-intelligence/",
    "Cross-District Intelligence Matching": "/api/v1/cross-district/",
    "Dynamic Evidence Linking": "/api/v1/evidence-linking/",
    "Entity Resolution & Record Merging": "/api/v1/intelligence/"
}

results = {}

for name, path in endpoints.items():
    try:
        req = urllib.request.Request(f'http://localhost:8000{path}')
        resp = urllib.request.urlopen(req)
        status = resp.status
        msg = "OK"
    except urllib.error.HTTPError as e:
        status = e.code
        msg = e.reason
    except Exception as e:
        status = "Error"
        msg = str(e)
    
    print(f"{name}: {status} {msg}")
