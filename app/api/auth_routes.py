# app/api/auth_routes.py

from flask import Blueprint, request, render_template, redirect, session
from app.core.chat.chat_service import process_user_query

auth_bp = Blueprint("auth", __name__)

# Dummy in-memory chat log (replace with DB later)
chat_memory = {}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")  # Ignored, placeholder
        if user_id:
            session["user_id"] = user_id
            chat_memory[user_id] = []  # Init log
            return redirect("/chat-ui")
    return render_template("login.html")

@auth_bp.route("/chat-ui", methods=["GET", "POST"])
def chat_ui():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            result = process_user_query(user_id, query)
            chat_memory[user_id].append({
                "user": query,
                "bot": result["answer"],
                "suggestions": result["suggested_next_steps"]
            })

    return render_template(
        "chat.html",
        user_id=user_id,
        chat_log=chat_memory.get(user_id, [])
    )
