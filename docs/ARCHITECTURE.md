# Architecture

CrimeMatrix is a three-service AI investigation platform designed for the Karnataka State Police. This document covers system design, data flow, and the reasoning behind each architectural choice.

---

## System Overview

```mermaid
graph TB
    subgraph Frontend["Frontend — React 19 + Tailwind 4"]
        UI[SPA Dashboard]
        Copilot[AI Copilot Chat]
        GraphViz[Graph Visualization]
        Maps[Geospatial Maps]
    end

    subgraph Backend["Backend API — FastAPI :8000"]
        API[REST API — 50+ endpoints]
        Models[68 SQLAlchemy Models]
        Services[38 Service Classes]
        Search[Search Engine]
        Analytics[Analytics Engine]
    end

    subgraph AIServices["AI Services — FastAPI :8002"]
        Agent[AI Agent Loop]
        Tools[28 Specialized Tools]
        RAG[RAG Pipeline]
        KG[Knowledge Graph]
        Reasoning[Reasoning Engine]
        Prediction[Prediction Engine]
        Identity[Identity Resolver]
        Language[Language Pipeline]
        Memory[Memory System]
    end

    subgraph Storage["Data Stores"]
        SQLite[(SQLite — 68 tables)]
        FAISS[(FAISS — Vector Store)]
        NX[(NetworkX — Graph)]
    end

    subgraph LLM["AI Providers"]
        Ollama[Ollama — Local Default]
        OpenAI[OpenAI — Optional]
        Gemini[Gemini — Optional]
    end

    UI --> API
    Copilot --> API
    GraphViz --> API
    Maps --> API

    API --> Models
    API --> Services
    API --> Search
    API --> Analytics

    API --> Agent
    Agent --> Tools
    Agent --> RAG
    Agent --> Reasoning

    Tools --> KG
    Tools --> Prediction
    Tools --> Identity
    Tools --> Language

    Models --> SQLite
    RAG --> FAISS
    KG --> NX

    Agent --> Ollama
    Agent --> OpenAI
    Agent --> Gemini
    Reasoning --> Ollama
    Language --> Ollama
```

---

## Request Flow

How a user query flows through the entire system:

```mermaid
sequenceDiagram
    participant Officer
    participant Frontend
    participant Backend
    participant AIServices
    participant LLM

    Officer->>Frontend: "Show similar robbery cases in Karnataka"
    Frontend->>Backend: POST /api/v1/copilot/chat
    Backend->>AIServices: POST /api/ai/chat

    Note over AIServices: Language Pipeline
    AIServices->>AIServices: Detect language (English)
    AIServices->>AIServices: Normalize query

    Note over AIServices: Agent Loop
    AIServices->>LLM: Plan: decompose query into steps
    LLM-->>AIServices: Plan: [search_similar, graph_traverse, predict]

    loop For each step
        AIServices->>AIServices: Execute tool
        AIServices->>Backend: Fetch crime data (if needed)
        Backend-->>AIServices: Crime records
    end

    AIServices->>AIServices: Build context from results
    AIServices->>LLM: Generate response with context
    LLM-->>AIServices: Response with reasoning chain

    AIServices-->>Backend: Response + reasoning trace
    Backend-->>Frontend: SSE stream / JSON response
    Frontend-->>Officer: Display results with reasoning
```

---

## AI Agent Loop

The core of CrimeMatrix is a structured reasoning loop, not a free-form chatbot:

```mermaid
flowchart LR
    Query[User Query] --> Greeting{Is Greeting?}
    Greeting -->|Yes| Respond[Return Greeting]
    Greeting -->|No| Plan[Planner]

    Plan -->|"LLM decomposes into steps"| Steps[Plan Steps]
    Steps --> Execute[Executor]

    Execute -->|"Run each tool"| Tool1[Tool 1]
    Execute --> Tool2[Tool 2]
    Execute --> Tool3[Tool N]

    Tool1 --> Result1[Result 1]
    Tool2 --> Result2[Result 2]
    Tool3 --> ResultN[Result N]

    Result1 --> Build[Context Builder]
    Result2 --> Build
    ResultN --> Build

    Build -->|"Compile results + query"| Context[Structured Context]
    Context --> Respond2[Responder]
    Respond2 -->|"LLM generates answer"| Answer[Final Response]
    Answer --> Memory[Update Memory]
    Answer --> Trace[Reasoning Trace]

    style Plan fill:#f59e0b,color:#000
    style Execute fill:#3b82f6,color:#fff
    style Build fill:#10b981,color:#fff
    style Respond2 fill:#8b5cf6,color:#fff
```

### Why This Design?

- **Deterministic execution** — Tools are called with exact parameters, no hallucinated tool calls
- **Transparent reasoning** — Every step is tracked in a reasoning trace
- **Retry with backoff** — Failed tool calls retry up to 2 times
- **Greeting short-circuit** — Simple greetings skip the entire pipeline

---

## Knowledge Graph

The knowledge graph connects entities across the investigation domain:

