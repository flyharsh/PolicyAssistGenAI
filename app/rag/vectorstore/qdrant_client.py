# app/rag/vectorstore/qdrant_client.py

import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType

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
    from app.config import QDRANT_COLLECTION

    if not client.collection_exists(QDRANT_COLLECTION):
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            on_disk=True
        )

        # Add index for policy_holder_id to enable filtering
        client.create_payload_index(
            collection_name=QDRANT_COLLECTION,
            field_name="policy_holder_id",
            field_schema=PayloadSchemaType.KEYWORD
        )