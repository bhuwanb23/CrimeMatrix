from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

try:
    response = client.post("/api/v1/search/", json={"query": "test", "filters": []})
    print(response.status_code)
    print(response.json())
except Exception as e:
    import traceback
    traceback.print_exc()
