# app/llm/responder.py

import os
import openai
from typing import List, Dict
import re

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set OpenAI API key from environment variable
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Set model name from environment or default


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

    # Combine all context chunks into a single string for the prompt
    context_text = "\n\n".join(
        f"[{chunk.get('policy_id', 'unknown')}]: {chunk.get('text', '')}"
        for chunk in context_chunks
    )

    # System prompt to instruct the LLM on its role and expected output
    system_prompt = """
You are an intelligent insurance assistant in a multi-turn conversation.

Your job:
1. Use the context provided to answer clearly.
2. Avoid repeating the same answers or suggesting the same actions again.
3. Understand what the user has already asked.
4. If context is unclear, ask for clarification.
5. At the end of each response, from new line suggest up to 2 next-step actions, create according to query, assume that the urls for the actions are already defined, provide urls or info for each action:

"""

    # Prepare the message payload for the OpenAI ChatCompletion API
    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"},
    ]

    # Call the OpenAI API to get the model's response
    response = openai.ChatCompletion.create(
        model=MODEL_NAME, messages=messages, temperature=0.4
    )

    # Extract the answer text from the API response
    raw_answer = response["choices"][0]["message"]["content"]

    # Return the answer and suggested next steps (parsed from the answer)
    return {
        "answer": raw_answer,
        "suggested_next_steps": extract_next_steps(raw_answer),
    }


def extract_next_steps(response_text: str) -> List[Dict]:
    """
    parser to simulate extracting next steps from LLM output.

    Args:
        response_text (str): The raw response from the LLM

    Returns:
        List[Dict]: List of { "text": str, "tag": str }
    """
    # Placeholder: implement with regex or instruction tuning later
    pattern = r'\{\s*"text":\s*"(.*?)",\s*"tag":\s*"(.*?)",\s*"action":\s*"(.*?)"\s*\}'
    matches = re.findall(pattern, response_text)

    if not matches:
        return []

    return [
        {"text": text, "tag": tag, "action": action}
        for text, tag, action in matches
    ]
