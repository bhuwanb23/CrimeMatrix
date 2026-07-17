import json
import time
from typing import Optional
from agent.message import Message, ConversationContext
from tools.registry import tool_registry
from core.provider import registry as provider_registry
from core.tokens import token_tracker
from core.prompts import prompt_manager
import structlog

logger = structlog.get_logger()


class AIAgent:
    def __init__(self, agent_id: str = "default", name: str = "CrimeMatrix Agent",
                 system_prompt: str = None, provider: str = None, model: str = None):
        self.agent_id = agent_id
        self.name = name
        self.system_prompt = system_prompt or prompt_manager.get("system").template
        self.provider_name = provider
        self.model_name = model

    async def chat(self, message: str, context: ConversationContext = None,
                   use_tools: bool = True) -> str:
        if context is None:
            context = ConversationContext()

        context.add(Message.user(message))

        llm_messages = [{"role": "system", "content": self.system_prompt}]
        llm_messages.extend(context.get_messages_for_llm())

        provider = provider_registry.get(self.provider_name)

        if use_tools:
            tools = tool_registry.list_all()
            if tools:
                tool_desc = "\n".join([
                    f"- {t['name']}: {t['description']}" for t in tools
                ])
                llm_messages[0]["content"] += f"\n\nYou have these tools available:\n{tool_desc}\n\nTo use a tool, respond with: [TOOL:tool_name:param_name=param_value,...]"

        start = time.time()
        try:
            response = await provider.chat(llm_messages, model=self.model_name)
            duration_ms = (time.time() - start) * 1000

            token_tracker.record(
                provider=provider.get_name(),
                model=self.model_name or provider.get_name(),
                prompt_tokens=provider.get_token_count(json.dumps(llm_messages)),
                completion_tokens=provider.get_token_count(response),
                duration_ms=duration_ms,
            )

            if use_tools and response.startswith("[TOOL:"):
                tool_result = await self._handle_tool_call(response)
                if tool_result:
                    context.add(Message.assistant(f"I'll use the {tool_result['tool']} tool."))
                    context.add(Message.tool(tool_result["result"], tool_result["tool"]))

                    follow_messages = [{"role": "system", "content": self.system_prompt}]
                    follow_messages.extend(context.get_messages_for_llm())
                    follow_messages.append({
                        "role": "user",
                        "content": f"Tool '{tool_result['tool']}' returned: {tool_result['result']}\n\nNow answer the original question."
                    })
                    final_response = await provider.chat(follow_messages, model=self.model_name)
                    context.add(Message.assistant(final_response))
                    return final_response

            context.add(Message.assistant(response))
            return response

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            token_tracker.record(
                provider=provider.get_name(),
                model=self.model_name or "unknown",
                prompt_tokens=0, completion_tokens=0,
                duration_ms=duration_ms, status="error",
            )
            raise

    async def stream(self, message: str, context: ConversationContext = None):
        if context is None:
            context = ConversationContext()

        context.add(Message.user(message))

        llm_messages = [{"role": "system", "content": self.system_prompt}]
        llm_messages.extend(context.get_messages_for_llm())

        provider = provider_registry.get(self.provider_name)
        full_response = []

        async for chunk in provider.stream(llm_messages, model=self.model_name):
            full_response.append(chunk)
            yield chunk

        context.add(Message.assistant("".join(full_response)))

    async def _handle_tool_call(self, response: str) -> Optional[dict]:
        try:
            prefix = "[TOOL:"
            suffix = "]"
            tool_str = response[len(prefix):-len(suffix)]
            parts = tool_str.split(":")
            tool_name = parts[0]
            kwargs = {}
            if len(parts) > 1:
                for param in parts[1].split(","):
                    if "=" in param:
                        k, v = param.split("=", 1)
                        kwargs[k] = v
            result = await tool_registry.invoke(tool_name, **kwargs)
            return {"tool": tool_name, "result": result}
        except Exception as e:
            logger.error("tool_call_error", error=str(e))
            return None
