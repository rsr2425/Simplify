from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_crawl_endpoint():
    response = client.post(
        "/crawl/",
        json={"url": "https://example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "received"}

def test_problems_endpoint():
    response = client.post(
        "/problems/",
        json={"user_query": "test query"}
    )
    assert response.status_code == 200
    assert "Problems" in response.json()
    assert len(response.json()["Problems"]) == 5 
    