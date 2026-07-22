from pathlib import Path
import re, json

frames = Path(r"c:\Users\bhuwan.bhawarlal\Desktop\projects\CrimeMatrix\videos\crimematrix-promo\compositions\frames")

for path in sorted(frames.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    text2 = text.replace(".frame-root {", "#root {").replace(".frame-root{", "#root {")
    text2 = re.sub(
        r'class="frame-root"(\s+id="[^"]+")?',
        'id="root"',
        text2,
        count=1,
    )

    def fix_id(m):
        quote = m.group(1)
        val = m.group(2)
        if val[:1].isdigit():
            return f"id={quote}el-{val}{quote}"
        return m.group(0)

    text2 = re.sub(r'id=(["\'])([^"\']+)\1', fix_id, text2)
    text2 = re.sub(r'(["\'])#(\d)', r"\1#el-\2", text2)
    if text2 != text:
        path.write_text(text2, encoding="utf-8")
        print("fixed", path.name)
    else:
        print("unchanged", path.name)

meta_path = Path(r"c:\Users\bhuwan.bhawarlal\Desktop\projects\CrimeMatrix\videos\crimematrix-promo\audio_meta.json")
meta = json.loads(meta_path.read_text(encoding="utf-8"))
durs = [16.661, 4.715, 7.488, 5.461, 10.304, 12.544, 21.717, 13.312, 15.211, 20.523, 17.771, 4.757]
meta["voices"] = [
    {"frame": i + 1, "path": f"assets/voice/frame-{i+1:02d}.wav", "duration_s": durs[i], "words": []}
    for i in range(12)
]
meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
print("voices restored", len(meta["voices"]), "sfx", len(meta.get("sfx", [])))
