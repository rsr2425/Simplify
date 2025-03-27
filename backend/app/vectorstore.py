"""
Super early version of a vector store. Just want to make something available for the rest of the app to use.

Vector store implementation with singleton pattern to ensure only one instance exists.
"""

import os
import requests
import nltk
import logging
import requests

from typing import Optional, List, Union
from langchain_qdrant import QdrantVectorStore
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
_vector_db_instance: Optional[QdrantVectorStore] = None
_embedding_model: Optional[Union[OpenAIEmbeddings, HuggingFaceEmbeddings]] = None
_embedding_model_id: str = None


def _initialize_vector_db():
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
        )
        for doc in documents
    ]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_chunks = text_splitter.split_documents(enriched_docs)

    store_documents(
        split_chunks,
        PROBLEMS_REFERENCE_COLLECTION_NAME,
    )


def get_qdrant_client():
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
            # _qdrant_client_instance = QdrantClient(":memory:")
            return _qdrant_client_instance

        logger.info(
            f"Attempting to connect to Qdrant at {os.environ.get("QDRANT_URL")}"
        )
        try:
            _qdrant_client_instance = QdrantClient(
                url=os.environ.get("QDRANT_URL"),
                api_key=os.environ.get("QDRANT_API_KEY"),
            )
            logger.info("Successfully connected to Qdrant Cloud")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant Cloud: {str(e)}")
            raise e
    return _qdrant_client_instance


def get_all_unique_source_of_docs_in_collection(
    collection_name: str = PROBLEMS_REFERENCE_COLLECTION_NAME,
    limit: int = 1000,
    offset: int = 0,
) -> List[Document]:
    response = get_qdrant_client().scroll(
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
        response = get_qdrant_client().scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset + limit,
        )
    return list(result)


# TODO This is a dumb hack to get around Qdrant client restrictions when using local file storage.
# Instead of using the client directly, we use QdrantVectorStore's similarity search
# with a dummy query to get all documents, then extract unique sources.
def get_all_unique_source_of_docs_in_collection_DUMB(
    collection_name: str = PROBLEMS_REFERENCE_COLLECTION_NAME,
) -> List[str]:
    vector_store = get_vector_db()
    # Use a very generic query that should match everything
    docs = vector_store.similarity_search("", k=1000)

    sources = set()
    for doc in docs:
        if doc.metadata and "title" in doc.metadata:
            sources.add(doc.metadata["title"])
    return list(sources)


def store_documents(
    documents: List[Document],
    collection_name: str,
    embedding_model_id: str = None,
):
    global _vector_db_instance
    assert _vector_db_instance is not None, "Vector database instance not initialized"

    embedding_model = get_embedding_model(embedding_model_id)
    client = get_qdrant_client()

    _vector_db_instance.add_documents(
        documents=documents,
        ids=[get_document_hash_as_uuid(doc) for doc in documents],
    )


def get_embedding_model(embedding_model_id: str = None):
    """
    Factory function that returns a singleton instance of the embedding model.
    Creates the instance if it doesn't exist.
    """
    global _embedding_model, _embedding_model_id

    if _embedding_model is None or embedding_model_id != _embedding_model_id:
        if embedding_model_id is None:
            _embedding_model = OpenAIEmbeddings(model=DEFAULT_EMBEDDING_MODEL_ID)
        else:
            _embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_id)
        _embedding_model_id = embedding_model_id

    return _embedding_model


def get_vector_db(embedding_model_id: str = None) -> QdrantVectorStore:
    """
    Factory function that returns a singleton instance of the vector database.
    Creates the instance if it doesn't exist.
    """
    global _vector_db_instance

    if _vector_db_instance is None:
        need_to_initialize_db = False
        embedding_model = get_embedding_model(embedding_model_id)

        client = get_qdrant_client()

        if not check_collection_exists(client, PROBLEMS_REFERENCE_COLLECTION_NAME):
            client.create_collection(
                PROBLEMS_REFERENCE_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=DEFAULT_VECTOR_DIMENSIONS, distance=DEFAULT_VECTOR_DISTANCE
                ),
            )
            need_to_initialize_db = True

        os.makedirs(LOCAL_QDRANT_PATH, exist_ok=True)

        # TODO temp. Need to close and reopen client to avoid RuntimeError: Storage folder /data/qdrant_db is already accessed by another instance of Qdrant client. If you require concurrent access, use Qdrant server instead.
        #   Better solution is to use Qdrant server instead of local file storage, but I'm not sure I can run Docker Compose in Hugging Face Spaces.
        client.close()
        _vector_db_instance = QdrantVectorStore.from_existing_collection(
            # client=client,
            # TODO temp. If this works, go file bug with langchain-qdrant
            # location=":memory:",
            path=LOCAL_QDRANT_PATH,
            collection_name=PROBLEMS_REFERENCE_COLLECTION_NAME,
            embedding=embedding_model,
        )
        # TODO super hacky, but maybe I don't need client anymore? I'll just try to use QdrantVectorStore
        # just really trying not to instantiate a new client to access local path
        # because as long as QdrantVectorStore is instantiated, it will use the same client it created on the backend
        client = None

        if need_to_initialize_db:
            _initialize_vector_db()

        # vector_store = QdrantVectorStore(
        #     client=client,
        #     collection_name=PROBLEMS_REFERENCE_COLLECTION_NAME,
        #     embedding=embedding_model,
        # )

    return _vector_db_instance
