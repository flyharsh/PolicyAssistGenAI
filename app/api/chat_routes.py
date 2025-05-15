# app/api/chat_routes.py

from flask import Blueprint, request, jsonify
from app.core.chat.chat_service import process_user_query

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Accepts a user query and returns an answer + next step suggestions.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    query = data.get("query")

    if not user_id or not query:
        return jsonify({"error": "Missing user_id or query"}), 400

    try:
        result = process_user_query(user_id, query)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
