# app/rag/ingestion/ingest_pipeline.py

import os
from tqdm import tqdm

from app.rag.ingestion.policy_loader import load_policy_documents
from app.rag.ingestion.text_splitter import split_text
from app.rag.vectorstore.embedder import generate_embeddings
from app.rag.vectorstore.qdrant_client import get_qdrant_client, ensure_collection
from app.rag.vectorstore.vector_uploader import upload_embeddings
from app.rag.vectorstore.model_loader import load_embedding_model
from app.rag.ingestion.collection_manager import reset_and_prepare_collection
from app.rag.vectorstore.qdrant_client import get_qdrant_client
from app.rag.vectorstore.model_loader import load_embedding_model


def ingest_all_policies(policy_folder: str):
    """
    Main pipeline to ingest all policy documents into Qdrant.

    Args:
        policy_folder (str): Directory containing policy JSON files

    This function:
    - Loads all policy documents from the specified folder.
    - Loads the embedding model and determines the vector size.
    - Connects to Qdrant and resets the collection.
    - Splits each policy into chunks, generates embeddings, and uploads them with metadata.
    """
    print(f"📄 Loading policies from {policy_folder}...")
    policies = load_policy_documents(policy_folder)  # Load all policy JSON files
    model = load_embedding_model()                   # Load embedding model
    vector_size = model.get_sentence_embedding_dimension()  # Get embedding vector size

    client = get_qdrant_client()                    # Get Qdrant client
    reset_and_prepare_collection(client, vector_size)  # Reset and prepare Qdrant collection

    for policy in tqdm(policies, desc="Ingesting policies"):
        policy_id = policy["policy_id"]             # Extract policy ID
        user_id = policy["user_id"]                 # Extract user ID
        policy_type = policy.get("policy_type", "unknown")  # Extract policy type
        full_text = policy.get("policy_text", "")   # Extract policy text

        if not full_text.strip():
            print(f"⚠️ Skipping empty policy: {policy_id}")  # Skip empty policies
            continue

        chunks = split_text(full_text)              # Split policy text into chunks
        embeddings = generate_embeddings(chunks)    # Generate embeddings for each chunk

        # Prepare metadata for each chunk
        metadata_list = [
            {
                "policy_id": policy_id,
                "policy_holder_id": user_id,
                "chunk_index": i,
                "policy_type": policy_type,
            }
            for i in range(len(chunks))
        ]

        upload_embeddings(client, embeddings, metadata_list)  # Upload embeddings and metadata to Qdrant

    print("🚀 Ingestion complete.")


ingest_all_policies("data/policies")  # Run the ingestion pipeline on the default folder
