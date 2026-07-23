import urllib.request
try:
    req = urllib.request.Request('http://localhost:8000/api/v1/investigations/')
    resp = urllib.request.urlopen(req)
    print("SUCCESS:")
    print(resp.read().decode())
except Exception as e:
    print("ERROR:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
