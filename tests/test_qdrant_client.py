# tests/test_qdrant_client.py

import pytest
from unittest.mock import patch, MagicMock
from app.rag.vectorstore.qdrant_client import get_qdrant_client, ensure_collection

# Test that get_qdrant_client returns a client instance
@patch("app.rag.vectorstore.qdrant_client.QdrantClient")
def test_get_qdrant_client_returns_instance(MockClient):
    client = get_qdrant_client()
    assert isinstance(client, MockClient)

# Test that collection is recreated when missing and index is added
@patch("app.rag.vectorstore.qdrant_client.QdrantClient")
def test_ensure_collection_creates_if_missing(MockClient):
    mock = MockClient()
    mock.collection_exists.return_value = False

    ensure_collection(mock, vector_size=384)

    mock.recreate_collection.assert_called_once()
    mock.create_payload_index.assert_called_once_with(
        collection_name="insurance_policies",
        field_name="policy_holder_id",
        field_schema=mock.create_payload_index.call_args[1]["field_schema"],
    )
