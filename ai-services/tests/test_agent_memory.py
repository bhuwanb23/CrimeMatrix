import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from agent.agent import CoreAgent
from agent.message import ConversationContext


class MockProvider:
    def __init__(self, response="Test response"):
        self.response = response

    def get_name(self):
        return "mock"

    async def chat(self, messages, model=None):
        return self.response

    async def stream(self, messages, model=None):
        for word in self.response.split():
            yield word + " "

    async def health_check(self):
        return True

    def get_token_count(self, text):
        return len(text) // 4


@pytest.mark.asyncio
async def test_agent_chat_no_tools():
    with patch("agent.agent.provider_registry") as mock_registry:
        mock_registry.get.return_value = MockProvider("Hello, I can help with crimes.")
        agent = CoreAgent(provider="mock", model="test")
        result = await agent.chat("Hello", use_tools=False, session_id="test_no_tools")
        assert "response" in result
        assert "Hello" in result["response"]


@pytest.mark.asyncio
async def test_agent_chat_with_tools():
    with patch("agent.agent.provider_registry") as mock_registry:
        mock_registry.get.return_value = MockProvider("The answer is 42")
        agent = CoreAgent(provider="mock", model="test")
        result = await agent.chat("What is the answer?", use_tools=True, session_id="test_tools")
        assert "response" in result
        assert "reasoning_trace" in result


@pytest.mark.asyncio
async def test_agent_multi_turn():
    with patch("agent.agent.provider_registry") as mock_registry:
        mock_registry.get.return_value = MockProvider("Response")
        agent = CoreAgent(provider="mock", model="test")
        ctx = ConversationContext(session_id="multi")
        r1 = await agent.chat("First message", ctx, use_tools=False, session_id="multi")
        r2 = await agent.chat("Second message", ctx, use_tools=False, session_id="multi")
        assert len(ctx.messages) == 4


@pytest.mark.asyncio
async def test_agent_memory_persists():
    with patch("agent.agent.provider_registry") as mock_registry:
        mock_registry.get.return_value = MockProvider("Response")
        agent = CoreAgent(provider="mock", model="test")
        await agent.chat("Hello", use_tools=False, session_id="mem_persist_test_unique")
        session_mem = await agent.memory.get_session("mem_persist_test_unique")
        assert len(session_mem.messages) == 2
