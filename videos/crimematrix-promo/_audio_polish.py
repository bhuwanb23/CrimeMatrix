"""Build captions.html, impact-soft SFX, BGM bed, and patch index.html."""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
FFBIN = ROOT / "tools" / "ffmpeg-8.1.2-essentials_build" / "bin"
FFMPEG = str(FFBIN / "ffmpeg.exe")

VOICES = json.loads((ROOT / "audio_meta.json").read_text(encoding="utf-8"))["voices"]

LINES = [
    "Every day, thousands of crime records are generated across Karnataka. Yet investigators still spend countless hours searching through fragmented databases, connecting evidence manually, and trying to uncover hidden relationships between cases.",
    "What if an AI could become every investigator's intelligent partner?",
    "Introducing CrimeMatrix — an AI-powered Crime Intelligence Platform built for the Karnataka State Police.",
    "CrimeMatrix transforms investigations through a conversational AI assistant.",
    "Instead of navigating multiple systems, officers simply ask questions in natural language—or even by voice—in English, Kannada, or Kanglish.",
    "The AI understands context, remembers ongoing investigations, and provides instant, explainable answers, making complex investigations faster and more intuitive.",
    "Beyond search, CrimeMatrix uncovers intelligence hidden within millions of records. Investigators can perform semantic crime searches, discover similar cases across districts, visualize criminal networks, explore relationship graphs, analyze crime trends, detect hotspots, and trace complete criminal timelines.",
    "Our Indian Identity Resolution Engine intelligently links duplicate identities despite spelling variations and multilingual records, ensuring investigators never miss critical connections.",
    "CrimeMatrix doesn't just analyze the past—it helps prevent future crime. AI predicts emerging crime patterns, identifies high-risk suspects, prioritizes investigations, and forecasts crime trends.",
    "Most importantly, our proactive intelligence engine continuously monitors new FIRs and evidence, automatically generating Whisper Alerts, detecting cross-district links, recommending investigative leads, and connecting evidence in real time—often before investigators even know to ask.",
    "CrimeMatrix is more than a dashboard. It is an AI Investigation Copilot, a Crime Intelligence Platform, and a proactive decision-support system built to empower law enforcement with faster investigations, smarter insights, and safer communities.",
    "CrimeMatrix — Transforming Crime Data into Actionable Intelligence.",
]

# Cumulative VO starts
starts = []
t = 0.0
for v in VOICES:
    starts.append(t)
    t += float(v["duration_s"])
TOTAL = t


def split_chunks(text: str, max_words: int = 12) -> list[str]:
    words = text.replace("—", " — ").split()
    chunks: list[str] = []
    buf: list[str] = []
    for w in words:
        buf.append(w)
        soft = w.endswith((".", "?", ",", ";", "—"))
        if len(buf) >= max_words or (soft and len(buf) >= 6):
            chunks.append(" ".join(buf))
            buf = []
    if buf:
        chunks.append(" ".join(buf))
    return chunks or [text]


def make_groups() -> list[dict]:
    groups: list[dict] = []
    for i, line in enumerate(LINES):
        vo_start = starts[i]
        vo_dur = float(VOICES[i]["duration_s"])
        chunks = split_chunks(line)
        # allocate time proportional to word count
        weights = [max(1, len(c.split())) for c in chunks]
        wsum = sum(weights)
        cursor = vo_start + 0.15
        usable = max(0.5, vo_dur - 0.35)
        for chunk, w in zip(chunks, weights):
            chunk_dur = usable * (w / wsum)
            words_txt = chunk.split()
            n = len(words_txt)
            step = chunk_dur / max(n, 1)
            words = []
            for j, wt in enumerate(words_txt):
                ws = cursor + j * step
                words.append({"text": wt, "start": round(ws, 3), "end": round(ws + step, 3)})
            groups.append(
                {
                    "start": round(cursor, 3),
                    "end": round(cursor + chunk_dur, 3),
                    "words": words,
                }
            )
            cursor += chunk_dur
    return groups


CAPTION_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
<style data-brand-tokens>
  :root {
    --cap-ink: #0f172a;
    --cap-canvas: #ffffff;
    --cap-accent: #f59e0b;
    --cap-accent-2: #b45309;
    --font-display: "Plus Jakarta Sans", system-ui, sans-serif;
    --font-body: "Plus Jakarta Sans", system-ui, sans-serif;
    --cap-band-top: 900px;
    --cap-band-height: 180px;
  }
