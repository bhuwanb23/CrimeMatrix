from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent.agent import CoreAgent
from agent.message import ConversationContext
from tools.registry import tool_registry
from core.tokens import token_tracker
from core.prompts import prompt_manager
from core.provider import registry as provider_registry
from streaming.sse import sse_response
from rag.pipeline import RAGPipeline
import structlog

logger = structlog.get_logger()

router = APIRouter()

# RAG pipeline
_rag = RAGPipeline()

# Shared instances
_default_agent = CoreAgent(agent_id="default", name="CrimeMatrix Copilot",
                           provider="ollama", model="llama3.2:1b")
_agents = {"default": _default_agent}
_sessions: dict[str, ConversationContext] = {}


class ChatRequest(BaseModel):
    message: str
    agent_id: str = "default"
    session_id: str = "default"
    user_id: str = "default"
    use_tools: bool = True


class ToolInvokeRequest(BaseModel):
    tool: str
    params: dict = {}


class PreferencesRequest(BaseModel):
    key: str
    value: str


class InvestigationRequest(BaseModel):
    investigation_id: int


# Chat
@router.post("/chat")
async def chat(data: ChatRequest):
    try:
        agent = _agents.get(data.agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{data.agent_id}' not found")

        if data.session_id not in _sessions:
            _sessions[data.session_id] = ConversationContext(session_id=data.session_id)
        context = _sessions[data.session_id]

        result = await agent.chat(data.message, context, data.use_tools,
                                  session_id=data.session_id, user_id=data.user_id)
        return {
            "success": True,
            "data": {
                "response": result["response"],
                "reasoning_trace": result["reasoning_trace"],
                "steps": result["steps"],
                "total_time_ms": result.get("total_time_ms", 0),
                "agent": data.agent_id,
                "session": data.session_id,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("chat_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(data: ChatRequest):
    agent = _agents.get(data.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{data.agent_id}' not found")

    if data.session_id not in _sessions:
        _sessions[data.session_id] = ConversationContext(session_id=data.session_id)
    context = _sessions[data.session_id]

    return sse_response(agent.stream(data.message, context,
                                     session_id=data.session_id, user_id=data.user_id))


# Agent management
@router.get("/agents")
async def list_agents():
    return {"success": True, "data": [
        {"id": a.agent_id, "name": a.name, "provider": a.provider_name, "model": a.model_name}
        for a in _agents.values()
    ]}


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    agent = _agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "data": {"id": agent.agent_id, "name": agent.name, "provider": agent.provider_name, "model": agent.model_name}}


# Session traces
@router.get("/sessions")
async def list_sessions():
    return {"success": True, "data": [
        {"session_id": s.session_id, "messages": len(s.messages), "traces": len(s.traces)}
        for s in _sessions.values()
    ]}


@router.get("/sessions/{session_id}/trace")
async def get_session_trace(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "data": session.get_full_trace()}


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    agent = _agents.get("default")
    if agent:
        agent.memory.clear_session(session_id)
    if session_id in _sessions:
        del _sessions[session_id]
        return {"success": True, "data": {"cleared": True}}
    return {"success": True, "data": {"cleared": False}}


# Memory
@router.get("/memory/sessions/{session_id}/history")
async def get_memory_history(session_id: str, limit: int = 50):
    agent = _agents.get("default")
    if not agent:
        raise HTTPException(status_code=404, detail="No agent")
    session_mem = agent.memory.get_session(session_id)
    messages = session_mem.get_messages()[-limit:]
    return {"success": True, "data": {"messages": messages, "total": len(session_mem.messages), "summary": session_mem.summary}}


@router.get("/memory/sessions/{session_id}/summary")
async def get_memory_summary(session_id: str):
    agent = _agents.get("default")
    if not agent:
        raise HTTPException(status_code=404, detail="No agent")
    session_mem = agent.memory.get_session(session_id)
    return {"success": True, "data": {"summary": session_mem.summary, "message_count": len(session_mem.messages)}}


@router.post("/memory/investigation")
async def load_investigation(data: InvestigationRequest):
    agent = _agents.get("default")
    if not agent:
        raise HTTPException(status_code=404, detail="No agent")
    inv = await agent.memory.investigation.load_investigation(data.investigation_id)
    if not inv:
        return {"success": False, "message": "Could not load investigation"}
    formatted = agent.memory.investigation.format_for_context(inv, "crime")
    return {"success": True, "data": {"raw": inv, "formatted": formatted}}


@router.get("/memory/preferences/{user_id}")
async def get_preferences(user_id: str):
    agent = _agents.get("default")
    if not agent:
        raise HTTPException(status_code=404, detail="No agent")
    return {"success": True, "data": agent.memory.preferences.get(user_id)}


@router.put("/memory/preferences/{user_id}")
async def set_preference(user_id: str, data: PreferencesRequest):
    agent = _agents.get("default")
    if not agent:
        raise HTTPException(status_code=404, detail="No agent")
    agent.memory.preferences.set(user_id, data.key, data.value)
    return {"success": True, "data": agent.memory.preferences.get(user_id)}


@router.get("/memory/working")
async def get_working_memory():
    agent = _agents.get("default")
    if not agent:
        raise HTTPException(status_code=404, detail="No agent")
    return {"success": True, "data": agent.memory.working.get_all()}


# Tools
@router.get("/tools")
async def list_tools():
    return {"success": True, "data": tool_registry.list_all()}


@router.get("/tools/{tool_name}")
async def get_tool(tool_name: str):
    tool = tool_registry.get(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"success": True, "data": tool.to_schema()}


@router.post("/tools/invoke")
async def invoke_tool(data: ToolInvokeRequest):
    try:
        result = await tool_registry.invoke(data.tool, **data.params)
        return {"success": True, "data": {"tool": data.tool, "result": result}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Health & Config
@router.get("/health")
async def health():
    health_status = {}
    for p_info in provider_registry.list_all():
        provider = provider_registry.get(p_info["name"])
        health_status[p_info["name"]] = await provider.health_check()
    return {"success": True, "data": {"providers": health_status, "agents": len(_agents), "tools": len(tool_registry.list_all())}}


@router.get("/models")
async def list_models():
    all_models = []
    for p_info in provider_registry.list_all():
        provider = provider_registry.get(p_info["name"])
        models = await provider.list_models()
        for m in models:
            m["provider"] = p_info["name"]
        all_models.extend(models)
    return {"success": True, "data": all_models}


@router.get("/tokens")
async def token_usage():
    return {"success": True, "data": token_tracker.get_summary()}


@router.get("/prompts")
async def list_prompts():
    return {"success": True, "data": prompt_manager.list_all()}


# RAG
class RAGSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    doc_type: Optional[str] = None
    session_id: str = "default"


@router.post("/rag/index")
async def rag_index(limit: int = 50):
    count = await _rag.index(limit)
    return {"success": True, "data": {"chunks_indexed": count, "indexed": _rag.is_indexed()}}


@router.post("/rag/search")
async def rag_search(data: RAGSearchRequest):
    result = _rag.search_and_cite(data.query, data.session_id, data.top_k)
    return {"success": True, "data": result}


@router.get("/rag/stats")
async def rag_stats():
    return {"success": True, "data": _rag.get_stats()}


@router.get("/rag/citations/{session_id}")
async def rag_citations(session_id: str):
    citations = _rag.citations.get_citations(session_id)
    return {"success": True, "data": citations}


# Search Intelligence
from search.engine import SearchEngine

_search_engine = SearchEngine(provider="ollama", model="llama3.2:1b")


class IntelligentSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    doc_type: Optional[str] = None
    use_rewrite: bool = True
    use_expand: bool = True
    use_rerank: bool = True


class SimilarCaseRequest(BaseModel):
    case_id: int
    top_k: int = 5


class CrossDistrictRequest(BaseModel):
    query: str
    districts: Optional[list] = None
    top_k: int = 10


class QueryExpandRequest(BaseModel):
    query: str


class QueryRewriteRequest(BaseModel):
    query: str


class RerankRequest(BaseModel):
    query: str
    results: list


@router.post("/search/intelligent")
async def intelligent_search(data: IntelligentSearchRequest):
    result = await _search_engine.intelligent_search(
        data.query, data.top_k, data.doc_type,
        data.use_rewrite, data.use_expand, data.use_rerank,
    )
    return {"success": True, "data": result}


@router.post("/search/similar")
async def similar_cases(data: SimilarCaseRequest):
    result = await _search_engine.find_similar(data.case_id, data.top_k)
    return {"success": True, "data": result}


@router.post("/search/cross-district")
async def cross_district(data: CrossDistrictRequest):
    result = await _search_engine.cross_district_search(data.query, data.districts, data.top_k)
    return {"success": True, "data": result}


@router.post("/search/expand")
async def expand_query(data: QueryExpandRequest):
    result = await _search_engine.expand_query(data.query)
    return {"success": True, "data": result}


@router.post("/search/rewrite")
async def rewrite_query(data: QueryRewriteRequest):
    result = await _search_engine.rewrite_query(data.query)
    return {"success": True, "data": result}


@router.post("/search/rerank")
async def rerank_results(data: RerankRequest):
    result = await _search_engine.rerank_results(data.query, data.results)
    return {"success": True, "data": result}


@router.get("/search/stats")
async def search_stats():
    return {"success": True, "data": _search_engine.get_stats()}
