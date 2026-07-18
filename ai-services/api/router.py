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
    investigation_context: Optional[str] = None
    language: str = "en"


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
                                  session_id=data.session_id, user_id=data.user_id,
                                  investigation_context=data.investigation_context)
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


# Identity Intelligence
from identity.name_matcher import IndianNameMatcher
from identity.transliteration import TransliterationEngine
from identity.duplicate_detector import DuplicateDetector
from identity.entity_resolver import EntityResolver
from identity.record_merger import RecordMerger
from identity.alias_detector import AliasDetector

_name_matcher = IndianNameMatcher()
_transliterator = TransliterationEngine()
_duplicate_detector = DuplicateDetector()
_entity_resolver = EntityResolver()
_record_merger = RecordMerger()
_alias_detector = AliasDetector()


class NameMatchRequest(BaseModel):
    name1: str
    name2: str


class TransliterateRequest(BaseModel):
    text: str
    target: str = "english"


class DuplicateRequest(BaseModel):
    records: list
    id_key: str = "id"


class ResolveRequest(BaseModel):
    mention: str
    candidates: list


class MergeRequest(BaseModel):
    primary: dict
    secondary: dict
    entity_type: str = "person"


class AliasRequest(BaseModel):
    name: str
    known_aliases: Optional[list] = None
    all_names: Optional[list] = None


@router.post("/identity/match")
async def match_names(data: NameMatchRequest):
    result = _name_matcher.match(data.name1, data.name2)
    return {"success": True, "data": result}


@router.post("/identity/match/batch")
async def batch_match_names(data: NameMatchRequest):
    results = _name_matcher.batch_match(data.name1, data.name2 if isinstance(data.name2, list) else [data.name2])
    return {"success": True, "data": results}


@router.post("/identity/transliterate")
async def transliterate(data: TransliterateRequest):
    result = _transliterator.transliterate(data.text, data.target)
    return {"success": True, "data": result}


@router.post("/identity/duplicates")
async def find_duplicates(data: DuplicateRequest):
    results = _duplicate_detector.find_duplicates(data.records, data.id_key)
    return {"success": True, "data": {"duplicates": results, "count": len(results)}}


@router.post("/identity/resolve")
async def resolve_entity(data: ResolveRequest):
    results = _entity_resolver.resolve_from_text(data.mention, data.candidates)
    return {"success": True, "data": results}


@router.post("/identity/merge")
async def merge_records(data: MergeRequest):
    merged = _record_merger.merge(data.primary, data.secondary, data.entity_type)
    return {"success": True, "data": merged}


@router.post("/identity/aliases")
async def detect_aliases(data: AliasRequest):
    aliases = _alias_detector.detect_aliases(data.name, data.known_aliases, data.all_names)
    return {"success": True, "data": aliases}


@router.get("/identity/stats")
async def identity_stats():
    return {"success": True, "data": {
        "merge_log_count": len(_record_merger.get_merge_log()),
        "supported_scripts": ["kannada", "devanagari", "latin"],
        "nickname_groups": len(NICKNAMES) if "NICKNAMES" in dir() else 0,
    }}


# Knowledge Graph Intelligence
import networkx as nx
from knowledge.graph_builder import GraphBuilder
from knowledge.query_engine import GraphQueryEngine
from knowledge.criminal_network import CriminalNetwork
from knowledge.relationship import RelationshipDiscovery
from knowledge.timeline_gen import TimelineGenerator
from knowledge.link_analysis import LinkAnalysis

_knowledge_graph = nx.Graph()
_graph_builder = GraphBuilder()
_query_engine = GraphQueryEngine(_knowledge_graph)
_criminal_network = CriminalNetwork(_knowledge_graph)
_relationship = RelationshipDiscovery(_knowledge_graph)
_timeline = TimelineGenerator(_knowledge_graph)
_link_analysis = LinkAnalysis(_knowledge_graph)


class KnowledgeQueryRequest(BaseModel):
    query_type: str
    node_id: Optional[str] = None
    node_id_2: Optional[str] = None
    depth: int = 2


