"""Smoke-check Catalyst Slate frontend deploy."""
from __future__ import annotations

import re
import urllib.request

BASE = "https://crimematrix-frontend-nvjwdioh.onslate.in"
BACKEND = (
    "https://crimematrix-backend-50044181811.development.catalystappsail.in"
    "/api/v1/districts/?page=1&page_size=1"
)


def fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "crimematrix-smoke"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def main() -> None:
    for path in ("/", "/copilot", "/investigations"):
        status, body = fetch(BASE + path)
        has_root = 'id="root"' in body or "id='root'" in body
        title = ""
        if "<title>" in body:
            title = body[body.find("<title>") : body.find("</title>") + 8]
        print(f"SPA {status} {path} root={has_root} {title}")

    status, body = fetch(BACKEND)
    print(f"API {status} districts={body[:120]!r}")

    _, html = fetch(BASE + "/")
    m = re.search(r"/assets/[^\"']+\.js", html)
    if not m:
        raise SystemExit("No JS asset found in index.html")
    asset = m.group(0)
    print(f"asset {asset}")
    _, js = fetch(BASE + asset)
    print(f"baked_backend={'crimematrix-backend-50044181811' in js}")


if __name__ == "__main__":
    main()
