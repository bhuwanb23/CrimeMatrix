# CrimeMatrix — AI Investigation Copilot for Karnataka State Police

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)

An AI-powered crime intelligence platform that transforms how law enforcement officers investigate crimes, identify suspects, and uncover criminal networks across Karnataka's 31 districts.

---

## The Problem

Karnataka State Police processes over **200,000 FIRs annually** across 31 districts. Officers face daily challenges that no spreadsheet or basic database can solve:

**Fragmented Identities** — The same suspect appears as "Raj" in Bengaluru, "Rajesh" in Mysuru, and "Rajendra" in Mangaluru. Without identity resolution, criminals slip through jurisdictional cracks.

**Language Barrier** — Field officers think and speak in Kannada. They mix Kannada with English (Kanglish) in daily conversation: *"Bellary suspect ge phone match check madi"*. Existing systems demand English-only input.

**Reactive Intelligence** — By the time patterns are spotted — a serial burglar targeting jewelry stores across three districts — the damage is done. Intelligence arrives after the crimes, not before.

**Black-Box AI** — When an AI system recommends "investigate Suspect A," officers need to know *why*. A recommendation without reasoning is just noise.

**Disconnected Investigations** — Each district maintains its own records. A robbery in Bengaluru and a similar MO in Mysuru never connect unless someone manually calls across districts.

---

## How CrimeMatrix Works

CrimeMatrix is an **AI Investigation Copilot** — not a chatbot, but a structured reasoning system that assists officers through the entire investigation lifecycle.

```
┌─────────────────────────────────────────────────────────────────┐
│                        OFFICER QUERY                             │
│   "Show me similar robbery cases across Karnataka last month"   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LANGUAGE PIPELINE                            │
│   Detect → Normalize (Kanglish/English/Kannada) → Translate     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AI AGENT LOOP                              │
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │ PLANNER  │───▶│ EXECUTOR │───▶│ CONTEXT  │───▶│ RESPONDER│ │
│   │          │    │          │    │ BUILDER  │    │          │  │
│   │ Decompose│    │ Run 28+  │    │ Compile  │    │ Generate │  │
│   │ into     │    │ tools:   │    │ results  │    │ final    │  │
│   │ steps    │    │ search,  │    │ into     │    │ answer   │  │
│   │          │    │ graph,   │    │ context  │    │ with     │  │
│   │          │    │ predict, │    │          │    │ reasoning│  │
│   │          │    │ reason   │    │          │    │ chain    │  │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYERS                           │
│                                                                  │
│   Knowledge Graph ─── Entity relationships across 68 models     │
│   RAG Pipeline ────── Semantic search over case documents       │
│   Prediction Engine ── Crime forecasting, hotspot detection     │
│   Identity Resolver ── Phonetic + nickname + transliteration    │
│   Reasoning Engine ─── Explainable chains with confidence       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESPONSE                                    │
│                                                                  │
│   "Found 12 similar cases across 4 districts. Key connections:  │
│    • MO fingerprint matches 3 unsolved burglaries               │
│    • Suspect vehicle (KA-01-M-4521) linked to FIR 102/2024      │
│    • Confidence: 87% — reasoning chain attached"                │
└─────────────────────────────────────────────────────────────────┘
```

### Investigation Workflow

When an officer registers a new FIR, CrimeMatrix proactively surfaces intelligence:

```
Officer creates FIR ──▶ System analyzes FIR details
                              │
                              ▼
                    ┌─────────────────────┐
                    │  REAL-TIME INTEL     │
                    │                      │
                    │  Similar unresolved  │
                    │  cases nearby        │
                    │                      │
                    │  Related suspects    │
                    │  in other districts  │
                    │                      │
                    │  Matching MO from    │
                    │  criminal profiles   │
                    │                      │
                    │  Vehicle/phone       │
                    │  matches across      │
                    │  investigations      │
                    └─────────────────────┘
                              │
                              ▼
                    Officer gets immediate
                    intelligence context
                    before investigation
                    even begins
```

