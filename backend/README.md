# CrimeMatrix Backend API

The primary REST API for crime data, investigations, search, and analytics.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Seed database
python seed_crimes.py

# Start server
uvicorn main:app --port 8000 --reload
```

API docs: `http://localhost:8000/docs`

## Architecture

```
backend/
├── app/
│   ├── api/v1/          # 50+ REST endpoints
│   ├── models/          # 68 SQLAlchemy models
│   ├── services/        # 38 business logic classes
│   ├── repositories/    # Data access layer
│   ├── schemas/         # Pydantic schemas
│   ├── db/              # Database session management
│   ├── audit/           # Audit middleware
│   ├── cache/           # Caching layer
│   ├── core/            # Logging, exceptions, config
│   ├── graph/           # NetworkX graph operations
│   ├── vector/          # FAISS vector store
│   ├── embeddings/      # Embedding services
│   ├── search/          # Search engine
│   ├── analytics/       # Analytics engine
│   ├── notifications/   # Notification system
│   ├── reports/         # Report generation
│   └── monitoring/      # System monitoring
├── alembic/             # 25 database migrations
├── tests/               # Test suite
├── seed_crimes.py       # Demo data seeder
└── config.py            # Pydantic Settings
```

## Tech Stack

- **Framework:** FastAPI 0.115
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Database:** SQLite (aiosqlite)
- **Graph:** NetworkX
- **Vector:** FAISS
- **Cache:** diskcache
- **Logging:** structlog

## API Endpoints

| Category | Prefix | Count |
|----------|--------|-------|
| Core | `/health`, `/status`, `/config` | 6 |
| Crime Data | `/crimes`, `/persons`, `/criminals` | 13 |
| Investigation | `/investigations`, `/notes`, `/bookmarks` | 8 |
| Search | `/search`, `/search/semantic` | 5 |
| Intelligence | `/similar-cases`, `/patterns`, `/trends` | 8 |
| AI Analytics | `/predictions`, `/early-warning` | 6 |
| Infrastructure | `/graph`, `/reports`, `/audit` | 10 |

## Database

68 SQLAlchemy models organized into 7 entity groups:

- **Core:** Crime, Person, Criminal, Victim, Witness, Suspect
- **Geography:** District, Station, Location
- **Investigation:** Investigation, Evidence, Report, CaseLink
- **Intelligence:** CrimePattern, MoProfile, BehaviorProfile
- **Prediction:** CrimePrediction, Hotspot, OffenderScore
- **Knowledge:** GraphMeta, CaseSimilarity, CaseEmbedding
- **Operations:** Alert, Notification, Audit

## Testing

```bash
python -m pytest tests/ -v
```
