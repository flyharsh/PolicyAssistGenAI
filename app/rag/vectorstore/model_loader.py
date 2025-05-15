# app/rag/vectorstore/model_loader.py

from sentence_transformers import SentenceTransformer
from functools import lru_cache
import os


@lru_cache(maxsize=1)
def load_embedding_model(model_name: str = None) -> SentenceTransformer:
    """
    Loads and caches the sentence transformer model.

    Args:
        model_name (str): Optional model name (from config or fallback).

    Returns:
        SentenceTransformer: The loaded model instance.
    """
    # Use provided model name or get from environment variable, fallback to default
    model_name = model_name or os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    print(f"🔄 Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)  # Load the sentence transformer model
    return model  # Return the loaded model instance
