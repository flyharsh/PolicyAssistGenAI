# app/rag/vectorstore/qdrant_client.py

import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "insurance_policies")

def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client.

    Returns:
        QdrantClient: Connected Qdrant instance.
    """
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

def ensure_collection(client: QdrantClient, vector_size: int):
    """
    Ensures the collection exists. Creates it if not.

    Args:
        client (QdrantClient): Qdrant connection
        vector_size (int): Dimension of embedding vector
    """
    if not client.collection_exists(COLLECTION_NAME):
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
