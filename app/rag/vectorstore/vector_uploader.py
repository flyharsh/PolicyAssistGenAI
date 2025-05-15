# app/rag/vectorstore/vector_uploader.py

import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from app.rag.vectorstore.qdrant_client import COLLECTION_NAME


def upload_embeddings(
    client: QdrantClient,
    embeddings: List[List[float]],
    metadata_list: List[Dict[str, Any]],
):
    """
    Uploads vector embeddings with metadata to Qdrant.

    Args:
        client (QdrantClient): Qdrant DB client
        embeddings (List[List[float]]): List of vectors
        metadata_list (List[Dict]): Metadata dict per chunk
    """
    # Ensure the number of embeddings matches the number of metadata entries
    assert len(embeddings) == len(
        metadata_list
    ), "Embedding and metadata count mismatch"

    points = []  # List to hold PointStruct objects for Qdrant
    for i, (vector, metadata) in enumerate(zip(embeddings, metadata_list)):
        # Create a unique ID for each point and attach its vector and metadata
        points.append(
            PointStruct(id=str(uuid.uuid4()), vector=vector, payload=metadata)
        )

    # Upload all points to the specified Qdrant collection
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Uploaded {len(points)} vectors to Qdrant.")
