import os
import socket
import pytest
import requests

from langchain.schema import Document
from backend.app.vectorstore import get_vector_db, get_qdrant_client


def test_directory_creation():
    get_vector_db()
    assert os.path.exists("static/data")
    assert os.path.exists("static/data/langchain_rag_tutorial.html")


# TODO remove this test when data ingrestion layer is implemented
def test_html_content():
    with open("static/data/langchain_rag_tutorial.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for some expected content from the LangChain RAG tutorial
    assert "RAG" in content
    assert "LangChain" in content


def test_vector_store_similarity_search():
    """Test that the vector store can perform similarity search"""
    # Test query
    query = "What is RAG?"

    # Get vector db instance and perform similarity search
    vector_db = get_vector_db()
    results = vector_db.similarity_search(query, k=2)

    # Verify we get results
    assert len(results) == 2
    assert isinstance(results[0], Document)

    # Verify the results contain relevant content
    combined_content = " ".join([doc.page_content for doc in results]).lower()
    assert "rag" in combined_content
    assert "retrieval" in combined_content


def test_vector_db_singleton():
    """Test that get_vector_db returns the same instance each time"""
    # Get two instances
    instance1 = get_vector_db()
    instance2 = get_vector_db()

    assert instance1 is instance2


def test_qdrant_cloud_connection():
    """Test basic connectivity to Qdrant Cloud"""
    # Skip test if not configured for cloud
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):

        pytest.skip("Qdrant Cloud credentials not configured")

    try:
        # Print URL for debugging (excluding any path components)
        qdrant_url = os.environ.get("QDRANT_URL", "")
        print(f"Attempting to connect to Qdrant at: {qdrant_url}")

        # Try to parse the URL components
        from urllib.parse import urlparse

        parsed_url = urlparse(qdrant_url)
        print(f"Scheme: {parsed_url.scheme}")
        print(f"Hostname: {parsed_url.hostname}")
        print(f"Port: {parsed_url.port}")
        print(f"Path: {parsed_url.path}")

        client = get_qdrant_client()
        client.get_collections()
        assert True, "Connection successful"
    except Exception as e:
        assert False, f"Failed to connect to Qdrant Cloud: {str(e)}"


def test_external_connectivity():
    """Test basic external connectivity and DNS resolution.
    Test needed since Docker gave an issue with this before. Couldn't resolve Qdrant host.
    """

    # Skip test if not configured for cloud
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        pytest.skip("Qdrant Cloud credentials not configured")

    # Test DNS resolution first
    try:
        # Try to resolve google.com
        google_ip = socket.gethostbyname("google.com")
        print(f"Successfully resolved google.com to {google_ip}")

        # If we have Qdrant URL, try to resolve that too
        qdrant_url = os.environ.get("QDRANT_URL", "")
        if qdrant_url:
            qdrant_host = (
                qdrant_url.replace("https://", "").replace("http://", "").split("/")[0]
            )
            print(f"Qdrant host: {qdrant_host}")
            qdrant_ip = socket.gethostbyname(qdrant_host)
            print(f"Successfully resolved Qdrant host {qdrant_host}")
    except socket.gaierror as e:
        assert False, f"DNS resolution failed: {str(e)}"

    # Test HTTP connectivity
    try:
        response = requests.get("https://www.google.com", timeout=5)
        assert (
            response.status_code == 200
        ), "Expected successful response from google.com"
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to google.com: {str(e)}"