@router.post("/knowledge/build")
async def knowledge_build():
    stats = await _graph_builder.build()
    _knowledge_graph.clear()
    _knowledge_graph.update(_graph_builder.graph)
    return {"success": True, "data": stats}


@router.post("/knowledge/query")
async def knowledge_query(data: KnowledgeQueryRequest):
    if data.query_type == "crimes_linked" and data.node_id:
        result = _query_engine.crimes_linked_to(data.node_id)
    elif data.query_type == "suspects_in_crime" and data.node_id:
        result = _query_engine.suspects_in_crime(data.node_id)
    elif data.query_type == "common_crimes" and data.node_id and data.node_id_2:
        result = _query_engine.common_crimes(data.node_id, data.node_id_2)
    elif data.query_type == "paths" and data.node_id and data.node_id_2:
        result = _query_engine.find_paths(data.node_id, data.node_id_2)
    elif data.query_type == "search" and data.node_id:
        result = _query_engine.search_nodes(data.node_id)
    else:
        result = {"error": "Invalid query type or missing parameters"}
    return {"success": True, "data": result}


@router.post("/knowledge/network")
async def knowledge_network(data: KnowledgeQueryRequest):
    if data.query_type == "clusters":
        result = _criminal_network.find_clusters()
    elif data.query_type == "risk" and data.node_id:
        result = _criminal_network.network_risk_score(data.node_id)
    elif data.query_type == "accomplices" and data.node_id:
        result = _criminal_network.accomplice_network(data.node_id, data.depth)
    else:
        result = {"error": "Invalid network query"}
    return {"success": True, "data": result}


@router.post("/knowledge/discover")
async def knowledge_discover(data: KnowledgeQueryRequest):
    if data.query_type == "hidden" and data.node_id and data.node_id_2:
        result = _relationship.find_hidden_connections(data.node_id, data.node_id_2)
    elif data.query_type == "shared" and data.node_id and data.node_id_2:
        result = _relationship.shared_connections(data.node_id, data.node_id_2)
    elif data.query_type == "strength" and data.node_id and data.node_id_2:
        result = _relationship.relationship_strength(data.node_id, data.node_id_2)
    elif data.query_type == "importance" and data.node_id:
        result = _relationship.node_importance(data.node_id)
    else:
        result = {"error": "Invalid discover query"}
    return {"success": True, "data": result}


@router.post("/knowledge/timeline")
async def knowledge_timeline(data: KnowledgeQueryRequest):
    if data.node_id:
        result = _timeline.entity_timeline(data.node_id)
    elif data.query_type == "bursts":
        result = _timeline.activity_bursts()
    else:
        result = _timeline.generate()
    return {"success": True, "data": result}


@router.post("/knowledge/analyze")
async def knowledge_analyze(data: KnowledgeQueryRequest):
    if data.query_type == "shortest" and data.node_id and data.node_id_2:
        result = _link_analysis.shortest_path(data.node_id, data.node_id_2)
    elif data.query_type == "centrality":
        result = _link_analysis.centrality()
    elif data.query_type == "communities":
        result = _link_analysis.communities()
    elif data.query_type == "bridges":
        result = _link_analysis.bridges()
    else:
        result = {"error": "Invalid analyze query"}
    return {"success": True, "data": result}


@router.get("/knowledge/stats")
async def knowledge_stats():
    return {"success": True, "data": {
        "nodes": _knowledge_graph.number_of_nodes(),
        "edges": _knowledge_graph.number_of_edges(),
        "components": nx.number_connected_components(_knowledge_graph) if _knowledge_graph.number_of_nodes() > 0 else 0,
    }}


# AI Reasoning Engine
from reasoning.engine import ReasoningEngine
from reasoning.evidence import EvidenceRanking
from reasoning.confidence import ConfidenceCalculator

_reasoning_engine = ReasoningEngine(provider="ollama", model="llama3.2:1b")
_evidence_ranker = EvidenceRanking()
_confidence_calc = ConfidenceCalculator()


