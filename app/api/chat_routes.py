# app/api/chat_routes.py

from flask import Blueprint, request, jsonify
from app.core.chat.chat_service import process_user_query

# Create a Flask Blueprint for chat-related routes
chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Accepts a user query and returns an answer + next step suggestions.

    Expects JSON payload:
    {
        "user_id": "<user identifier>",
        "query": "<user's question>"
    }

    Returns:
        200: JSON with answer and suggested next steps.
        400: If user_id or query is missing.
        500: If an internal error occurs.
    """
    data = request.get_json()  # Parse JSON payload from request
    user_id = data.get("user_id")  # Extract user_id from payload
    query = data.get("query")      # Extract query from payload

    if not user_id or not query:
        # Return error if required fields are missing
        return jsonify({"error": "Missing user_id or query"}), 400

    try:
        # Process the user's query using the chat service
        result = process_user_query(user_id, query)
        return jsonify(result), 200  # Return result as JSON
    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"error": str(e)}), 500
