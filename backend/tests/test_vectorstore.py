import os
from langchain.schema import Document
from backend.app.vectorstore import get_vector_db

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
    
    # Verify they are the same object
    assert instance1 is instance2