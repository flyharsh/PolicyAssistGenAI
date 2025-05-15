# tests/test_retrieval.py

import pytest
from unittest.mock import MagicMock
from app.rag.vectorstore.vector_retriever import retrieve_relevant_chunks


# Test retrieval filters chunks based on policy_holder_id
def test_retrieve_relevant_chunks_filters_user_id():
    mock_client = MagicMock()

    # Mock Qdrant response with payloads
    mock_client.search.return_value = [
        MagicMock(payload={"text": "Policy A", "policy_holder_id": "user_001"}),
        MagicMock(payload={"text": "Policy B", "policy_holder_id": "user_001"}),
    ]

    query_embedding = [0.01] * 384
    user_id = "user_001"

    # Execute retrieval
    results = retrieve_relevant_chunks(mock_client, query_embedding, user_id)

    # Assertions
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(r["policy_holder_id"] == user_id for r in results)
    mock_client.search.assert_called_once()
