"""
Super early version of a vector store. Just want to make something available for the rest of the app to use.

Vector store implementation with singleton pattern to ensure only one instance exists.
"""

import os
import requests
import nltk
import logging
from typing import Optional
from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")

DEFAULT_EMBEDDING_MODEL_ID = "text-embedding-3-small"
LOCAL_QDRANT_PATH = "/data/qdrant_db"

logger = logging.getLogger(__name__)

# Global variable to store the singleton instance
_vector_db_instance: Optional[Qdrant] = None
# TODO fix bug. There's a logical error where if you change the embedding model, the vector db instance might not updated
#   to match the new embedding model.
_embedding_model_id: str = None


def get_qdrant_client():
    if os.environ.get("QDRANT_URL") is None or os.environ.get("QDRANT_API_KEY") is None:
        logger.error(
            "QDRANT_URL or QDRANT_API_KEY is not set. Defaulting to local memory vector store."
        )

        os.makedirs(LOCAL_QDRANT_PATH, exist_ok=True)
        return QdrantClient(path=LOCAL_QDRANT_PATH)

    QDRANT_URL = os.environ.get("QDRANT_URL")
    QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def get_vector_db(embedding_model_id: str = None) -> Qdrant:
    """
    Factory function that returns a singleton instance of the vector database.
    Creates the instance if it doesn't exist.
    """
    global _vector_db_instance

    if _vector_db_instance is None:
        # Create static/data directory if it doesn't exist
        os.makedirs("static/data", exist_ok=True)

        # Download and save the webpage if it doesn't exist
        html_path = "static/data/langchain_rag_tutorial.html"
        if not os.path.exists(html_path):
            url = "https://python.langchain.com/docs/tutorials/rag/"
            response = requests.get(url)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(response.text)

        embedding_model = None
        if embedding_model_id is None:
            embedding_model = OpenAIEmbeddings(modzŻel=DEFAULT_EMBEDDING_MODEL_ID)
        else:
            embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_id)

        # Load HTML files from static/data directory
        loader = DirectoryLoader("static/data", glob="*.html")
        documents = loader.load()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        split_chunks = text_splitter.split_documents(documents)

        # Create vector store instance
        client = get_qdrant_client()
        _vector_db_instance = Qdrant.from_documents(
            split_chunks,
            embedding_model,
            client=client,
            collection_name="extending_context_window_llama_3",
        )

    return _vector_db_instance
