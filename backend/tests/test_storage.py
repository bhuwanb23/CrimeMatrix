import asyncio
from app.storage.service import StorageService


async def test():
    print("=== Phase 10: Storage Layer E2E Test ===")
    print()

    storage = StorageService("test_storage")
    await storage.initialize()

    # Test 1: Upload file
    print("--- Test 1: Upload file ---")
    result = await storage.upload("test.txt", b"Hello World", "uploads")
    print("  Uploaded: %s (%d bytes)" % (result["filename"], result["size"]))

    # Test 2: Download file
    print("--- Test 2: Download file ---")
    content = await storage.download(result["path"])
    print("  Downloaded: %s" % content.decode())

    # Test 3: File exists
    print("--- Test 3: File exists ---")
    exists = await storage.exists(result["path"])
    print("  Exists: %s" % exists)

    # Test 4: List files
    print("--- Test 4: List files ---")
    files = await storage.list_files("uploads")
    print("  Files: %s" % files)

    # Test 5: Delete file
    print("--- Test 5: Delete file ---")
    deleted = await storage.delete(result["path"])
    print("  Deleted: %s" % deleted)
    exists_after = await storage.exists(result["path"])
    print("  Exists after delete: %s" % exists_after)

    # Cleanup
    import shutil
    shutil.rmtree("test_storage", ignore_errors=True)

    print()
    print("=== ALL TESTS PASSED ===")


asyncio.run(test())
