# tests/test_llm.py

import pytest
from app.llm.responder import extract_next_steps


# Test that extract_next_steps returns structured list from plain LLM response
def test_extract_next_steps_structure():
    llm_response = (
        "Sure. Your policy covers hospital visits up to $100,000.\n"
        "- Would you like to see your deductible? (show_details)\n"
        "- Do you want to initiate a new claim? (initiate_process)"
    )

    steps = extract_next_steps(llm_response)

    # Should return a list of suggestion dicts
    assert isinstance(steps, list)
    for step in steps:
        assert "text" in step
        assert "tag" in step
        assert isinstance(step["text"], str)
        assert isinstance(step["tag"], str)
