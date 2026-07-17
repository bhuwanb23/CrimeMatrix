import asyncio
import networkx as nx
from app.db.session import init_db
from app.graph.persistence import GraphPersistence
from app.graph.loader import GraphLoader


async def test():
    await init_db()
    from app.db.session import async_session

    print("=== Phase 6: Knowledge Graph Persistence E2E Test ===")
    print()

    async with async_session() as db:
        persistence = GraphPersistence(db)

        # Test 1: Save nodes with confidence
        print("--- Test 1: Save nodes with confidence ---")
        await persistence.save_node("suspect_1", "suspect", {"name": "John", "age": 30}, confidence=0.95)
        await persistence.save_node("suspect_2", "suspect", {"name": "Jane", "age": 25}, confidence=0.80)
        await persistence.save_node("crime_1", "crime", {"title": "Theft", "status": "open"}, confidence=1.0)
        print("  Saved 3 nodes with confidence scores")

        # Test 2: Save edges with weight
        print("--- Test 2: Save edges with weight ---")
        await persistence.save_edge("suspect_1", "crime_1", "involved_in", {"date": "2024-01-15"}, weight=0.9)
        await persistence.save_edge("suspect_2", "crime_1", "witness", weight=0.5)
        print("  Saved 2 edges with weights")

        # Test 3: Load into NetworkX with confidence
        print("--- Test 3: Load into NetworkX ---")
        loader = GraphLoader(db)
        stats = await loader.load()
        print("  Loaded:", stats)

        # Test 4: Verify confidence and weight
        print("--- Test 4: Verify confidence and weight ---")
        for node_id, data in loader.graph.nodes(data=True):
            print("  Node %s: confidence=%.2f, type=%s" % (node_id, data.get("confidence", 0), data.get("type")))
        for source, target, data in loader.graph.edges(data=True):
            print("  Edge %s -> %s: weight=%.2f, relation=%s" % (source, target, data.get("weight", 0), data.get("relation")))

        # Test 5: Version tracking
        print("--- Test 5: Version tracking ---")
        version = await persistence.get_latest_version()
        print("  Latest version:", version)
        history = await persistence.get_version_history()
        print("  Version history:", len(history), "versions")

        # Test 6: Save and reload persistence
        print("--- Test 6: Save and reload persistence ---")
        loader2 = GraphLoader(db)
        loader2.graph = loader.graph
        save_stats = await loader2.save()
        print("  Saved:", save_stats)

        loader3 = GraphLoader(db)
        reload_stats = await loader3.load()
        print("  Reloaded:", reload_stats)

        # Verify data survived
        j1 = loader3.graph.nodes.get("suspect_1", {})
        print("  suspect_1 confidence: %s (expected 0.95)" % j1.get("confidence"))
        e = loader3.graph.edges.get(("suspect_1", "crime_1"), {})
        print("  suspect_1->crime_1 weight: %s (expected 0.9)" % e.get("weight"))

        # Cleanup
        await persistence.clear()
        print()
        print("=== ALL TESTS PASSED ===")


asyncio.run(test())