</style>
<style>
  #captions-root {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  .caption-layer {
    position: absolute;
    inset: 0;
    z-index: 20;
    pointer-events: none;
  }
  .caption-stage {
    position: absolute;
    left: 0;
    right: 0;
    top: var(--cap-band-top, 900px);
    height: var(--cap-band-height, 180px);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .caption-group {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
  }
  .caption-pill {
    max-width: 78%;
    padding: 16px 36px 18px;
    background: color-mix(in srgb, var(--cap-accent, #f59e0b) 6%, var(--cap-canvas, #ffffff));
    border: 1.5px solid color-mix(in srgb, var(--cap-accent, #f59e0b) 28%, transparent);
    border-radius: 14px;
  }
  .caption-line {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.1em 0.28em;
    font-family: var(--font-display, "Plus Jakarta Sans"), system-ui, sans-serif;
    font-weight: 600;
    font-size: clamp(28px, 2.6vw, 40px);
    line-height: 1.2;
    letter-spacing: -0.02em;
  }
  .caption-word {
    display: inline-block;
    padding: 0 0.14em;
    border-radius: 0.28em;
    color: color-mix(in srgb, var(--cap-ink, #0f172a) 55%, var(--cap-canvas, #ffffff));
  }
  .caption-word.is-active {
    color: #0f172a;
    background: var(--cap-accent, #f59e0b);
  }
  .caption-word.is-spoken {
    color: var(--cap-ink, #0f172a);
    background: transparent;
  }
</style>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<div
  id="captions-root"
  data-composition-id="captions"
  data-timeline-locked
  data-start="0"
  data-duration="__DURATION__"
  data-fps="30"
  data-width="1920"
  data-height="1080"
>
  <div class="caption-layer" aria-hidden="true">
    <div id="caption-stage" class="caption-stage"></div>
  </div>
</div>
<script>
  var GROUPS = __GROUPS__;
  var DURATION = __DURATION__;

  (function () {
    var stage = document.getElementById("caption-stage");
    GROUPS.forEach(function (group, g) {
      var groupEl = document.createElement("div");
      groupEl.className = "caption-group";
      groupEl.id = "caption-group-" + g;
      var pill = document.createElement("div");
      pill.className = "caption-pill";
      var line = document.createElement("div");
      line.className = "caption-line";
      (group.words || []).forEach(function (w, i) {
        var span = document.createElement("span");
        span.className = "caption-word";
        span.id = "caption-word-" + g + "-" + i;
        span.textContent = String(w.text);
        line.appendChild(span);
      });
      pill.appendChild(line);
      groupEl.appendChild(pill);
      stage.appendChild(groupEl);
    });

    window.__timelines = window.__timelines || {};
    var tl = gsap.timeline({ paused: true });

    GROUPS.forEach(function (group, g) {
      var groupEl = document.getElementById("caption-group-" + g);
      var words = group.words || [];
      var next = GROUPS[g + 1];
      var isLast = g === GROUPS.length - 1;
      var start = Math.max(0, Number(group.start));
      var end = isLast ? DURATION : Math.min(Number(next.start), Number(group.end) + 0.3);
      if (end <= start) end = start + 0.01;

      tl.set(groupEl, { opacity: 1 }, start);
      tl.set(groupEl, { opacity: 0 }, end);

      words.forEach(function (w, i) {
        var el = document.getElementById("caption-word-" + g + "-" + i);
        var at = Math.max(start, Number(w.start));
        tl.set(el, { className: "caption-word" }, start);
        tl.set(el, { className: "caption-word is-active" }, at);
        tl.fromTo(el, { scale: 0.985 }, { scale: 1, duration: 0.18, ease: "power1.out" }, at);
        if (i + 1 < words.length) {
          var nextAt = Math.max(start, Number(words[i + 1].start));
          tl.set(el, { className: "caption-word is-spoken" }, nextAt);
        }
      });
      if (words.length) {
        var lastEl = document.getElementById("caption-word-" + g + "-" + (words.length - 1));
        var lastSpoken = Math.min(end, Number(words[words.length - 1].end) + 0.1);
        tl.set(lastEl, { className: "caption-word is-spoken" }, lastSpoken);
      }
    });

    tl.to({}, { duration: DURATION }, 0);
    window.__timelines["captions"] = tl;
  })();
</script>
    </template>
  </body>
</html>
"""


def run_ffmpeg(args: list[str]) -> None:
    cmd = [FFMPEG, "-y", *args]
    print(" ", " ".join(cmd[-8:]))
    subprocess.run(cmd, check=True, capture_output=True)


def make_impact() -> None:
    out = ROOT / "assets" / "sfx" / "impact-soft.mp3"
    # Soft low thud + short noise burst, ~0.45s
    run_ffmpeg(
        [
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=90:duration=0.18",
            "-f",
            "lavfi",
            "-i",
            "anoisesrc=color=pink:duration=0.12:amplitude=0.15",
            "-filter_complex",
            "[0:a]afade=t=out:st=0.05:d=0.13,volume=0.55[a0];"
            "[1:a]afade=t=out:st=0.02:d=0.1,adelay=40|40,volume=0.35[a1];"
            "[a0][a1]amix=inputs=2:duration=longest,alimiter=limit=0.6[out]",
            "-map",
            "[out]",
            "-t",
            "0.45",
            str(out),
        ]
    )
    print("wrote", out)


def make_bgm() -> None:
    out = ROOT / "assets" / "bgm" / "underscore.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = math.ceil(TOTAL) + 1
    # Low investigative pad: layered sines + filtered noise, ducked soft
    run_ffmpeg(
        [
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=110:duration={dur}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=164.81:duration={dur}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=220:duration={dur}",
            "-f",
            "lavfi",
            "-i",
            f"anoisesrc=color=brown:duration={dur}:amplitude=0.04",
            "-filter_complex",
            "[0:a]volume=0.08[a0];"
            "[1:a]volume=0.05[a1];"
            "[2:a]volume=0.035[a2];"
            "[3:a]lowpass=f=400,volume=0.12[a3];"
            "[a0][a1][a2][a3]amix=inputs=4:duration=longest,"
            "afade=t=in:st=0:d=2,afade=t=out:st={fade}:d=3,alimiter=limit=0.25[out]".format(
                fade=max(1, dur - 3)
            ),
            "-map",
            "[out]",
            "-t",
            str(dur),
            str(out),
        ]
    )
    print("wrote", out)


def write_captions() -> None:
    groups = make_groups()
    html = (
        CAPTION_HTML.replace("__GROUPS__", json.dumps(groups, ensure_ascii=False))
        .replace("__DURATION__", str(round(TOTAL, 3)))
    )
    out = ROOT / "compositions" / "captions.html"
    out.write_text(html, encoding="utf-8")
    print("wrote", out, "groups=", len(groups))


def patch_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")

    impact_starts = [
        ("02", 16.661 + 0.9),
        ("03", 21.376 + 1.0),
        ("06", 44.629 + 2.5),
        ("08", 78.89 + 4.0),
        ("10", 107.413 + 3.5),
        ("12", 145.707 + 2.4),
    ]

    if "impact-soft.mp3" not in text:
        sfx_block = "\n".join(
            f"""      <audio
        id="el-sfx-impact-{i}"
        src="assets/sfx/impact-soft.mp3"
        data-start="{start}"
        data-duration="0.45"
        data-track-index="{30 + i}"
        data-volume="0.4"
      ></audio>"""
            for i, (_, start) in enumerate(impact_starts)
        )
        text = text.replace("      <!-- SFX -->", "      <!-- SFX -->\n" + sfx_block)

    if "underscore.mp3" not in text:
        bgm = f"""      <audio
        id="el-bgm-underscore"
        src="assets/bgm/underscore.mp3"
        data-start="0"
        data-duration="{round(TOTAL, 3)}"
        data-track-index="15"
        data-volume="0.12"
      ></audio>
"""
        text = text.replace("      <!-- SFX -->", bgm + "\n      <!-- SFX -->")

    if 'data-composition-id="captions"' not in text and "compositions/captions.html" not in text:
        cap = f"""      <div
        id="el-captions"
        class="scene"
        data-composition-id="captions"
        data-composition-src="compositions/captions.html"
        data-start="0"
        data-duration="{round(TOTAL, 3)}"
        data-track-index="50"
      ></div>
"""
        text = text.replace("      <!-- SFX -->", cap + "\n      <!-- SFX -->")

    # Hide inactive scenes at t=0 (except first)
    if 'gsap.set("#el-02-intelligent-partner"' not in text:
        hide = """
      (function () {
        var hide = [
          "#el-02-intelligent-partner",
          "#el-03-introducing-crimematrix",
          "#el-04-conversational-copilot",
          "#el-05-multilingual-voice",
          "#el-06-explainable-answers",
          "#el-07-intelligence-mosaic",
          "#el-08-identity-resolution",
          "#el-09-predictive-intelligence",
          "#el-10-whisper-alerts",
          "#el-11-three-roles",
          "#el-12-tagline-cta"
        ];
        gsap.set(hide, { opacity: 0 });
        gsap.set("#el-01-fragmented-records", { opacity: 1 });
      })();
"""
        text = text.replace(
            'window.__timelines["main"] = gsap.timeline({ paused: true });',
            'window.__timelines["main"] = gsap.timeline({ paused: true });' + hide,
        )

    path.write_text(text, encoding="utf-8")
    print("patched index.html")

    # Update audio_meta
    meta = json.loads((ROOT / "audio_meta.json").read_text(encoding="utf-8"))
    meta["bgm"] = {"path": "assets/bgm/underscore.mp3", "duration_s": TOTAL, "volume": 0.12}
    existing = {(s.get("frame"), s.get("file")) for s in meta.get("sfx", [])}
    for i, (label, start) in enumerate(
        [(2, 16.661 + 0.9), (3, 21.376 + 1.0), (6, 44.629 + 2.5), (8, 78.89 + 4.0), (10, 107.413 + 3.5), (12, 145.707 + 2.4)]
    ):
        key = (label, "assets/sfx/impact-soft.mp3")
        if key not in existing:
            meta.setdefault("sfx", []).append(
                {
                    "frame": label,
                    "file": "assets/sfx/impact-soft.mp3",
                    "start_s": start,
                    "duration_s": 0.45,
                    "volume": 0.4,
                }
            )
    (ROOT / "audio_meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print("updated audio_meta.json")


if __name__ == "__main__":
    make_impact()
    make_bgm()
    write_captions()
    patch_index()
