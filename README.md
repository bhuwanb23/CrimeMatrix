<p align="center">
  <img src="frontend/public/favicon.svg" alt="CrimeMatrix" width="56" height="54" />
</p>

<h1 align="center">CrimeMatrix</h1>

<p align="center">
  <strong>AI Investigation Copilot for Karnataka State Police</strong><br/>
  Query records. Resolve identities. Surface patterns. Deliver explainable, court-ready insight —
  in English, Kannada, and Kanglish.
</p>

<p align="center">
  <a href="https://hack2skill.com/event/datathon2026"><img src="https://img.shields.io/badge/Datathon-2026-0F172A?style=for-the-badge" alt="Datathon 2026" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
</p>

<p align="center">
  <a href="#why-it-exists">Why</a> ·
  <a href="#what-officers-can-do">Capabilities</a> ·
  <a href="#how-an-investigation-flows">Flow</a> ·
  <a href="#system-at-a-glance">Architecture</a> ·
  <a href="#run-locally">Run</a> ·
  <a href="#documentation">Docs</a>
</p>

---

## Why it exists

Karnataka State Police registers **200,000+ FIRs** a year across **31 districts**. The hard part is rarely finding *a* record — it is connecting the right people, places, and patterns before the next incident.

| Friction in the field | What that costs |
|---|---|
| Same suspect, five spellings, three stations | Hours lost reconciling identities by hand |
| Queries in Kanglish, files in English / Kannada | Search that misses what the officer meant |
| Intelligence that arrives *after* a series | Reactive policing instead of early intervention |
| Black-box “AI suggestions” | Outputs officers cannot defend in court |
| District silos | Links that never leave a local folder |

CrimeMatrix is built against that reality — for [Datathon 2026](https://hack2skill.com/event/datathon2026) and the KSP brief on conversational AI, analytics, and predictive policing.

---

## What officers can do

Not a chatbot bolted onto a database. An investigation loop: ask → reason → evidence → explain.

| | Capability | In practice |
|---|---|---|
| **01** | **Investigation Copilot** | Multi-turn Q&A with tool use, context, and structured reasoning — not one-shot answers |
| **02** | **Identity Resolution** | Phonetic matches, nicknames, and Kannada transliteration across district boundaries |
| **03** | **Modus Operandi Matching** | Serial links from behavioural fingerprints, not only shared names or phones |
| **04** | **Knowledge Graph** | People, cases, vehicles, phones, and locations as a navigable network |
| **05** | **Predictive Signals** | Forecasts, hotspot cues, and risk scores for proactive deployment |
| **06** | **Whisper Alerts** | Cross-district matches pushed when they matter — without a manual hunt |
| **07** | **Explainable Output** | Reasoning chain + confidence with every recommendation |
| **08** | **Court-Ready Reports** | Investigation summaries with evidence references and an audit trail |

---

## How an investigation flows

```mermaid
flowchart LR
  A["Officer asks<br/>EN · KN · Kanglish"] --> B["Language<br/>normalisation"]
  B --> C["Agent plans<br/>& calls tools"]
  C --> D["Search · Graph<br/>Identity · Predict"]
  D --> E["Answer + rationale<br/>+ confidence"]
```

**Example**

> *“Show me similar robbery cases across Karnataka.”*

CrimeMatrix returns matched cases across districts — with **why** they match and **how confident** the link is — not a flat keyword dump.

---

## System at a glance

Three cooperating services. One investigation surface.

```mermaid
flowchart TB
  subgraph Client["Interface"]
    FE["React 19 · Vite · Tailwind"]
  end

  subgraph Core["Platform"]
    API["Backend API · FastAPI"]
    AI["AI Services · Agent · RAG · Tools"]
  end

  subgraph Intelligence["Models & stores"]
    LLM["Ollama · Gemini · OpenAI"]
    DB[("SQLite")]
    VEC["FAISS · NetworkX"]
  end

  FE --> API
  API --> AI
  AI --> LLM
  API --> DB
  AI --> VEC
  AI --> DB
```

| Layer | Choice |
|---|---|
| Interface | React 19, Vite, Tailwind CSS 4 |
| API & data | FastAPI, SQLAlchemy, SQLite |
| Intelligence | Agent loop, FAISS, NetworkX, sentence-transformers |
| LLM providers | Ollama (local default) · Gemini · OpenAI |

Design rationale and deeper diagrams live in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/DESIGN-DECISIONS.md`](docs/DESIGN-DECISIONS.md).

---

## Run locally

**You need:** Docker and Docker Compose.

```bash
git clone https://github.com/bhuwanb23/CrimeMatrix.git
cd CrimeMatrix
docker compose up
```

| Service | URL |
|---|---|
| Application | [http://localhost:5173](http://localhost:5173) |
| Backend API | [http://localhost:8000/docs](http://localhost:8000/docs) |
| AI Services | [http://localhost:8002/docs](http://localhost:8002/docs) |

Ollama pulls `llama3.2:1b` on first start. Optional cloud keys go in each service’s `.env`.

<details>
<summary><strong>Manual setup</strong> (without Docker)</summary>

<br/>

Run order: **backend → seed → AI (+ Ollama) → frontend**.

```bash
# 1 · Backend
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload

# 2 · Seed (API must be up)
python -m seed --fresh
python -m seed --bootstrap-only

# 3 · AI services
cd ../ai-services
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8002 --reload

# 4 · Frontend
cd ../frontend
npm install && npm run dev
```

For local LLMs: [install Ollama](https://ollama.com/), then `ollama pull llama3.2:1b`.  
Full deployment notes: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

</details>

---

## Documentation

| Document | What’s inside |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System design, agent loop, data flow |
| [`docs/DESIGN-DECISIONS.md`](docs/DESIGN-DECISIONS.md) | Why each major choice was made |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Environments, configuration, ops checklist |
| [`docs/API.md`](docs/API.md) | REST surfaces (Swagger-backed) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute |
| [`SECURITY.md`](SECURITY.md) | How to report vulnerabilities |

---

## License

Released under the [MIT License](LICENSE).

Built for **[Datathon 2026](https://hack2skill.com/event/datathon2026)** — conversational AI, analytics, and predictive policing for Karnataka State Police.