```mermaid
graph LR
    subgraph Entities
        Person[Person]
        Crime[Crime]
        Vehicle[Vehicle]
        Officer[Officer]
        Station[Station]
        District[District]
        Phone[Phone]
    end

    subgraph Relationships
        R1[reported_in]
        R2[involved_in]
        R3[owns]
        R4[has_phone]
        R5[works_at]
        R6[located_in]
        R7[investigated_by]
    end

    Person -->|R2| Crime
    Person -->|R3| Vehicle
    Person -->|R4| Phone
    Crime -->|R1| Station
    Crime -->|R7| Officer
    Station -->|R6| District
    Officer -->|R5| Station

    style Person fill:#f59e0b,color:#000
    style Crime fill:#ef4444,color:#fff
    style Vehicle fill:#3b82f6,color:#fff
    style Officer fill:#10b981,color:#fff
```

### Graph Operations

| Operation | Purpose | Tool |
|-----------|---------|------|
| **Traversal** | Find all entities connected to a node | `graph_traverse` |
| **Shortest Path** | Find connection between two entities | `graph_shortest_path` |
| **Neighbors** | Get direct connections | `graph_neighbors` |
| **Community Detection** | Identify criminal clusters | `link_analysis.communities` |
| **Centrality** | Find key players in network | `link_analysis.centrality` |
| **Hidden Connections** | Discover indirect links | `relationship.find_hidden` |

---

## Memory Architecture

The memory system has four layers, each serving a different purpose:

```mermaid
graph TB
    subgraph MemorySystem["Memory Manager"]
        Session[Session Memory]
        Working[Working Memory]
        Investigation[Investigation Context]
        Preferences[User Preferences]
    end

    subgraph Persistence["Persistence Layer"]
        SQLite2[(SQLite Store)]
    end

    subgraph Compression["Context Compressor"]
        Compressor[Auto-Compress]
    end

    Session -->|"Auto-compress when >50 messages"| Compressor
    Compressor -->|"Summary replaces old messages"| Session

    Session --> SQLite2
    Working -->|"Scratchpad for active case"| Working
    Investigation -->|"Load case data on demand"| Investigation

    MemorySystem -->|"Inject into system prompt"| LLM[LLM Context]

    style Session fill:#f59e0b,color:#000
    style Working fill:#3b82f6,color:#fff
    style Investigation fill:#8b5cf6,color:#fff
    style Preferences fill:#10b981,color:#fff
```

| Layer | Purpose | Lifetime |
|-------|---------|----------|
| **Session Memory** | Conversation history with auto-compression | Per session |
| **Working Memory** | Short-term scratchpad for active investigation | Per turn |
| **Investigation Context** | Loaded case data for context injection | Per investigation |
| **User Preferences** | Per-user settings and preferences | Persistent |

---

## Search Intelligence Pipeline

CrimeMatrix doesn't just search — it intelligently processes queries:

```mermaid
flowchart LR
    Query[User Query] --> Rewrite[Query Rewrite]
    Rewrite -->|"LLM rewrites ambiguous queries"| Expand[Query Expansion]
    Expand -->|"LLM adds related terms"| Hybrid[Hybrid Search]
    Hybrid -->|"Semantic + Keyword"| Rerank[Result Reranking]
    Rerank -->|"LLM ranks by relevance"| Results[Top-K Results]

    subgraph HybridDetails["Hybrid Search"]
        Semantic[FAISS Semantic]
        Keyword[Keyword Match]
    end

    Hybrid --> Semantic
    Hybrid --> Keyword

    Results --> Citations[Citation Manager]
    Results --> Context[Context Builder]

    style Rewrite fill:#f59e0b,color:#000
    style Expand fill:#f59e0b,color:#000
    style Hybrid fill:#3b82f6,color:#fff
    style Rerank fill:#8b5cf6,color:#fff
```

### Pipeline Stages

1. **Query Rewrite** — LLM rewrites ambiguous or incomplete queries
2. **Query Expansion** — LLM adds related terms and synonyms
3. **Hybrid Search** — Combines FAISS semantic search with keyword matching
4. **Result Reranking** — LLM re-ranks results by relevance to the original query
5. **Citation Tracking** — Sources are tracked per session for accountability

---

## Identity Resolution Engine

The most domain-specific component — solving the fragmented identity problem unique to Indian law enforcement:

```mermaid
flowchart TB
    Input[Name Input] --> Normalize[Normalize]
    Normalize --> Parts[Split into Parts]

    Parts --> Exact{Exact Match?}
    Exact -->|Yes| Score100[Score: 100]

    Parts --> Nickname[Nickname Check]
    Nickname -->|"Raj ↔ Rajesh ↔ Rajendra"| NickBonus[Nickname Bonus: +30]

    Parts --> Phonetic[Soundex Phonetic]
    Phonetic -->|"Kumar ≈ Kumer"| PhonoBonus[Phonetic Bonus: +20]

    Parts --> Vowel[Vowel Normalize]
    Vowel -->|"Sridhar ≈ Shridhar"| VowelBonus[Vowel Bonus: +10]

    Parts --> Surname[Surname Match]
    Surname -->|"Gowda ≈ Gowdar"| SurnameBonus[Surname Bonus: +10]

    NickBonus --> Final[Final Score]
    PhonoBonus --> Final
    VowelBonus --> Final
    SurnameBonus --> Final

    Final --> Match{Score > 50?}
    Match -->|Yes| Matched[Same Person]
    Match -->|No| Different[Different Person]

    style Normalize fill:#f59e0b,color:#000
    style Nickname fill:#ef4444,color:#fff
    style Phonetic fill:#3b82f6,color:#fff
    style Vowel fill:#8b5cf6,color:#fff
    style Surname fill:#10b981,color:#fff
```