---

## Architecture

CrimeMatrix runs as three independent services, each with a clear responsibility:

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│                    React 19 + Tailwind 4                        │
│                                                                  │
│   Dashboard │ Copilot │ Cases │ Intelligence │ Graph │ Maps     │
│   Patterns │ Timeline │ Predictions │ Alerts │ Reports          │
└────────────┬────────────────────────────────────┬───────────────┘
             │                                    │
             │  REST + SSE                        │  REST
             ▼                                    ▼
┌────────────────────────┐          ┌────────────────────────────┐
│      BACKEND API       │          │      AI SERVICES           │
│   FastAPI + SQLAlchemy  │◀────────▶│   FastAPI + Agent Loop     │
│      Port 8000         │  HTTP    │      Port 8002             │
│                        │          │                            │
│   50+ API endpoints    │          │   70+ AI endpoints         │
│   68 database models   │          │   28 specialized tools     │
│   38 service classes   │          │   4 built-in workflows     │
│   25 migrations        │          │   3 LLM providers          │
└────────┬───────────────┘          └──────────┬─────────────────┘
         │                                     │
         ▼                                     ▼
┌────────────────────┐          ┌──────────────────────────────┐
│   SQLite Database  │          │      External Services       │
│   68 tables        │          │                              │
│   Async (aiosqlite)│          │   Ollama (default, local)    │
│   Alembic migrations│         │   OpenAI (optional)          │
└────────────────────┘          │   Gemini (optional)          │
                                │                              │
                                │   FAISS (vector search)      │
                                │   NetworkX (knowledge graph) │
                                └──────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Three services, not monolith** | AI concerns separated from CRUD; independent scaling and deployment |
| **Plan → Execute → Respond** | Deterministic tool execution — no hallucinated tool calls, transparent reasoning |
| **Ollama as default** | Offline-first; no API key required for demo; local inference |
| **SQLite over PostgreSQL** | Zero-config setup; portable; async via aiosqlite |
| **In-memory FAISS** | No external vector DB required; sufficient for investigation-scale data |
| **NetworkX over Neo4j** | Python-native; no external graph DB; investigation-scale graphs |

See [docs/DESIGN-DECISIONS.md](docs/DESIGN-DECISIONS.md) for detailed rationale.

---

## Key Capabilities

| Problem | How CrimeMatrix Solves It |
|---------|--------------------------|
| **Fragmented identities** | Indian Identity Resolution Engine — phonetic matching (Soundex), 28+ nickname mappings, Kannada/Devanagari/Latin transliteration, fuzzy name comparison |
| **Language barrier** | Kanglish normalizer + multi-language pipeline (English, Kannada, Hindi) — officers type naturally, system understands |
| **Reactive investigation** | Whisper Alerts — proactive cross-district intelligence matching as new FIRs arrive |
| **Black-box AI** | Explainable reasoning chains — every recommendation shows its evidence, confidence score, and source attribution |
| **Disconnected cases** | Knowledge Graph — entity relationship mapping across persons, crimes, vehicles, officers, and stations |
| **Manual pattern detection** | AI-powered crime pattern discovery, hotspot prediction, and modus operandi fingerprinting |
| **No case prioritization** | Intelligent Case Prioritization — scores based on severity, repeat offenders, network connections, and prediction confidence |
| **Court report generation** | Court-Ready Investigation Reports — evidence references, reasoning chains, audit trails, timeline export |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.ai/) (for local AI inference)

### Option A: Docker Compose (Recommended)

```bash
git clone https://github.com/your-org/CrimeMatrix.git
cd CrimeMatrix
docker compose up
```

Access the app at `http://localhost:5173`.

### Option B: Manual Setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed_crimes.py
uvicorn main:app --port 8000

# AI Services (new terminal)
cd ai-services
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8002

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Option C: Makefile

