# CrimeMatrix

**AI Investigation Copilot for Karnataka State Police**

[![Datathon 2026](https://img.shields.io/badge/Datathon-2026-FF6B35)](https://hack2skill.com/event/datathon2026)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)

CrimeMatrix helps investigation officers query crime records, resolve identities across districts, surface patterns early, and produce explainable, audit-ready investigation outputs — in English, Kannada, and Kanglish.

Built for [Datathon 2026](https://hack2skill.com/event/datathon2026) against the KSP brief on conversational AI, analytics, and predictive policing.

---

## The Challenge

Karnataka State Police handles **200,000+ FIRs** each year across **31 districts**. Day-to-day investigation work is slowed by:

| Challenge | What it looks like in practice |
|-----------|--------------------------------|
| Fragmented identities | The same person appears under different names and spellings across stations |
| Language friction | Officers often query in Kanglish, not clean English or Kannada alone |
| Reactive intelligence | Patterns emerge after crimes stack up, not before |
| Opaque recommendations | Officers need to know *why* a suggestion was made |
| Siloed districts | Records stay local; cross-district links are hard to find |

---

## What CrimeMatrix Does

CrimeMatrix is an investigation copilot — not a standalone chatbot. It supports the full loop from intake and search through analysis and reporting.

| Capability | What officers get |
|------------|-------------------|
| **Investigation Copilot** | Natural-language Q&A with multi-turn context and structured reasoning |
| **Identity Resolution** | Phonetic matching, nickname variants, and Kannada transliteration across districts |
| **Modus Operandi Matching** | Serial-crime links from behavioural fingerprints, not only shared entities |
| **Knowledge Graph** | Network views of people, cases, vehicles, phones, and locations |
| **Predictive Intelligence** | Forecasting, hotspot signals, and risk scoring for proactive response |
| **Whisper Alerts** | Cross-district matches surfaced without waiting for a manual search |
| **Explainable Outputs** | Reasoning chains and confidence with every recommendation |
| **Court-Ready Reports** | Investigation summaries with evidence references and audit trail |

---

## How It Works

1. The officer asks a question in English, Kannada, or Kanglish.
2. A language pipeline detects and normalizes the query.
3. An agent plans steps, runs specialized investigation tools, and builds context.
4. The response returns findings with a reasoning chain and confidence.

Example:

> *"Show me similar robbery cases across Karnataka"*  
> → Matched cases across districts, with rationale and confidence — not a bare search list.

---

## Quick Start

**Requirements:** Docker and Docker Compose.

```bash
git clone https://github.com/bhuwanb23/CrimeMatrix.git
cd CrimeMatrix
docker compose up
```

Open the application at [http://localhost:5173](http://localhost:5173).

<details>
<summary>Manual setup (without Docker)</summary>

Run each service in its own terminal.

```bash
# Backend — http://localhost:8000
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload

# In another terminal — seed DB + compute intelligence (API must be up)
cd backend
source venv/bin/activate   # Windows: venv\Scripts\activate
python -m seed --fresh
python -m seed --bootstrap-only

# AI Services — http://localhost:8002 (required for Copilot / semantic search)
cd ai-services
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8002 --reload

# Frontend — http://localhost:5173 (API default http://localhost:8000/api/v1)
cd frontend
npm install
npm run dev
```

For local LLM support, run [Ollama](https://ollama.com/) and pull a model (for example `llama3.2:1b`). Configure API keys in each service’s `.env` as needed. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment notes.

**Run order:** backend → `python -m seed --fresh` → `python -m seed --bootstrap-only` → ai-services (+ Ollama for Copilot) → frontend.

</details>

---

## Stack

| Layer | Technologies |
|-------|----------------|
| Interface | React 19, Vite, Tailwind CSS |
| API & data | FastAPI, SQLAlchemy, SQLite |
| Intelligence | Ollama, OpenAI, Gemini · FAISS · NetworkX · sentence-transformers |

Further design notes live in [docs/](docs/).

### Crime vs Case detail

Case detail pages load the primary record from **`GET /crimes/{id}`** (search also lists crimes). Optional CaseMaster sub-resources (`/cases/{id}/complainant`, evidence, etc.) only populate when a matching `cases.id` exists — missing rows show empty sections and do not block the page.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Security concerns: [SECURITY.md](SECURITY.md).

---

## License

Released under the [MIT License](LICENSE).

Built for [Datathon 2026](https://hack2skill.com/event/datathon2026).