# app/rag/vectorstore/vector_retriever.py

from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchParams

from app.rag.vectorstore.qdrant_client import COLLECTION_NAME


def retrieve_relevant_chunks(
    client: QdrantClient, query_embedding: List[float], user_id: str, top_k: int = 5
) -> List[str]:
    """
    Retrieves the most relevant chunks for a given user based on query embedding.

    Args:
        client (QdrantClient): Qdrant instance
        query_embedding (List[float]): The vector for the user's query
        user_id (str): ID of the logged-in user
        top_k (int): Number of results to return

    Returns:
        List[str]: List of retrieved payloads (chunk text and metadata)
    """
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        search_params=SearchParams(hnsw_ef=128),  # Use HNSW search with specified ef parameter
        query_filter=Filter(
            must=[
                FieldCondition(key="policy_holder_id", match=MatchValue(value=user_id))
            ]
        ),  # Filter results by user ID for privacy
    )

    # Return the payload (text and metadata) for each retrieved chunk
    return [point.payload for point in results]
