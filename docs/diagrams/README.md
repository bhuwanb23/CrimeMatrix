# CrimeMatrix diagrams

16:9 (1920×1080) navy + gold on white — for PowerPoint, Notion, and the GitHub README.

| Asset | Purpose |
|-------|---------|
| [`01-user-flow-sequence`](01-user-flow-sequence.png) | Investigation sequence — officer → Slate → Backend → AI → LLM → store |
| [`02-hybrid-architecture`](02-hybrid-architecture.png) | Hybrid architecture — L1 Experience → L4 Intelligence |
| [`03-use-case-map`](03-use-case-map.png) | Actors and core use cases |
| [`04-ai-crime-intelligence-ecosystem`](04-ai-crime-intelligence-ecosystem.png) | Signals → AI core → outcomes |

README-only banners live in [`../assets/`](../assets/):

| Asset | Purpose |
|-------|---------|
| [`readme-hero.png`](../assets/readme-hero.png) | Dark hero banner |
| [`readme-impact.png`](../assets/readme-impact.png) | Impact metrics strip |
| [`promo-poster.jpg`](../assets/promo-poster.jpg) | Operational-pain visual |

Each diagram ships as **`.svg`** (edit / scale) and **`.png`** (paste into slides or Markdown).

## Regenerate PNGs

```bash
cd docs/scripts
npm install
node render-diagrams.mjs
```

Uses [`@resvg/resvg-js`](https://github.com/yisibl/resvg-js) so renders stay sharp at 1920px width.