```bash
make setup    # Install all dependencies
make seed     # Seed database with demo data
make dev      # Start all services
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed setup instructions.

---

## Tech Stack

| Service | Technology | Purpose |
|---------|-----------|---------|
| **Backend API** | FastAPI, SQLAlchemy 2.0, Alembic, SQLite | CRUD operations, data models, search, analytics |
| **AI Services** | FastAPI, Agent Loop, 3 LLM providers | AI reasoning, RAG, knowledge graph, predictions |
| **Frontend** | React 19, Tailwind CSS 4, Vite 8, Recharts | Investigation dashboard, copilot interface |
| **AI Providers** | Ollama (default), OpenAI, Gemini | Local and cloud LLM inference |
| **Vector Search** | FAISS | Semantic document retrieval |
| **Graph Analysis** | NetworkX | Criminal network analysis, relationship discovery |
| **NLP** | sentence-transformers, scikit-learn | Embeddings, similarity, clustering |

---

## Project Structure

```
CrimeMatrix/
├── backend/                    # Backend API service
│   ├── app/
│   │   ├── api/v1/            # 50+ REST endpoints
│   │   ├── models/            # 68 SQLAlchemy models
│   │   ├── services/          # 38 business logic classes
│   │   ├── repositories/      # Data access layer
│   │   └── ...
│   ├── alembic/               # 25 database migrations
│   ├── tests/                 # Backend test suite
│   └── seed_crimes.py         # Demo data seeder
│
├── ai-services/               # AI Intelligence service
│   ├── agent/                 # Core agent loop (Planner → Executor → Responder)
│   ├── tools/                 # 28 specialized tools
│   │   ├── crime/             # Crime search, detail, list, stats
│   │   ├── graph/             # Graph traversal, shortest path, neighbors
│   │   ├── identity/          # Indian name matching, transliteration
│   │   ├── knowledge/         # Knowledge graph queries
│   │   ├── reasoning/         # Explainable reasoning chains
│   │   ├── prediction/        # Crime forecasting, hotspot, risk scoring
│   │   ├── search/            # Intelligent search pipeline
│   │   └── ...
│   ├── knowledge/             # Knowledge graph builder
│   ├── memory/                # Multi-layer memory system
│   ├── rag/                   # RAG pipeline
│   ├── reasoning/             # Reasoning engine
│   ├── prediction/            # Prediction engine
│   ├── identity/              # Identity resolution
│   ├── language/              # Language pipeline (Kanglish, translation)
│   ├── workflows/             # Investigation workflows
│   └── tests/                 # 23 test files
│
├── frontend/                  # React SPA
│   ├── src/
│   │   ├── components/        # 46+ UI components
│   │   ├── services/          # 24 API service modules
│   │   └── ...
│   └── DESIGN.md              # Design system
│
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # System design with diagrams
│   ├── DESIGN-DECISIONS.md    # Architecture rationale
│   ├── API.md                 # API overview
│   └── DEPLOYMENT.md          # Setup guide
│
├── reference/                 # Product specifications
│   ├── features.md            # Feature matrix
│   └── comparsion.md          # Innovation strategy
│
├── docker-compose.yml         # One-command setup
├── Makefile                   # Build automation
├── CONTRIBUTING.md            # Contribution guide
├── SECURITY.md                # Security policy
└── LICENSE                    # MIT License
```

---

## API Overview

CrimeMatrix exposes two APIs:

- **Backend API** (`http://localhost:8000/api/v1/`) — 50+ endpoints for crime data, investigations, search, intelligence, analytics
- **AI Services API** (`http://localhost:8002/api/ai/`) — 70+ endpoints for AI chat, tools, RAG, identity resolution, knowledge graph, reasoning, predictions

See [docs/API.md](docs/API.md) for the complete API reference.

Interactive API docs are available at:
- `http://localhost:8000/docs` (Backend)
- `http://localhost:8002/docs` (AI Services)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Security

For security concerns, see [SECURITY.md](SECURITY.md).

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
