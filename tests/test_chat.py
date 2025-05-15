# tests/test_chat.py

import pytest
from unittest.mock import patch
from app.core.chat.chat_service import process_user_query


# Test the full chat pipeline with all dependencies mocked
@patch("app.core.chat.chat_service.generate_embeddings")
@patch("app.core.chat.chat_service.get_qdrant_client")
@patch("app.core.chat.chat_service.retrieve_relevant_chunks")
@patch("app.core.chat.chat_service.ask_chatgpt")
def test_process_user_query(mock_ask, mock_retrieve, mock_qdrant, mock_embed):
    # Step 1: Setup mocks
    mock_embed.return_value = [[0.1] * 384]
    mock_retrieve.return_value = [
        {"policy_id": "P123", "text": "coverage includes hospital stays"}
    ]
    mock_ask.return_value = {
        "answer": "Your policy covers hospitalization.",
        "suggested_next_steps": [{"text": "View deductible", "tag": "show_details"}],
    }

    # Step 2: Run the chat service
    result = process_user_query("user_001", "What does my policy cover?")

    # Step 3: Assert output
    assert "answer" in result
    assert "suggested_next_steps" in result
    assert isinstance(result["suggested_next_steps"], list)