### Matching Strategies

| Strategy | Weight | Example |
|----------|--------|---------|
| **Exact match** | 100 | "Rajesh" = "Rajesh" |
| **Nickname** | +30 | "Raj" = "Rajesh" = "Rajendra" |
| **Phonetic (Soundex)** | +20 | "Kumar" ≈ "Kumer" |
| **Vowel normalization** | +10 | "Sridhar" ≈ "Shridhar" |
| **Surname variant** | +10 | "Gowda" ≈ "Gowdar" |
| **Prefix match** | +40 | "Rajesh" starts with "Raj" |

---

## Prediction Engine

Six prediction models working together:

```mermaid
graph TB
    subgraph PredictionEngine["Prediction Engine"]
        Forecast[Crime Forecasting]
        Hotspot[Hotspot Detection]
        Recidivism[Repeat Offender]
        Risk[Risk Scoring]
        MO[MO Similarity]
        Recommender[Case Recommender]
    end

    subgraph Data["Input Data"]
        Historical[Historical Crimes]
        Profiles[Suspect Profiles]
        Cases[Case Details]
    end

    Historical --> Forecast
    Historical --> Hotspot
    Profiles --> Recidivism
    Profiles --> Risk
    Cases --> MO
    Cases --> Recommender

    Forecast --> Output[Predictions & Recommendations]
    Hotspot --> Output
    Recidivism --> Output
    Risk --> Output
    MO --> Output
    Recommender --> Output

    style Forecast fill:#f59e0b,color:#000
    style Hotspot fill:#ef4444,color:#fff
    style Recidivism fill:#3b82f6,color:#fff
    style Risk fill:#8b5cf6,color:#fff
    style MO fill:#10b981,color:#fff
    style Recommender fill:#06b6d4,color:#fff
```

| Model | Purpose | Method |
|-------|---------|--------|
| **Crime Forecasting** | Predict future crime volume | Time-series analysis |
| **Hotspot Detection** | Identify high-risk areas | Geographic clustering |
| **Repeat Offender** | Predict recidivism | Profile-based scoring |
| **Risk Scoring** | Assess suspect risk level | Multi-factor analysis |
| **MO Similarity** | Compare modus operandi | Behavioral fingerprinting |
| **Case Recommender** | Prioritize investigations | Multi-criteria scoring |

---

## Data Model

The database has 68 models organized into seven entity groups:

```mermaid
erDiagram
    CRIME ||--o{ PERSON : involves
    CRIME }o--|| DISTRICT : occurs_in
    CRIME }o--|| STATION : reported_to
    CRIME }o--|| CRIME_TYPE : classified_as
    PERSON ||--o{ VEHICLE : owns
    PERSON ||--o{ PHONE : has
    PERSON ||--o{ CRIMINAL : is
    CRIMINAL ||--o{ OFFENDER_SCORE : scored
    CRIMINAL ||--o{ REPEAT_OFFENDER : tracked
    CRIMINAL ||--o{ BEHAVIOR_PROFILE : profiled
    CRIME ||--o{ EVIDENCE : has
    CRIME ||--o{ INVESTIGATION : investigated
    CRIME ||--o{ TIMELINE_EVENT : recorded
    CRIME ||--o{ CASE_LINK : linked
    CRIME ||--o{ CRIME_PATTERN : pattern
    CRIME ||--o{ CRIME_PREDICTION : predicted
    CRIME ||--o{ ALERT_EVENT : triggers
    OFFICER ||--o{ INVESTIGATION : conducts
    OFFICER }o--|| STATION : assigned
    STATION }o--|| DISTRICT : located_in
    SUSPECT }o--|| PERSON : is
    SUSPECT ||--o{ SUSPECT_RISK_SCORE : scored
    VICTIM }o--|| PERSON : is
    WITNESS }o--|| PERSON : is
```

### Entity Groups

| Group | Models | Purpose |
|-------|--------|---------|
| **Core** | Crime, Person, Criminal, Victim, Witness, Suspect | People and events |
| **Geography** | District, Station, Location | Spatial context |
| **Investigation** | Investigation, Evidence, Report, CaseLink, Note, Bookmark | Case management |
| **Intelligence** | CrimePattern, PatternCluster, MoProfile, BehaviorProfile, RepeatOffender | Pattern analysis |
| **Prediction** | CrimePrediction, CrimeForecast, Hotspot, OffenderScore, RiskScoreHistory | Predictive analytics |
| **Knowledge** | GraphMeta, CaseSimilarity, CaseEmbedding, MoEmbedding | AI intelligence |
| **Operations** | Alert, AlertRule, EarlyWarningAlert, Notification, Audit | System operations |
