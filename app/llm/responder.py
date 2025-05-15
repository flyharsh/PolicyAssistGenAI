# app/llm/responder.py

import os
import openai
from typing import List, Dict

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def ask_chatgpt(query: str, context_chunks: List[Dict]) -> Dict:
    """
    Sends the user query + relevant context to ChatGPT and returns the response.

    Args:
        query (str): The user's question
        context_chunks (List[Dict]): Retrieved policy chunks (payloads)

    Returns:
        Dict: {
            "answer": str,
            "suggested_next_steps": List[Dict]
        }
    """

    context_text = "\n\n".join(
        f"[{chunk.get('policy_id', 'unknown')}]: {chunk.get('text', '')}" for chunk in context_chunks
    )

    system_prompt = """
You are a helpful insurance assistant. Use the context below to answer the user's question clearly and concisely.
Also suggest up to 2 next possible actions with tags like:
- ask_clarification
- show_details
- initiate_process
- explore_related
"""

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
    ]

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.4
    )

    raw_answer = response["choices"][0]["message"]["content"]

    return {
        "answer": raw_answer,
        "suggested_next_steps": extract_next_steps(raw_answer)
    }

def extract_next_steps(response_text: str) -> List[Dict]:
    """
    Dummy parser to simulate extracting next steps from LLM output.

    Returns:
        List[Dict]: List of { "text": str, "tag": str }
    """
    # Placeholder: implement with regex or instruction tuning later
    return [
        {"text": "Would you like me to show your deductible details?", "tag": "show_details"},
        {"text": "Do you want to initiate a new claim?", "tag": "initiate_process"}
    ]
