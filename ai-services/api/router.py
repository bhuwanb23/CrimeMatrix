from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from orchestrator.orchestrator import orchestrator
from tools.registry import tool_registry
from core.tokens import token_tracker
from core.prompts import prompt_manager
from core.provider import registry as provider_registry
from streaming.sse import sse_response
from agent.message import ConversationContext

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    agent_id: str = "default"
    session_id: str = "default"
    use_tools: bool = True


class ToolInvokeRequest(BaseModel):
    tool: str
    params: dict = {}


# Chat
@router.post("/chat")
async def chat(data: ChatRequest):
    try:
        response = await orchestrator.chat(data.message, data.agent_id, data.session_id)
        return {"success": True, "data": {"response": response, "agent": data.agent_id, "session": data.session_id}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(data: ChatRequest):
    async def generate():
        async for chunk in orchestrator.stream_chat(data.message, data.agent_id, data.session_id):
            yield {"event": "message", "data": chunk}
        yield {"event": "done", "data": ""}

    return sse_response(orchestrator.stream_chat(data.message, data.agent_id, data.session_id))


# Agents
@router.get("/agents")
async def list_agents():
    return {"success": True, "data": orchestrator.list_agents()}


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    agent = orchestrator.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "data": {"id": agent.agent_id, "name": agent.name, "provider": agent.provider_name, "model": agent.model_name}}


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


# Sessions
@router.get("/sessions")
async def list_sessions():
    return {"success": True, "data": orchestrator.list_sessions()}


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    cleared = orchestrator.clear_session(session_id)
    return {"success": True, "data": {"cleared": cleared}}


# Health
@router.get("/health")
async def health():
    health_status = {}
    for p_info in provider_registry.list_all():
        provider = provider_registry.get(p_info["name"])
        health_status[p_info["name"]] = await provider.health_check()
    return {"success": True, "data": {"providers": health_status}}


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


# Tokens
@router.get("/tokens")
async def token_usage():
    return {"success": True, "data": token_tracker.get_summary()}


# Prompts
@router.get("/prompts")
async def list_prompts():
    return {"success": True, "data": prompt_manager.list_all()}
