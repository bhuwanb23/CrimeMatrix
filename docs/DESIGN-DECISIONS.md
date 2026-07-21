# Design Decisions

This document records the key architectural decisions behind CrimeMatrix, why each was made, and what alternatives were considered.

---

## 1. Three Services, Not a Monolith

**Decision:** Split the system into Backend API, AI Services, and Frontend — three independent FastAPI/React services.

**Context:** CrimeMatrix combines traditional CRUD operations (crime records, investigations, reports) with compute-heavy AI operations (LLM calls, graph analysis, vector search). These have different resource profiles and scaling needs.

**Alternatives Considered:**
- *Monolith with AI modules* — Simpler deployment, but AI operations would block CRUD requests during LLM inference
- *Microservices (10+ services)* — Over-engineered for the current scale; adds deployment complexity

**Rationale:**
- AI services can scale independently (more LLM calls = more AI instances)
- Backend stays responsive during long AI operations
- Frontend can be deployed as a static site separate from APIs
- Each service has its own dependency tree (AI services need sentence-transformers; backend needs SQLAlchemy)

**Trade-off:** Requires HTTP communication between services (additionals latency), but this is acceptable at the current scale.

---

## 2. Plan → Execute → Respond (Not ReAct)

**Decision:** Use a structured agent loop where the LLM plans steps first, then executes them deterministically, rather than the ReAct pattern where the LLM decides actions at each step.

**Context:** In law enforcement, hallucinated tool calls are dangerous. An AI that invents a tool call like `arrest_suspect(id=123)` is worse than no AI at all.

**Alternatives Considered:**
- *ReAct (Reason + Act)* — LLM decides which tool to call at each step. More flexible, but can hallucinate tool names and parameters
- *Function calling* — LLM outputs structured tool calls. Better than ReAct, but still allows the LLM to choose non-existent tools
- *Hardcoded pipelines* — Fixed sequences for known query types. Too rigid for open-ended queries

**Rationale:**
- Planning phase decomposes the query into validated steps
- Execution phase only runs tools that actually exist in the registry
- If the LLM plans a non-existent tool, the executor returns an error gracefully
- The reasoning trace is fully auditable — every step is logged

**Trade-off:** Less flexible than ReAct for novel query types, but safer and more predictable for law enforcement use.

---

## 3. Ollama as Default Provider

**Decision:** Default to Ollama (local inference) over cloud providers (OpenAI, Gemini).

**Context:** Karnataka police stations may have unreliable internet. A system that requires cloud API keys to function is useless in the field.

**Alternatives Considered:**
- *OpenAI as default* — Better model quality, but requires API key, internet, and costs money per query
- *Gemini as default* — Good multilingual support, but same dependency issues
- *Self-hosted vLLM* — Best performance, but requires GPU hardware

**Rationale:**
- Zero-config startup — no API keys needed for demo
- Offline-first — works without internet
- Privacy — data never leaves the local machine
- Cost — no per-query charges during development
- Fallback to cloud providers when available (OpenAI/Gemini auto-registered if keys exist)

**Trade-off:** Local models (llama3.2:1b) are less capable than cloud models. The system handles this by supporting multiple providers and letting users choose.

---

## 4. SQLite Over PostgreSQL

**Decision:** Use SQLite with async driver (aiosqlite) instead of PostgreSQL.

**Context:** This is a hackathon project that needs to be portable. Officers should be able to clone and run it without installing a database server.

**Alternatives Considered:**
- *PostgreSQL* — Production-grade, better concurrency, full-text search. But requires separate installation and configuration
- *MongoDB* — Flexible schema, good for varied crime data. But loses relational integrity
- *MySQL* — Common in Indian government systems. But same installation burden as PostgreSQL

**Rationale:**
- Zero-config — database file is just `data/crimematrix.db`
- Portable — entire database is a single file
- Async support — aiosqlite provides concurrent access
- Alembic migrations work with SQLite
- Sufficient for demo scale (thousands of records, not millions)

**Trade-off:** SQLite has limited concurrency (write-locks entire database) and no full-text search. Acceptable for demo; would switch to PostgreSQL for production at scale.

---

## 5. In-Memory FAISS Over Vector Database

**Decision:** Use FAISS (CPU) for vector storage instead of a dedicated vector database (Pinecone, Weaviate, Qdrant).

