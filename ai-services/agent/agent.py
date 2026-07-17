import json
import time
from typing import Optional, AsyncGenerator
from agent.message import Message, ConversationContext, Plan, PlanStep, ToolResult
from agent.planner import Planner
from agent.executor import Executor
from agent.context import ContextBuilder
from agent.responder import ResponseGenerator
from tools.registry import tool_registry
from core.provider import registry as provider_registry
from core.tokens import token_tracker
from core.prompts import prompt_manager
import structlog

logger = structlog.get_logger()


class CoreAgent:
    def __init__(self, agent_id: str = "default", name: str = "CrimeMatrix Agent",
                 system_prompt: str = None, provider: str = None, model: str = None):
        self.agent_id = agent_id
        self.name = name
        self.system_prompt = system_prompt or prompt_manager.get("system").template
        self.provider_name = provider
        self.model_name = model
        self.planner = Planner(provider, model)
        self.executor = Executor()
        self.context_builder = ContextBuilder()
        self.responder = ResponseGenerator(provider, model)

    async def chat(self, message: str, context: ConversationContext = None,
                   use_tools: bool = True) -> dict:
        if context is None:
            context = ConversationContext()

        context.add(Message.user(message))
        start_time = time.time()
        reasoning_trace = []

        if not use_tools:
            provider = provider_registry.get(self.provider_name)
            llm_messages = [{"role": "system", "content": self.system_prompt}]
            llm_messages.extend(context.get_messages_for_llm())
            start = time.time()
            response = await provider.chat(llm_messages, model=self.model_name)
            duration_ms = (time.time() - start) * 1000
            token_tracker.record(provider.get_name(), self.model_name or "default",
                                 provider.get_token_count(json.dumps(llm_messages)),
                                 provider.get_token_count(response), duration_ms)
            context.add(Message.assistant(response))
            return {"response": response, "reasoning_trace": [], "steps": 0}

        tools = tool_registry.list_all()
        available_tools = [t for t in tools]

        reasoning_trace.append({"type": "thinking", "content": f"Planning approach for: {message[:200]}"})

        plan = await self.planner.plan(message, available_tools)
        reasoning_trace.append({"type": "plan", "content": f"Created plan with {len(plan.steps)} steps", "plan": plan.to_dict()})

        results = []

        if plan.steps:
            for step in plan.steps:
                reasoning_trace.append({
                    "type": "step_start",
                    "content": f"Executing: {step.goal}",
                    "step": step.to_dict(),
                })

                step.status = "running"
                result = await self.executor.execute(step)
                step.status = "completed" if result.success else "failed"
                step.result = result.output if result.success else result.error
                results.append(result)

                reasoning_trace.append({
                    "type": "step_complete",
                    "content": f"Step {'✅' if result.success else '❌'}: {step.goal}",
                    "result": result.to_dict(),
                })

        compiled_context = self.context_builder.build(message, plan, results)
        reasoning_trace.append({"type": "thinking", "content": "Generating final response"})

        start = time.time()
        final_response = await self.responder.generate(message, compiled_context)
        duration_ms = (time.time() - start) * 1000
        provider = provider_registry.get(self.provider_name)
        token_tracker.record(provider.get_name(), self.model_name or "default",
                             provider.get_token_count(compiled_context),
                             provider.get_token_count(final_response), duration_ms)

        context.add(Message.assistant(final_response))
        context.add_trace(reasoning_trace)

        total_time = (time.time() - start_time) * 1000
        return {
            "response": final_response,
            "reasoning_trace": reasoning_trace,
            "steps": len(plan.steps),
            "total_time_ms": round(total_time, 2),
        }

    async def stream(self, message: str, context: ConversationContext = None) -> AsyncGenerator[dict, None]:
        if context is None:
            context = ConversationContext()

        context.add(Message.user(message))

        tools = tool_registry.list_all()
        plan = await self.planner.plan(message, tools)

        yield {"type": "plan", "content": f"Plan: {len(plan.steps)} steps", "plan": plan.to_dict()}

        results = []
        for step in plan.steps:
            yield {"type": "step_start", "content": f"Executing: {step.goal}"}
            result = await self.executor.execute(step)
            step.result = result.output if result.success else result.error
            results.append(result)
            yield {"type": "step_complete", "content": f"{'✅' if result.success else '❌'} {step.goal}", "result": result.to_dict()}

        compiled_context = self.context_builder.build(message, plan, results)

        yield {"type": "thinking", "content": "Generating response..."}

        provider = provider_registry.get(self.provider_name)
        system_prompt = self.system_prompt + "\n\n" + compiled_context
        llm_messages = [{"role": "system", "content": system_prompt}]

        full_response = []
        async for chunk in provider.stream(llm_messages, model=self.model_name):
            full_response.append(chunk)
            yield {"type": "message", "content": chunk}

        context.add(Message.assistant("".join(full_response)))
        yield {"type": "done", "content": ""}
