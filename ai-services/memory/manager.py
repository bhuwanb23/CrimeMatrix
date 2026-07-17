from memory.session import SessionMemory
from memory.compressor import ContextCompressor
from memory.working import WorkingMemory
from memory.preferences import UserPreferences
from memory.investigation import InvestigationContext
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()


class MemoryManager:
    def __init__(self, provider: str = None, model: str = None):
        self.sessions: Dict[str, SessionMemory] = {}
        self.compressor = ContextCompressor(provider, model)
        self.preferences = UserPreferences()
        self.investigation = InvestigationContext()
        self.working = WorkingMemory()

    def get_session(self, session_id: str) -> SessionMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionMemory(session_id)
        return self.sessions[session_id]

    async def before_turn(self, query: str, session_id: str = "default",
                          user_id: str = "default") -> dict:
        session = self.get_session(session_id)
        prefs = self.preferences.get(user_id)
        context_parts = []

        if session.summary:
            context_parts.append(f"Previous conversation summary:\n{session.summary}")

        recent = session.get_unsummarized_messages()
        if recent:
            history = "\n".join([f"{m['role']}: {m['content'][:200]}" for m in recent[-10:]])
            context_parts.append(f"Recent conversation:\n{history}")

        working_ctx = self.working.format_for_context()
        if working_ctx:
            context_parts.append(working_ctx)

        prefs_prompt = self.preferences.format_for_system_prompt(user_id)
        if prefs_prompt:
            context_parts.append(prefs_prompt)

        return {
            "conversation_context": "\n\n".join(context_parts),
            "preferences": prefs,
            "session": session.to_dict(),
        }

    async def after_turn(self, query: str, response: str, session_id: str = "default"):
        session = self.get_session(session_id)
        session.add_message("user", query)
        session.add_message("assistant", response)

        if session.needs_compression():
            logger.info("auto_compressing", session=session_id, messages=len(session.messages))
            all_msgs = session.get_messages()
            summary, kept = await self.compressor.compress(all_msgs)
            session.clear()
            session.set_summary(summary, 0)
            for m in kept:
                session.add_message(m["role"], m["content"])

    def clear_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def list_sessions(self) -> List[dict]:
        return [s.to_dict() for s in self.sessions.values()]