class ReasoningAnalyzeRequest(BaseModel):
    hypothesis: str
    evidence: list
    chain_type: str = "abductive"


class ReasoningChainRequest(BaseModel):
    hypothesis: str
    evidence: list
    chain_type: str = "abductive"


class ReasoningConfidenceRequest(BaseModel):
    chain: dict


class ReasoningEvidenceRequest(BaseModel):
    evidence: list
    hypothesis: Optional[str] = None


class ReasoningExplainRequest(BaseModel):
    hypothesis: str
    evidence: list
    chain_type: str = "abductive"


@router.post("/reasoning/analyze")
async def reasoning_analyze(data: ReasoningAnalyzeRequest):
    result = await _reasoning_engine.analyze(data.hypothesis, data.evidence, data.chain_type)
    return {"success": True, "data": result}


@router.post("/reasoning/chain")
async def reasoning_chain(data: ReasoningChainRequest):
    from reasoning.chain import ReasoningChainGenerator
    gen = ReasoningChainGenerator()
    chain = gen.build(data.hypothesis, data.evidence, data.chain_type)
    return {"success": True, "data": chain}


@router.post("/reasoning/confidence")
async def reasoning_confidence(data: ReasoningConfidenceRequest):
    result = _confidence_calc.compute(data.chain)
    return {"success": True, "data": result}


@router.post("/reasoning/evidence")
async def reasoning_evidence(data: ReasoningEvidenceRequest):
    ranked = _evidence_ranker.rank(data.evidence, data.hypothesis)
    return {"success": True, "data": ranked}


@router.post("/reasoning/explain")
async def reasoning_explain(data: ReasoningExplainRequest):
    result = await _reasoning_engine.analyze(data.hypothesis, data.evidence, data.chain_type)
    return {"success": True, "data": {"explanation": result["explanation"], "confidence": result["confidence"]}}


# Prediction Engine
from prediction.engine import PredictionEngine

_prediction_engine = PredictionEngine()


class PredictionRequest(BaseModel):
    prediction_type: str
    data: dict


@router.post("/predict/forecast")
async def predict_forecast(data: dict):
    result = _prediction_engine.forecast.forecast(data.get("historical", []), data.get("periods_ahead", 1))
    return {"success": True, "data": result}


@router.post("/predict/hotspots")
async def predict_hotspots(data: dict):
    result = _prediction_engine.hotspot.identify_hotspots(data.get("crimes", []), data.get("top_n", 5))
    return {"success": True, "data": result}


@router.post("/predict/recidivism")
async def predict_recidivism(data: dict):
    result = _prediction_engine.repeat_offender.predict(data.get("profile", {}))
    return {"success": True, "data": result}


@router.post("/predict/risk")
async def predict_risk(data: dict):
    result = _prediction_engine.risk.score(data.get("profile", {}))
    return {"success": True, "data": result}


@router.post("/predict/mo-similarity")
async def predict_mo_similarity(data: dict):
    result = _prediction_engine.mo.compare(data.get("mo1", ""), data.get("mo2", ""))
    return {"success": True, "data": result}


@router.post("/predict/cases")
async def predict_cases(data: dict):
    result = _prediction_engine.recommender.recommend(data.get("case", {}), data.get("all_cases", []))
    return {"success": True, "data": result}


@router.get("/predict/stats")
async def predict_stats():
    return {"success": True, "data": _prediction_engine.get_stats()}


# Speech & Translation
from language.stt import SpeechToText
from language.tts import TextToSpeech
from language.translator import Translator
from language.kanglish import KanglishNormalizer
from language.normalizer import QueryNormalizer

_stt = SpeechToText()
_tts = TextToSpeech()
_translator = Translator()
_kanglish = KanglishNormalizer()
_normalizer = QueryNormalizer()


class STTRequest(BaseModel):
    audio_text: Optional[str] = None
    language: str = "auto"


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    gender: str = "female"


class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"


