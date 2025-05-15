# app/rag/ingestion/collection_manager.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType
from app.config import QDRANT_COLLECTION

def reset_and_prepare_collection(client: QdrantClient, vector_size: int):
    """
    Deletes and recreates the collection with indexed fields for filtering.

    Args:
        client (QdrantClient): Qdrant client instance
        vector_size (int): Dimension of the embeddings
    """
    if client.collection_exists(QDRANT_COLLECTION):
        print(f"🧹 Dropping existing collection: {QDRANT_COLLECTION}")
        client.delete_collection(QDRANT_COLLECTION)

    print(f"📦 Creating collection: {QDRANT_COLLECTION}")
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

    print("🔑 Creating index for `policy_holder_id` field")
    client.create_payload_index(
        collection_name=QDRANT_COLLECTION,
        field_name="policy_holder_id",
        field_schema=PayloadSchemaType.KEYWORD
    )
