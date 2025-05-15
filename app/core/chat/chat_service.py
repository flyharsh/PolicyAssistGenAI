# app/core/chat/chat_service.py

from app.rag.vectorstore.qdrant_client import get_qdrant_client  # Import function to get Qdrant vector DB client
from app.rag.vectorstore.embedder import generate_embeddings     # Import function to generate embeddings for queries
from app.rag.vectorstore.vector_retriever import retrieve_relevant_chunks  # Import function to retrieve relevant chunks
from app.llm.responder import ask_chatgpt                        # Import function to interact with LLM (ChatGPT)


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
    print(f"📨 Query received from {user_id}: {query}")  # Log the incoming query for debugging
    query_embedding = generate_embeddings([query])[0]    # Generate embedding for the user query

    client = get_qdrant_client()                         # Get Qdrant vector database client
    chunks = retrieve_relevant_chunks(client, query_embedding, user_id=user_id)  # Retrieve relevant context chunks

    response = ask_chatgpt(query=query, context_chunks=chunks)  # Get response from LLM using query and context
    return response  # Return the response dictionary
