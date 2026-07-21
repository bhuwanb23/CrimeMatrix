# CrimeMatrix AI Services

The intelligence layer — AI-powered analysis, reasoning, predictions, and the investigation copilot.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama (separate terminal)
ollama serve
ollama pull llama3.2:1b

# Start server
uvicorn main:app --port 8002 --reload
```

API docs: `http://localhost:8002/docs`

## Architecture

```
ai-services/
├── agent/               # Core agent loop
│   ├── agent.py         # Main agent (Plan → Execute → Respond)
│   ├── planner.py       # Query decomposition
│   ├── executor.py      # Tool execution with retry
│   ├── context.py       # Result compilation
│   └── responder.py     # Response generation
├── tools/               # 28 specialized tools
│   ├── crime/           # Crime search, detail, list, stats
│   ├── graph/           # Graph traversal, shortest path
│   ├── identity/        # Indian name matching
│   ├── knowledge/       # Knowledge graph queries
│   ├── reasoning/       # Explainable reasoning chains
│   ├── prediction/      # Crime forecasting, risk scoring
│   ├── search/          # Intelligent search pipeline
│   ├── investigation/   # Investigation tools
│   ├── analytics/       # Analytics tools
│   ├── embeddings/      # Embedding search
│   ├── language/        # Translation
│   ├── rag/             # RAG search
│   ├── recommendations/ # Case recommendations
│   ├── patterns/        # Pattern detection
│   ├── similar/         # Similar cases
│   ├── report/          # Report generation
│   ├── workflows/       # Workflow runner
│   └── builtins/        # Calculator, web fetch
├── core/                # Provider abstraction
│   ├── provider.py      # Provider registry
│   ├── providers/       # Ollama, OpenAI, Gemini
│   ├── prompts.py       # Prompt management
│   └── tokens.py        # Token tracking
├── knowledge/           # Knowledge graph builder
├── memory/              # Multi-layer memory system
├── rag/                 # RAG pipeline
├── reasoning/           # Reasoning engine
├── prediction/          # Prediction engine
├── identity/            # Identity resolution
├── language/            # Language pipeline
├── search/              # Search intelligence
├── embeddings/          # Embedding services
├── workflows/           # Investigation workflows
├── evaluation/          # AI monitoring
├── models/              # Model registry
├── streaming/           # SSE streaming
├── storage/             # File storage
├── pattern/             # Pattern analysis
├── graph/               # Graph operations
└── tests/               # 23 test files
```

## AI Providers

| Provider | Default Model | Requires |
|----------|--------------|----------|
| **Ollama** (default) | llama3.2:1b | Local Ollama server |
| **OpenAI** | gpt-4o-mini | API key |
| **Gemini** | gemini-2.0-flash | API key |

## Tool Inventory (28 Tools)

| Category | Tools |
|----------|-------|
| **Crime** | crime_search, crime_detail, crime_list, crime_stats |
| **Graph** | graph_traverse, graph_shortest_path, graph_neighbors |
| **Analytics** | analytics_counts, analytics_trends |
| **Investigation** | investigation_notes, investigation_timeline, case_status, investigation_analyze |
| **Search** | rag_search, search_intelligent, similar_cases |
| **Identity** | identity_match |
| **Knowledge** | knowledge_graph |
| **Reasoning** | reasoning_analyze |
| **Prediction** | prediction_engine |
| **Language** | translator |
| **Embeddings** | embedding_search |
| **Workflows** | workflow_run |
| **Recommendations** | recommendation_engine |
| **Patterns** | pattern_detect |
| **Report** | report_generate |
| **Builtins** | calculator, web_fetch |

## Memory System

| Layer | Purpose | Lifetime |
|-------|---------|----------|
| Session Memory | Conversation history | Per session |
| Working Memory | Active investigation scratchpad | Per turn |
| Investigation Context | Loaded case data | Per investigation |
| User Preferences | Per-user settings | Persistent |

## Workflows

| Workflow | Purpose |
|----------|---------|
| `investigation` | Multi-step case analysis |
| `case_analysis` | Comprehensive case review |
| `suspect_profile` | Suspect profiling |
| `crime_briefing` | Crime briefing generation |

## Testing

```bash
python -m pytest tests/ -v
```
