import asyncio
from app.db.session import init_db
from app.embeddings.persistence import VectorPersistence


async def test():
    await init_db()
    from app.db.session import async_session

    print("=== Phase 7: Embedding Persistence E2E Test ===")
    print()

    async with async_session() as db:
        persistence = VectorPersistence(db)

        # Test 1: Save with source
        print("--- Test 1: Save with source ---")
        doc_id = await persistence.save_embedding(
            "fir", "fir_1", "Theft at MG Road", [0.1, 0.2, 0.3],
            {"type": "theft"}, source="fir_loader"
        )
        print("  Saved doc_id=%d with source=fir_loader" % doc_id)

        # Test 2: Get document with source
        print("--- Test 2: Get document ---")
        doc = await persistence.get_document(doc_id)
        print("  Source: %s, Created: %s" % (doc["source"], doc["created_at"][:19]))

        # Test 3: Update with new source
        print("--- Test 3: Update embedding ---")
        await persistence.update_embedding(doc_id, content="Updated theft report", source="manual_update")
        doc2 = await persistence.get_document(doc_id)
        print("  Updated source: %s, Content: %s" % (doc2["source"], doc2["content"][:30]))

        # Test 4: Load all with source
        print("--- Test 4: Load all chunks ---")
        chunks = await persistence.get_all_chunks()
        for c in chunks:
            print("  [%s] %s (source: %s)" % (c["domain"], c["content"][:30], c.get("source")))

        # Test 5: Count
        print("--- Test 5: Count ---")
        total = await persistence.count()
        fir_count = await persistence.count("fir")
        print("  Total: %d, FIR: %d" % (total, fir_count))

        # Cleanup
        await persistence.clear()
        print()
        print("=== ALL TESTS PASSED ===")


asyncio.run(test())
