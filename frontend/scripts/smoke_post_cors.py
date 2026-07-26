import urllib.request

body = b'{"query":"theft"}'
req = urllib.request.Request(
    "https://crimematrix-backend-50044181811.development.catalystappsail.in/api/v1/search/",
    data=body,
    method="POST",
    headers={
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://crimematrix-frontend-nvjwdioh.onslate.in",
    },
)
with urllib.request.urlopen(req, timeout=45) as r:
    print("POST", r.status)
    for k, v in r.headers.items():
        if "access" in k.lower():
            print(f"{k}: {v}")
    print(r.read()[:200])
