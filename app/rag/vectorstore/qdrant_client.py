# app/rag/vectorstore/qdrant_client.py

import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")  # Qdrant server URL
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)             # Qdrant API key (optional)
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "insurance_policies")  # Default collection name


def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client.

    Returns:
        QdrantClient: Connected Qdrant instance.
    """
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)  # Create and return Qdrant client


def ensure_collection(client: QdrantClient, vector_size: int):
    """
    Ensures the Qdrant collection exists with the correct configuration.

    Args:
        client (QdrantClient): Qdrant client instance.
        vector_size (int): Dimension of the embedding vectors.

    If the collection does not exist, it is created with the specified vector size and cosine distance.
    Also adds an index on 'policy_holder_id' for efficient filtering.
    """
    from app.config import QDRANT_COLLECTION

    if not client.collection_exists(QDRANT_COLLECTION):
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            on_disk=True,
        )

        # Add index for policy_holder_id to enable filtering
        client.create_payload_index(
            collection_name=QDRANT_COLLECTION,
            field_name="policy_holder_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )
