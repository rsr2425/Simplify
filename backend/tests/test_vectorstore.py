import pytest
import os
from langchain.schema import Document
from backend.app import vectorstore

def test_directory_creation():
    """Test that the static/data directory is created"""
    assert os.path.exists("static/data")
    assert os.path.exists("static/data/langchain_rag_tutorial.html")

def test_html_content():
    """Test that the HTML content was downloaded and contains expected content"""
    with open("static/data/langchain_rag_tutorial.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for some expected content from the LangChain RAG tutorial
    assert "RAG" in content
    assert "LangChain" in content

def test_vector_store_similarity_search():
    """Test that the vector store can perform similarity search"""
    # Test query
    query = "What is RAG?"
    
    # Perform similarity search
    results = vectorstore.vector_db.similarity_search(query, k=2)
    
    # Verify we get results
    assert len(results) == 2
    assert isinstance(results[0], Document)
    
    # Verify the results contain relevant content
    combined_content = " ".join([doc.page_content for doc in results]).lower()
    assert "rag" in combined_content
    assert "retrieval" in combined_content