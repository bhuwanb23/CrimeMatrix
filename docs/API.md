# API Reference

CrimeMatrix exposes two REST APIs. Both provide interactive documentation via Swagger UI.

---

## Backend API (`http://localhost:8000/api/v1/`)

The primary API for crime data, investigations, search, and analytics.

### Core Resources

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | System status |
| `/version` | GET | API version |
| `/config` | GET | Configuration |
| `/metadata` | GET | Database metadata |
| `/statistics` | GET | Crime statistics |

### Crime Data

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/crimes` | GET/POST | List/create crimes |
| `/crimes/{id}` | GET/PUT/DELETE | Get/update/delete crime |
| `/persons` | GET/POST | List/create persons |
| `/criminals` | GET/POST | List/create criminals |
| `/victims` | GET/POST | List/create victims |
| `/witnesses` | GET/POST | List/create witnesses |
| `/officers` | GET/POST | List/create officers |
| `/stations` | GET/POST | List/create stations |
| `/districts` | GET/POST | List/create districts |
| `/vehicles` | GET/POST | List/create vehicles |
| `/phones` | GET/POST | List/create phones |
| `/locations` | GET/POST | List/create locations |
| `/crime-types` | GET/POST | List/create crime types |

### Investigation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/investigations` | GET/POST | List/create investigations |
| `/investigations/{id}` | GET/PUT | Get/update investigation |
| `/notes` | GET/POST | Investigation notes |
| `/bookmarks` | GET/POST | Saved investigations |
| `/timeline` | GET/POST | Investigation timeline events |
| `/attachments` | GET/POST | Case attachments |
| `/case-links` | GET/POST | Links between cases |
| `/case-status` | GET/POST | Case status changes |

### Search & Intelligence

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search` | POST | General search |
| `/search/semantic` | POST | Semantic search |
| `/search/district` | POST | District-scoped search |
| `/search/saved` | GET | Saved searches |
| `/search/history` | GET | Search history |
| `/similar-cases` | GET/POST | Similar case discovery |
| `/recommendations` | GET | AI case recommendations |
| `/intelligence` | GET | Intelligence feed |
| `/patterns` | GET | Crime patterns |
| `/trends` | GET | Crime trends |
| `/hotspots` | GET | Crime hotspots |
| `/maps` | GET | Geospatial data |

### Criminal Analysis

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/criminal-timeline` | GET | Criminal activity timeline |
| `/behavior` | GET | Behavioral profiles |
| `/repeat-offenders` | GET | Repeat offender tracking |
| `/mo` | GET/POST | Modus operandi profiles |

### AI Analytics

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analytics` | GET | Crime analytics |
| `/analytics-dashboard` | GET | Dashboard aggregations |
| `/predictions` | GET/POST | Crime predictions |
| `/early-warning` | GET | Early warning alerts |
| `/suspect-risk` | GET | Suspect risk scores |
| `/priorities` | GET | Case prioritization |

### Infrastructure

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/graph` | GET/POST | Knowledge graph operations |
| `/reports` | GET/POST | Report generation |
| `/notifications` | GET | System notifications |
| `/audit` | GET | Audit trail |
| `/memory` | GET | Investigation memory |
| `/embeddings` | GET/POST | Vector embeddings |
| `/monitoring` | GET | System monitoring |
| `/storage` | GET/POST | File storage |
| `/copilot` | POST | AI copilot chat |

### Example: Search for Crimes

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "robbery in Bengaluru",
    "filters": {
      "district": "Bengaluru Urban",
      "crime_type": "Robbery"
    },
    "limit": 10
  }'
```

### Example: Get Crime Detail

```bash
curl http://localhost:8000/api/v1/crimes/1
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Armed robbery at jewelry store on MG Road",
    "description": "Two suspects entered the store at 2:30 AM...",
    "status": "open",
    "priority": "high",
    "district": "Bengaluru Urban",
    "crime_type": "Robbery"
  }
}
```

---

## AI Services API (`http://localhost:8002/api/ai/`)

The intelligence layer — AI-powered analysis, reasoning, and predictions.

### Chat & Agent

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Chat with AI agent |
| `/chat/stream` | POST | Streaming chat (SSE) |
| `/agents` | GET | List available agents |
| `/agents/{id}` | GET | Get agent details |
| `/sessions` | GET | List active sessions |
| `/sessions/{id}/trace` | GET | Get session reasoning trace |
| `/sessions/{id}` | DELETE | Clear session |

### Memory

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/memory/sessions/{id}/history` | GET | Session conversation history |
| `/memory/sessions/{id}/summary` | GET | Session summary |
| `/memory/investigation` | POST | Load investigation context |
| `/memory/preferences/{user_id}` | GET/PUT | User preferences |
| `/memory/working` | GET | Working memory |

### Tools

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tools` | GET | List all 28 tools |
| `/tools/{name}` | GET | Get tool schema |
| `/tools/invoke` | POST | Invoke a tool directly |

