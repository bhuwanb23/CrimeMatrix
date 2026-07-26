from typing import Dict, Optional
from agent.agent import CoreAgent
from agent.message import ConversationContext
from config import get_config
import structlog

logger = structlog.get_logger()


class Orchestrator:
    def __init__(self):
        self._agents: Dict[str, CoreAgent] = {}
        self._sessions: Dict[str, ConversationContext] = {}
        cfg = get_config()

        default_agent = CoreAgent(
            agent_id="default",
            name="CrimeMatrix Copilot",
            provider=cfg.default_provider,
            model=cfg.default_model,
        )
        self._agents["default"] = default_agent

    def get_agent(self, agent_id: str = "default") -> Optional[CoreAgent]:
        return self._agents.get(agent_id)

    def create_agent(self, agent_id: str, name: str, provider: str = None,
                     model: str = None, system_prompt: str = None) -> CoreAgent:
        cfg = get_config()
        agent = CoreAgent(
            agent_id,
            name,
            system_prompt,
            provider or cfg.default_provider,
            model or cfg.default_model,
        )
        self._agents[agent_id] = agent
        return agent

    def get_session(self, session_id: str) -> ConversationContext:
        if session_id not in self._sessions:
            self._sessions[session_id] = ConversationContext(session_id=session_id)
        return self._sessions[session_id]

    def clear_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def list_agents(self) -> list:
        return [
            {"id": a.agent_id, "name": a.name, "provider": a.provider_name, "model": a.model_name}
            for a in self._agents.values()
        ]

    def list_sessions(self) -> list:
        return [
            {"session_id": s.session_id, "messages": len(s.messages)}
            for s in self._sessions.values()
        ]

    async def chat(self, message: str, agent_id: str = "default",
                   session_id: str = None) -> str:
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found")

        context = self.get_session(session_id or "default")
        return await agent.chat(message, context)

    async def stream_chat(self, message: str, agent_id: str = "default",
                          session_id: str = None):
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found")

        context = self.get_session(session_id or "default")
        async for chunk in agent.stream(message, context):
            yield chunk


orchestrator = Orchestrator()
