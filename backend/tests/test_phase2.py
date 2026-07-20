import asyncio
from app.graph.network import GraphManager
from app.vector.embedder import VectorStore
from app.cache.local_cache import LocalCache
from app.storage.local_storage import LocalStorage


async def test_storage():
    storage = LocalStorage()
    await storage.upload('test.txt', b'Hello CrimeMatrix!')
    data = await storage.download('test.txt')
    print(f"Storage upload/download: {data}")
    files = await storage.list_files()
    print(f"Storage files: {files}")
    await storage.delete('test.txt')
    print("Storage delete: OK")


def test_graph():
    gm = GraphManager()
    gm.add_node('RK', 'suspect', name='Ravi Kumar')
    gm.add_node('DR', 'suspect', name='Deepak Reddy')
    gm.add_node('CASE', 'case', title='Theft')
    gm.add_edge('RK', 'DR', 'accomplice')
    gm.add_edge('RK', 'CASE', 'linked_to')
    print(f"Graph: {gm.graph.number_of_nodes()} nodes, {gm.graph.number_of_edges()} edges")
    neighbors = gm.get_neighbors('RK')
    print(f"RK neighbors: {len(neighbors)}")


def test_vector():
    vs = VectorStore()
    vs.add_document('c1', 'Theft at Malleshwaram')
    vs.add_document('c2', 'Robbery in Indiranagar')
    vs.add_document('c3', 'Burglary at Whitefield')
    results = vs.search('theft')
    print(f"Vector search: {len(results)} results")


def test_cache():
    cache = LocalCache()
    cache.set('test', 'hello', 300)
    print(f"Cache get: {cache.get('test')}")
    cache.delete('test')
    print(f"Cache after delete: {cache.get('test')}")


if __name__ == "__main__":
    print("=== Phase 2 Tests ===\n")
    test_graph()
    test_vector()
    test_cache()
    asyncio.run(test_storage())
    print("\n✅ All Phase 2 modules working!")