class KanglishRequest(BaseModel):
    text: str
    target: str = "english"


class NormalizeRequest(BaseModel):
    query: str


@router.post("/language/stt")
async def speech_to_text(data: STTRequest):
    result = await _stt.transcribe(audio_text=data.audio_text, language=data.language)
    return {"success": True, "data": result}


@router.post("/language/tts")
async def text_to_speech(data: TTSRequest):
    result = await _tts.synthesize(data.text, language=data.language, gender=data.gender)
    return {"success": True, "data": result}


@router.post("/language/translate")
async def translate(data: TranslateRequest):
    result = _translator.translate(data.text, data.source_lang, data.target_lang)
    return {"success": True, "data": result}


@router.post("/language/kanglish")
async def kanglish_normalize(data: KanglishRequest):
    result = _kanglish.normalize(data.text, data.target)
    return {"success": True, "data": result}


@router.post("/language/normalize")
async def normalize_query(data: NormalizeRequest):
    result = _normalizer.normalize(data.query)
    return {"success": True, "data": result}


@router.get("/language/stats")
async def language_stats():
    return {"success": True, "data": {
        "supported_languages": ["en", "kn", "hi"],
        "kanglish_entries": len(KANGlish_KN),
        "en_kn_dict_size": len(EN_KN_DICT) if "EN_KN_DICT" in dir() else 0,
    }}


# Embedding Services
from embeddings.service import EmbeddingService

_embedding_service = EmbeddingService()


class EmbedRequest(BaseModel):
    text: str
    domain: str = "fir"
    item_id: Optional[str] = None


class BatchEmbedRequest(BaseModel):
    texts: list
    domain: str = "fir"


class SimilarityRequest(BaseModel):
    embedding1: list
    embedding2: list


class EmbedSearchRequest(BaseModel):
    query: str
    domain: str = "fir"
    top_k: int = 5


@router.post("/embeddings/embed")
async def embed_text(data: EmbedRequest):
    vec = await _embedding_service.embed(data.text, data.domain, data.item_id)
    return {"success": True, "data": {"embedding": vec, "dimension": len(vec), "domain": data.domain}}


@router.post("/embeddings/batch")
async def embed_batch(data: BatchEmbedRequest):
    vecs = await _embedding_service.embed_batch(data.texts, data.domain)
    return {"success": True, "data": {"embeddings": vecs, "count": len(vecs), "domain": data.domain}}


@router.post("/embeddings/similarity")
async def embedding_similarity(data: SimilarityRequest):
    score = _embedding_service.similarity(data.embedding1, data.embedding2)
    return {"success": True, "data": {"similarity": score}}


@router.post("/embeddings/search")
async def embedding_search(data: EmbedSearchRequest):
    results = await _embedding_service.search(data.query, data.domain, data.top_k)
    return {"success": True, "data": results}


@router.get("/embeddings/stats")
async def embedding_stats():
    return {"success": True, "data": _embedding_service.get_stats()}


# AI Workflow Engine
from workflows.engine import WorkflowEngine
from workflows.registry import workflow_registry

_workflow_engine = WorkflowEngine()


class WorkflowRunRequest(BaseModel):
    workflow: str
    inputs: Optional[dict] = None


@router.post("/workflows/run")
async def run_workflow(data: WorkflowRunRequest):
    result = await _workflow_engine.run(data.workflow, data.inputs)
    return {"success": True, "data": result}


@router.get("/workflows")
async def list_workflows():
    return {"success": True, "data": _workflow_engine.list_workflows()}


@router.get("/workflows/{name}")
async def get_workflow(name: str):
    wf = _workflow_engine.get_workflow(name)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"success": True, "data": wf}


@router.get("/workflows/{name}/steps")
async def get_workflow_steps(name: str):
    wf = workflow_registry.get(name)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    steps = [{"name": s["name"], "description": s.get("description", "")} for s in wf.get("steps", [])]
    return {"success": True, "data": steps}