**Context:** The RAG pipeline needs semantic search over crime documents. At demo scale, a full vector database is overkill.

**Alternatives Considered:**
- *Pinecone* — Managed, fast, scalable. But requires cloud account and costs money
- *Weaviate* — Open-source, feature-rich. But requires separate service
- *pgvector* — PostgreSQL extension. Good if already using PostgreSQL
- *Chroma* — Simple, Python-native. But FAISS is more mature

**Rationale:**
- Zero external dependencies — FAISS is a Python package
- Fast enough for demo scale (thousands of documents)
- No separate service to manage
- Can migrate to a dedicated vector DB later without changing the interface

**Trade-off:** No persistence (index rebuilt on restart), no distributed search. Acceptable for demo; would use a dedicated vector DB in production.

---

## 6. NetworkX Over Neo4j

**Decision:** Use NetworkX for knowledge graph operations instead of Neo4j.

**Context:** The knowledge graph connects persons, crimes, vehicles, officers, and stations. At demo scale, an in-memory graph is sufficient.

**Alternatives Considered:**
- *Neo4j* — Industry standard for graph databases. Cypher query language. But requires separate service and setup
- *Amazon Neptune* — Managed graph database. But requires AWS account
- *ArangoDB* — Multi-model database. But complex setup

**Rationale:**
- Zero external dependencies — NetworkX is a Python package
- Full graph algorithms library (centrality, communities, shortest path)
- Graph can be built from backend API data in seconds
- No separate service to manage

**Trade-off:** No persistence (graph rebuilt on restart), limited to memory size. Acceptable for demo; would use Neo4j for production with millions of entities.

---

## 7. Kanglish as a Separate Module

**Decision:** Build a dedicated Kanglish (Kannada + English) normalizer instead of relying on generic translation.

**Context:** Karnataka police officers don't type in pure Kannada or pure English. They mix both: *"Bellary suspect ge phone match check madi"* (Check phone match for Bellary suspect). This is the real-world input pattern.

**Alternatives Considered:**
- *Google Translate API* — Handles Kannada → English. But adds latency, cost, and internet dependency
- *Generic multilingual model* — Can handle code-mixed text. But not tuned for Karnataka-specific patterns
- *Ignore the problem* — Just use English. Excludes most field officers

**Rationale:**
- Real-world usage pattern — officers type in Kanglish daily
- No internet dependency — dictionary-based normalization
- Fast — no LLM call needed for normalization
- Extensible — easy to add new Kanglish entries
- Works offline — critical for rural police stations

**Trade-off:** Limited vocabulary (needs manual dictionary updates), but covers the most common patterns.

---

## 8. Explainable Reasoning Chains

**Decision:** Every AI recommendation includes a reasoning chain with confidence scores, evidence ranking, and source attribution.

**Context:** In law enforcement, AI recommendations can lead to investigations, arrests, and court proceedings. A black-box recommendation is legally and ethically unacceptable.

**Alternatives Considered:**
- *Just show the answer* — Simpler, but officers can't verify or trust the recommendation
- *Show confidence only* — Better than nothing, but doesn't explain WHY
- *Full reasoning chain* — Most transparent, but more complex to implement

**Rationale:**
- Law enforcement requires audit trails — every action must be traceable
- Officers need to understand AI reasoning to make informed decisions
- Court proceedings require evidence and reasoning documentation
- Builds trust — officers who understand the AI are more likely to use it

**Trade-off:** Longer responses, more LLM tokens used. But transparency is non-negotiable for law enforcement.

---

## Summary

| Decision | Key Factor | Production Upgrade Path |
|----------|-----------|------------------------|
| Three services | Independent scaling | Add API gateway, service mesh |
| Plan→Execute→Respond | Safety over flexibility | Add ReAct fallback for low-risk queries |
| Ollama default | Offline-first, zero-config | Add cloud provider fallback |
| SQLite | Portability, zero-config | Switch to PostgreSQL |
| FAISS | Zero dependencies | Switch to Weaviate/Qdrant |
| NetworkX | Zero dependencies | Switch to Neo4j |
| Kanglish module | Real-world usage | Add LLM-based normalization |
| Explainable chains | Legal/ethical requirement | Add visual reasoning chains |
