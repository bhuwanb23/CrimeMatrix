import asyncio
from app.db.session import init_db
from app.monitoring.persistence import MonitoringPersistence


async def test():
    await init_db()
    from app.db.session import async_session

    print("=== Phase 8: AI Monitoring Database E2E Test ===")
    print()

    async with async_session() as db:
        mon = MonitoringPersistence(db)

        # Test 1: Model Usage
        print("--- Test 1: Model Usage ---")
        await mon.record_model_usage("ollama", "llama3.2:1b", 150, 50, 1200.0)
        await mon.record_model_usage("openai", "gpt-4o", 200, 100, 800.0)
        usage = await mon.get_model_usage()
        print("  Recorded: %d model calls" % len(usage))
        summary = await mon.get_model_usage_summary()
        print("  Summary: %d calls, %d tokens, avg %.1fms" % (summary["total_calls"], summary["total_tokens"], summary["avg_duration_ms"]))

        # Test 2: Latency
        print("--- Test 2: Latency ---")
        await mon.record_latency("/api/ai/chat", 1500.0, "ollama")
        await mon.record_latency("/api/ai/chat", 800.0, "ollama")
        await mon.record_latency("/api/ai/tools/invoke", 200.0)
        latency = await mon.get_latency(endpoint="/api/ai/chat")
        print("  Recorded: %d latency records" % len(latency))
        stats = await mon.get_latency_stats("/api/ai/chat")
        print("  Stats: count=%d, avg=%.1fms, p50=%sms" % (stats["count"], stats["avg_ms"], stats["p50"]))

        # Test 3: Token Usage
        print("--- Test 3: Token Usage ---")
        await mon.record_tokens("ollama", "llama3.2:1b", 100, 50)
        await mon.record_tokens("openai", "gpt-4o", 500, 200)
        token_records = await mon.get_token_usage()
        print("  Recorded: %d token records" % len(token_records))
        token_summary = await mon.get_token_summary()
        print("  Total tokens: %d" % token_summary["total_tokens"])

        # Test 4: Tool Calls
        print("--- Test 4: Tool Calls ---")
        await mon.record_tool_call("calculator", True, 50.0)
        await mon.record_tool_call("calculator", True, 30.0)
        await mon.record_tool_call("crime_search", False, 500.0, error="timeout")
        tool_records = await mon.get_tool_calls()
        print("  Recorded: %d tool calls" % len(tool_records))
        tool_stats = await mon.get_tool_call_stats()
        print("  Stats: total=%d, success_rate=%.1f%%" % (tool_stats["total"], tool_stats["success_rate"]))

        # Cleanup
        from sqlalchemy import delete
        from app.monitoring.models import ModelUsage, LatencyRecord, TokenUsageRecord, ToolCall
        await db.execute(delete(ToolCall))
        await db.execute(delete(TokenUsageRecord))
        await db.execute(delete(LatencyRecord))
        await db.execute(delete(ModelUsage))
        await db.commit()

        print()
        print("=== ALL TESTS PASSED ===")


asyncio.run(test())