### RAG (Retrieval-Augmented Generation)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rag/index` | POST | Index documents |
| `/rag/search` | POST | RAG search with citations |
| `/rag/stats` | GET | Index statistics |
| `/rag/citations/{session_id}` | GET | Session citations |

### Search Intelligence

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search/intelligent` | POST | Full intelligent search pipeline |
| `/search/similar` | POST | Find similar cases |
| `/search/cross-district` | POST | Cross-district search |
| `/search/expand` | POST | Query expansion |
| `/search/rewrite` | POST | Query rewriting |
| `/search/rerank` | POST | Result reranking |

### Identity Resolution

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/identity/match` | POST | Match two names |
| `/identity/match/batch` | POST | Batch name matching |
| `/identity/transliterate` | POST | Transliterate text |
| `/identity/duplicates` | POST | Find duplicate records |
| `/identity/resolve` | POST | Resolve entity mention |
| `/identity/merge` | POST | Merge duplicate records |
| `/identity/aliases` | POST | Detect aliases |

### Knowledge Graph

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/knowledge/build` | POST | Build graph from backend data |
| `/knowledge/query` | POST | Query graph relationships |
| `/knowledge/network` | POST | Criminal network analysis |
| `/knowledge/discover` | POST | Discover hidden connections |
| `/knowledge/timeline` | POST | Generate entity timelines |
| `/knowledge/analyze` | POST | Graph analysis (centrality, communities) |

### Reasoning

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reasoning/analyze` | POST | Full reasoning analysis |
| `/reasoning/chain` | POST | Build reasoning chain |
| `/reasoning/confidence` | POST | Calculate confidence |
| `/reasoning/evidence` | POST | Rank evidence |
| `/reasoning/explain` | POST | Generate explanation |

### Predictions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict/forecast` | POST | Crime forecasting |
| `/predict/hotspots` | POST | Hotspot prediction |
| `/predict/recidivism` | POST | Recidivism prediction |
| `/predict/risk` | POST | Risk scoring |
| `/predict/mo-similarity` | POST | MO similarity comparison |
| `/predict/cases` | POST | Case recommendations |

### Language

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/language/stt` | POST | Speech-to-text |
| `/language/tts` | POST | Text-to-speech |
| `/language/translate` | POST | Translate text |
| `/language/kanglish` | POST | Normalize Kanglish |
| `/language/normalize` | POST | Normalize query |

### Workflows

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/workflows` | GET | List available workflows |
| `/workflows/{name}` | GET | Get workflow details |
| `/workflows/{name}/steps` | GET | Get workflow steps |
| `/workflows/run` | POST | Execute a workflow |

### Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/monitor/latency` | GET | Latency statistics |
| `/monitor/tokens` | GET | Token usage |
| `/monitor/hallucination` | GET | Hallucination metrics |
| `/monitor/tools` | GET | Tool success rates |
| `/monitor/accuracy` | GET | Accuracy metrics |
| `/monitor/confidence` | GET | Confidence distribution |
| `/monitor/cost` | GET | Cost analysis |
| `/monitor/feedback` | GET/POST | User feedback |
| `/monitor/dashboard` | GET | Full monitoring dashboard |
| `/monitor/summary` | GET | Summary statistics |

### Example: Chat with AI

```bash
curl -X POST http://localhost:8002/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me similar robbery cases across Karnataka",
    "session_id": "investigation-001",
    "use_tools": true
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "response": "Found 12 similar cases across 4 districts...",
    "reasoning_trace": [
      {"type": "thinking", "content": "Planning approach for: Show me similar robbery cases..."},
      {"type": "plan", "content": "Created plan with 3 steps"},
      {"type": "step_start", "content": "Executing: Search for robbery cases"},
      {"type": "step_complete", "content": "Step completed: Found 45 matching cases"}
    ],
    "steps": 3,
    "total_time_ms": 2847.5
  }
}
```

### Example: Identity Match

```bash
curl -X POST http://localhost:8002/api/ai/identity/match \
  -H "Content-Type: application/json" \
  -d '{"name1": "Rajesh Kumar", "name2": "Raj Kumar"}'
```

Response:
```json
{
  "success": true,
  "data": {
    "score": 70,
    "match_type": "nickname",
    "details": "Parts: 50, Nickname: 30, Phonetic: 0"
  }
}
```

---

## Streaming (SSE)

The chat endpoint supports Server-Sent Events for real-time streaming:

```javascript
const eventSource = new EventSource(
  'http://localhost:8002/api/ai/chat/stream?' +
  new URLSearchParams({ message: 'Hello', session_id: 'test' })
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'message') {
    process.stdout.write(data.content);
  }
};
```

Event types:
- `plan` — Agent created a plan
- `step_start` — Executing a tool
- `step_complete` — Tool execution complete
- `thinking` — Agent is reasoning
- `message` — Response content chunk
- `done` — Stream complete
