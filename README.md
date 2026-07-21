<div align="center">

![CrimeMatrix Dashboard](frontend/src/assets/hero.png)

# CrimeMatrix

**AI Investigation Copilot for Karnataka State Police**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![CI](https://img.shields.io/badge/CI-Passing-brightgreen)
![Tests](https://img.shields.io/badge/87-Tests-Passing-brightgreen)

</div>

---

An intelligent crime investigation platform that transforms how law enforcement officers investigate crimes, identify suspects, and uncover criminal networks across Karnataka's 31 districts.

**Handles 200,000+ FIRs annually** — resolving fragmented identities, connecting cross-district cases, and delivering explainable AI recommendations with reasoning chains.

---

## Features

| | Feature | Description |
|---|---------|-------------|
| | **AI Copilot** | Natural language investigation assistant with multi-turn context |
| | **Identity Resolution** | Phonetic matching, 28+ nickname mappings, Kannada transliteration |
| | **Knowledge Graph** | Criminal network analysis across 68 interconnected data models |
| | **Predictive Analytics** | Crime forecasting, hotspot detection, risk scoring |
| | **Explainable AI** | Every recommendation includes reasoning chain and confidence score |
| | **Kanglish Support** | Understands "Bellary suspect ge phone match check madi" naturally |

---

## Quick Start

```bash
git clone https://github.com/your-org/CrimeMatrix.git
cd CrimeMatrix
docker compose up
```

> **5 minutes to running** — Access at `http://localhost:5173`

<details>
<summary>Manual setup</summary>

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && python seed_crimes.py
uvicorn main:app --port 8000

# AI Services
cd ai-services && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8002

# Frontend
cd frontend && npm install && npm run dev
```

</details>

---

## Architecture

```mermaid
graph LR
    subgraph Frontend["Frontend — React 19"]
        UI[Dashboard + Copilot]
    end
    
    subgraph Backend["Backend API — FastAPI"]
        API[50+ Endpoints]
        DB[(SQLite — 68 Tables)]
    end
    
    subgraph AI["AI Services — FastAPI"]
        Agent[Agent Loop]
        Tools[28 Tools]
        KG[Knowledge Graph]
        RAG[RAG Pipeline]
        Predict[Prediction Engine]
    end
    
    subgraph Providers["AI Providers"]
        Ollama[Ollama — Local]
        OpenAI[OpenAI — Cloud]
        Gemini[Gemini — Cloud]
    end
    
    UI -->|REST + SSE| API
    API --> DB
    API --> Agent
    Agent --> Tools
    Agent --> KG
    Agent --> RAG
    Agent --> Predict
    Agent --> Ollama
    Agent --> OpenAI
    Agent --> Gemini
```

Three independent services — deployable separately, scalable independently. See [Architecture Docs](docs/ARCHITECTURE.md) for details.

---

## Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local-F59E0B)
![FAISS](https://img.shields.io/badge/FAISS-Vector-009688)
![NetworkX](https://img.shields.io/badge/NetworkX-Graph-FF6600)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

---

## API

Two REST APIs with interactive documentation:

| Service | URL | Endpoints |
|---------|-----|-----------|
| Backend API | `localhost:8000/docs` | 50+ crime data, investigations, search |
| AI Services | `localhost:8002/docs` | 70+ AI reasoning, RAG, predictions |

---

## Community

- [GitHub Issues](https://github.com/your-org/CrimeMatrix/issues) — Bug reports & feature requests
- [Contributing Guide](CONTRIBUTING.md) — How to contribute
- [Security Policy](SECURITY.md) — Vulnerability reporting

---

## License

[MIT](LICENSE)
