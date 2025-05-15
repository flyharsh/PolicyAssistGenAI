# app/rag/ingestion/text_splitter.py

from typing import List


def split_text(text: str, max_tokens: int = 200) -> List[str]:
    """
    Splits policy text into smaller chunks for embedding.

    Args:
        text (str): Full policy text.
        max_tokens (int): Max tokens per chunk (approximate, by word count).

    Returns:
        List[str]: List of text chunks.
    """
    words = text.split()  # Split the text into words
    chunks = []  # List to hold all text chunks
    for i in range(0, len(words), max_tokens):
        # Join a slice of words to form a chunk
        chunk = " ".join(words[i : i + max_tokens])
        chunks.append(chunk)  # Add the chunk to the list
    return chunks  # Return the list of chunks
