# app/core/chat/chat_service.py

from app.rag.vectorstore.qdrant_client import get_qdrant_client
from app.rag.vectorstore.embedder import generate_embeddings
from app.rag.vectorstore.vector_retriever import retrieve_relevant_chunks
from app.llm.responder import ask_chatgpt

def process_user_query(user_id: str, query: str) -> dict:
    """
    Full flow: user query → embedding → retrieval → LLM → response

    Args:
        user_id (str): Authenticated user ID
        query (str): User's input message

    Returns:
        dict: {
            "answer": str,
            "suggested_next_steps": List[Dict]
        }
    """
    print(f"📨 Query received from {user_id}: {query}")
    query_embedding = generate_embeddings([query])[0]

    client = get_qdrant_client()
    chunks = retrieve_relevant_chunks(client, query_embedding, user_id=user_id)

    response = ask_chatgpt(query=query, context_chunks=chunks)
    return response
