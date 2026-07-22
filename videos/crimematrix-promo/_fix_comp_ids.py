from pathlib import Path
import re

frames = Path(r"c:\Users\bhuwan.bhawarlal\Desktop\projects\CrimeMatrix\videos\crimematrix-promo\compositions\frames")

for path in sorted(frames.glob("*.html")):
    stem = path.stem  # e.g. 01-fragmented-records
    text = path.read_text(encoding="utf-8")
    # Restore correct composition id (must match filename / storyboard src)
    text = re.sub(
        r'data-composition-id="el-[^"]+"',
        f'data-composition-id="{stem}"',
        text,
    )
    # Timeline key must match composition id
    text = re.sub(
        r'window\.__timelines\["el-[^"]+"\]',
        f'window.__timelines["{stem}"]',
        text,
    )
    text = re.sub(
        r"window\.__timelines\['el-[^']+'\]",
        f"window.__timelines['{stem}']",
        text,
    )
    # Also fix any bare registration that lost matching
    # Ensure at least one correct registration exists
    if f'window.__timelines["{stem}"]' not in text and f"window.__timelines['{stem}']" not in text:
        # try replace any __timelines["..."] near end
        text = re.sub(
            r'window\.__timelines\["[^"]+"\]\s*=\s*tl',
            f'window.__timelines["{stem}"] = tl',
            text,
            count=1,
        )
    path.write_text(text, encoding="utf-8")
    print("restored", stem)