# Model Management
from models.registry import model_registry, MODEL_TYPES
from models.conversation import ConversationModel
from models.embedding import EmbeddingModel
from models.speech import SpeechModel
from models.translation import TranslationModel
from models.prediction import PredictionModel

_conversation_model = ConversationModel()
_embedding_model = EmbeddingModel()
_speech_model = SpeechModel()
_translation_model = TranslationModel()
_prediction_model = PredictionModel()


class ModelRegisterRequest(BaseModel):
    name: str
    model_type: str
    provider: str
    model_name: Optional[str] = None
    default: bool = False


@router.get("/models/registry")
async def list_model_registry():
    return {"success": True, "data": model_registry.list_all()}


@router.get("/models/registry/{model_type}")
async def list_models_by_type(model_type: str):
    models = model_registry.list_type(model_type)
    return {"success": True, "data": models}


@router.post("/models/registry")
async def register_model(data: ModelRegisterRequest):
    model_registry.register(data.name, data.model_type, data.provider, data.model_name, default=data.default)
    return {"success": True, "data": {"registered": data.name, "type": data.model_type}}


@router.get("/models/config")
async def model_config():
    return {"success": True, "data": {
        "conversation": _conversation_model.get_config(),
        "embedding": _embedding_model.get_config(),
        "speech": _speech_model.get_config(),
        "translation": _translation_model.get_config(),
        "prediction": _prediction_model.get_config(),
        "defaults": model_registry.get_defaults(),
    }}


# AI Evaluation & Monitoring
from evaluation.dashboard import MonitoringDashboard

_dashboard = MonitoringDashboard()


class FeedbackRequest(BaseModel):
    rating: int
    query: str
    response: str = ""
    session_id: str = "default"
    comment: Optional[str] = None
    tags: Optional[list] = None


@router.get("/monitor/latency")
async def monitor_latency(endpoint: str = None):
    return {"success": True, "data": _dashboard.latency.get_stats(endpoint)}


@router.get("/monitor/tokens")
async def monitor_tokens(provider: str = None):
    if provider:
        return {"success": True, "data": _dashboard.tokens.get_stats(provider)}
    return {"success": True, "data": {"overall": _dashboard.tokens.get_stats(), "by_provider": _dashboard.tokens.get_by_provider()}}


@router.get("/monitor/hallucination")
async def monitor_hallucination():
    return {"success": True, "data": _dashboard.hallucination.get_stats()}


@router.get("/monitor/tools")
async def monitor_tools(tool: str = None):
    if tool:
        return {"success": True, "data": _dashboard.tool_success.get_stats(tool)}
    return {"success": True, "data": {"overall": _dashboard.tool_success.get_stats(), "by_tool": _dashboard.tool_success.get_by_tool()}}


@router.get("/monitor/accuracy")
async def monitor_accuracy(domain: str = None):
    return {"success": True, "data": _dashboard.accuracy.get_stats(domain)}


@router.get("/monitor/confidence")
async def monitor_confidence():
    return {"success": True, "data": {"stats": _dashboard.confidence.get_stats(), "distribution": _dashboard.confidence.get_distribution()}}


@router.get("/monitor/cost")
async def monitor_cost():
    return {"success": True, "data": {"overall": _dashboard.cost.get_stats(), "by_provider": _dashboard.cost.get_by_provider()}}


@router.post("/monitor/feedback")
async def submit_feedback(data: FeedbackRequest):
    _dashboard.feedback.submit(data.rating, data.query, data.response, data.session_id, data.comment, data.tags)
    return {"success": True, "data": _dashboard.feedback.get_stats()}


@router.get("/monitor/feedback")
async def get_feedback():
    return {"success": True, "data": {"stats": _dashboard.feedback.get_stats(), "recent": _dashboard.feedback.get_recent(10)}}


@router.get("/monitor/dashboard")
async def monitor_dashboard():
    return {"success": True, "data": _dashboard.get_full_dashboard()}


@router.get("/monitor/summary")
async def monitor_summary():
    return {"success": True, "data": _dashboard.get_summary()}
