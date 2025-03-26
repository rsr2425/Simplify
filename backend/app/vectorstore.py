"""
Super early version of a vector store. Just want to make something available for the rest of the app to use.

Vector store implementation with singleton pattern to ensure only one instance exists.
"""

import os
import requests
import nltk
import logging
import uuid
import hashlib

from typing import Optional, List
from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain.schema import Document
from .vectorstore_helpers import (
    get_document_hash_as_uuid,
    enrich_document_metadata,
    check_collection_exists,
)

nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")

DEFAULT_EMBEDDING_MODEL_ID = "text-embedding-3-small"
DEFAULT_VECTOR_DIMENSIONS = 1536
DEFAULT_VECTOR_DISTANCE = Distance.COSINE
PROBLEMS_REFERENCE_COLLECTION_NAME = "problems_reference_collection"
LOCAL_QDRANT_PATH = "/data/qdrant_db"

logger = logging.getLogger(__name__)

# Global variable to store the singleton instance
_qdrant_client_instance: Optional[QdrantClient] = None
_vector_db_instance: Optional[Qdrant] = None
# TODO fix bug. There's a logical error where if you change the embedding model, the vector db instance might not updated
#   to match the new embedding model.
_embedding_model_id: str = None


def _get_qdrant_client():
    global _qdrant_client_instance

    if _qdrant_client_instance is None:
        if (
            os.environ.get("QDRANT_URL") is None
            or os.environ.get("QDRANT_API_KEY") is None
        ):
            logger.warning(
                "QDRANT_URL or QDRANT_API_KEY is not set. Defaulting to local memory vector store."
            )

            os.makedirs(LOCAL_QDRANT_PATH, exist_ok=True)
            _qdrant_client_instance = QdrantClient(path=LOCAL_QDRANT_PATH)

        QDRANT_URL = os.environ.get("QDRANT_URL")
        QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

        _qdrant_client_instance = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    return _qdrant_client_instance


def _initialize_vector_db(embedding_model):
    os.makedirs("static/data", exist_ok=True)

    html_path = "static/data/langchain_rag_tutorial.html"
    if not os.path.exists(html_path):
        url = "https://python.langchain.com/docs/tutorials/rag/"
        response = requests.get(url)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)

    loader = DirectoryLoader("static/data", glob="*.html")
    documents = loader.load()

    enriched_docs = [
        enrich_document_metadata(
            doc,
            title="LangChain RAG Tutorial",
            type="tutorial",
            source_url="https://python.langchain.com/docs/tutorials/rag/",
            description="Official LangChain tutorial on building RAG applications",
            date_added="2024-03-21",
            category="documentation",
            version="1.0",
            language="en",
            original_source=doc.metadata.get("source"),
        )
        for doc in documents
    ]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_chunks = text_splitter.split_documents(enriched_docs)

    client = _get_qdrant_client()
    store_documents(
        split_chunks,
        PROBLEMS_REFERENCE_COLLECTION_NAME,
        client,
    )


def get_all_unique_source_docs_in_collection(
    collection_name: str, client: QdrantClient, limit: int = 1000, offset: int = 0
) -> List[Document]:
    response = client.scroll(
        collection_name=collection_name,
        limit=limit,
        offset=offset,
        with_payload=["source"],
        with_vectors=False,
    )
    result = set()
    while len(response[0]) > 0:
        for point in response[0]:
            if "source" in point.payload:
                result.add(point.payload["source"])
        offset = response[1]
        response = client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset + limit,
        )
    return list(result)


def store_documents(
    documents: List[Document],
    collection_name: str,
    client: QdrantClient,
    embedding_model=None,
):
    if embedding_model is None:
        embedding_model = OpenAIEmbeddings(model=DEFAULT_EMBEDDING_MODEL_ID)

    if not check_collection_exists(client, collection_name):
        client.create_collection(
            collection_name,
            vectors_config=VectorParams(
                size=DEFAULT_VECTOR_DIMENSIONS, distance=DEFAULT_VECTOR_DISTANCE
            ),
        )

    vectorstore = Qdrant(
        client=client, collection_name=collection_name, embeddings=embedding_model
    )

    vectorstore.add_documents(
        documents=documents,
        ids=[get_document_hash_as_uuid(doc) for doc in documents],
    )


# TODO already probably exposing too much by returning a Qdrant object here
def get_vector_db(embedding_model_id: str = None) -> Qdrant:
    """
    Factory function that returns a singleton instance of the vector database.
    Creates the instance if it doesn't exist.
    """
    global _vector_db_instance

    if _vector_db_instance is None:
        embedding_model = None
        if embedding_model_id is None:
            embedding_model = OpenAIEmbeddings(model=DEFAULT_EMBEDDING_MODEL_ID)
        else:
            embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_id)

        client = _get_qdrant_client()
        collection_info = client.get_collection(PROBLEMS_REFERENCE_COLLECTION_NAME)
        if collection_info.vectors_count is None or collection_info.vectors_count == 0:
            _initialize_vector_db(embedding_model)

        _vector_db_instance = Qdrant.from_existing_collection(
            collection_name=PROBLEMS_REFERENCE_COLLECTION_NAME,
            embedding_model=embedding_model,
            client=client,
        )

    return _vector_db_instance
