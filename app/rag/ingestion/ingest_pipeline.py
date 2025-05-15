# app/rag/ingestion/ingest_pipeline.py

import os
from tqdm import tqdm

from app.rag.ingestion.policy_loader import load_policy_documents
from app.rag.ingestion.text_splitter import split_text
from app.rag.vectorstore.embedder import generate_embeddings
from app.rag.vectorstore.qdrant_client import get_qdrant_client, ensure_collection
from app.rag.vectorstore.vector_uploader import upload_embeddings
from app.rag.vectorstore.model_loader import load_embedding_model

def ingest_all_policies(policy_folder: str):
    """
    Main pipeline to ingest all policy documents into Qdrant.

    Args:
        policy_folder (str): Directory containing policy JSON files
    """
    print(f"📄 Loading policies from {policy_folder}...")
    policies = load_policy_documents(policy_folder)
    model = load_embedding_model()
    vector_size = model.get_sentence_embedding_dimension()

    client = get_qdrant_client()
    ensure_collection(client, vector_size)

    for policy in tqdm(policies, desc="Ingesting policies"):
        policy_id = policy["policy_id"]
        user_id = policy["user_id"]
        policy_type = policy.get("policy_type", "unknown")
        full_text = policy.get("policy_text", "")

        if not full_text.strip():
            print(f"⚠️ Skipping empty policy: {policy_id}")
            continue

        chunks = split_text(full_text)
        embeddings = generate_embeddings(chunks)

        metadata_list = [
            {
                "policy_id": policy_id,
                "policy_holder_id": user_id,
                "chunk_index": i,
                "policy_type": policy_type
            }
            for i in range(len(chunks))
        ]

        upload_embeddings(client, embeddings, metadata_list)

    print("🚀 Ingestion complete.")

ingest_all_policies("data/policies")