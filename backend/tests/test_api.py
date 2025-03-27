from fastapi.testclient import TestClient
from backend.app.main import app
import pytest

client = TestClient(app)


def test_crawl_endpoint():
    response = client.post("/api/ingest/", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert response.json() == {"status": "received"}


def test_problems_endpoint():
    response = client.post("/api/problems/", json={"user_query": "RAG"})
    assert response.status_code == 200
    assert "Problems" in response.json()
    assert len(response.json()["Problems"]) == 5


def test_feedback_validation_error():
    """Test that mismatched problems and answers lengths return 400"""
    response = client.post(
        "/api/feedback",
        json={
            "user_query": "Python lists",
            "problems": ["What is a list?", "How do you append?"],
            "user_answers": [
                "A sequence",
            ],  # Only one answer
        },
    )

    assert response.status_code == 400
    assert "same length" in response.json()["detail"]


# this test can be a bit flaky, but it's not a big deal (because it's checking the content of the response. Correct/Incorrect might be prefaced by /n or something)
def test_successful_feedback():
    """Test successful grading of multiple problems"""
    response = client.post(
        "/api/feedback",
        json={
            "user_query": "RAG",
            "problems": [
                "What are the two main components of a typical RAG application?",
                "What is the purpose of the indexing component in a RAG application?",
            ],
            "user_answers": [
                "A list is a mutable sequence type that can store multiple items in Python",
                "You use the append() method to add an element to the end of a list",
            ],
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert "feedback" in result
    assert len(result["feedback"]) == 2

    for feedback in result["feedback"]:
        assert feedback.strip().startswith(("Correct", "Incorrect"))
        assert len(feedback.split(". ")) >= 2


def test_topics_endpoint():
    """Test that topics endpoint returns expected sources"""
    response = client.post("/api/topics")
    assert response.status_code == 200
    result = response.json()
    
    assert "sources" in result
    assert len(result["sources"]) == 1
    assert result["sources"][0] == "LangChain RAG Tutorial"
