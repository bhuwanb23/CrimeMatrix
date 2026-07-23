"""Align getElementById / buildDepthStack ids with DOM el- prefixed ids."""
from __future__ import annotations

import re
from pathlib import Path

FRAMES = Path(__file__).parent / "compositions" / "frames"

# getElementById("X") -> getElementById("el-X") when DOM has el-X and not X
GET_RE = re.compile(r"""getElementById\(\s*(['"])([^'"]+)\1\s*\)""")

# buildDepthStack("11-depth-N") callers
DEPTH_CALLS = [
    ("11-depth-1", "el-11-depth-1"),
    ("11-depth-2", "el-11-depth-2"),
    ("11-depth-3", "el-11-depth-3"),
]

# frame 09 path loop ids
PATH_IDS_09 = [
    "09-pi-axis-x",
    "09-pi-axis-y",
    "09-pi-grid-1",
    "09-pi-grid-2",
    "09-pi-grid-3",
]


def fix_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    orig = text
    changes: list[str] = []

    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', text))

    def repl_get(m: re.Match[str]) -> str:
        q, name = m.group(1), m.group(2)
        if name in ids:
            return m.group(0)
        el = f"el-{name}"
        if el in ids:
            changes.append(f"getElementById: {name} -> {el}")
            return f"getElementById({q}{el}{q})"
        return m.group(0)

    text = GET_RE.sub(repl_get, text)

    # Explicit string fixes for depth stack calls (passed as args, not getElementById)
    for old, new in DEPTH_CALLS:
        if f'"{old}"' in text and new in ids:
            text = text.replace(f'"{old}"', f'"{new}"')
            changes.append(f"depth stack arg: {old} -> {new}")
        if f"'{old}'" in text and new in ids:
            text = text.replace(f"'{old}'", f"'{new}'")
            changes.append(f"depth stack arg: {old} -> {new}")

    # Frame 09: array of path id strings without el-
    for pid in PATH_IDS_09:
        el = f"el-{pid}"
        if f'"{pid}"' in text and el in ids:
            text = text.replace(f'"{pid}"', f'"{el}"')
            changes.append(f"path id string: {pid} -> {el}")

    # Frame 03: .frame-root -> #root
    if 'querySelector(".frame-root")' in text:
        text = text.replace('querySelector(".frame-root")', 'querySelector("#root")')
        changes.append(".frame-root -> #root")

    # Corrupted hex colors
    if "#el-0f172a" in text:
        text = text.replace("#el-0f172a", "#0f172a")
        changes.append("#el-0f172a -> #0f172a")

    if text != orig:
        path.write_text(text, encoding="utf-8")
    return changes


def main() -> None:
    for path in sorted(FRAMES.glob("*.html")):
        changes = fix_file(path)
        if changes:
            print(path.name)
            for c in changes:
                print(f"  {c}")
        else:
            print(f"{path.name}: ok")


if __name__ == "__main__":
    main()
