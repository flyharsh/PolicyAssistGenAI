# app/rag/vectorstore/embedder.py

from typing import List
from app.rag.vectorstore.model_loader import load_embedding_model


def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    """
    Converts list of text chunks into embeddings.

    Args:
        chunks (List[str]): List of string chunks.

    Returns:
        List[List[float]]: List of dense vector embeddings.
    """
    model = load_embedding_model()  # Load the embedding model
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)  # Generate embeddings for all chunks
    return embeddings.tolist()  # Convert numpy array to list and return
