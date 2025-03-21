from fastapi.testclient import TestClient
from backend.app.main import app
import pytest

client = TestClient(app)


def test_crawl_endpoint():
    response = client.post("/api/crawl/", json={"url": "https://example.com"})
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


@pytest.mark.asyncio
async def test_successful_feedback():
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

    # Check that responses start with either "Correct" or "Incorrect"
    for feedback in result["feedback"]:
        assert feedback.startswith(("Correct", "Incorrect"))
        # Check that there's an explanation after the classification
        assert len(feedback.split(". ")) >= 2
