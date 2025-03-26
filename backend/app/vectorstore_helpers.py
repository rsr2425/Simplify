import hashlib
import uuid

from langchain.schema import Document
from qdrant_client import QdrantClient
from typing import List


def check_collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """Check if a collection exists in Qdrant."""
    return client.get_collection(collection_name) is not None


def get_document_hash_as_uuid(doc):
    content_hash = hashlib.sha256(doc.page_content.encode()).hexdigest()
    uuid_from_hash = uuid.UUID(content_hash[:32])
    return str(uuid_from_hash)


def enrich_document_metadata(doc: Document, **additional_metadata) -> Document:
    doc.metadata.update(additional_metadata)
    return doc
