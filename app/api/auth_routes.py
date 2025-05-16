# app/api/auth_routes.py

from flask import Blueprint, request, render_template, redirect, session
from app.core.chat.chat_service import process_user_query
from flask import session, redirect, url_for

# Create a Flask Blueprint for authentication-related routes
auth_bp = Blueprint("auth", __name__)

# Dummy in-memory chat log (replace with persistent DB in production)
chat_memory = {}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.
    - GET: Render the login form.
    - POST: Store user_id in session and initialize chat log.
    """
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")  # Password is ignored (placeholder)
        if user_id:
            session["user_id"] = user_id  # Store user_id in session for later use
            chat_memory[user_id] = []     # Initialize chat log for this user
            return redirect("/chat-ui")   # Redirect to chat UI after login
    return render_template("login.html")  # Render login form on GET or failed POST


@auth_bp.route("/chat-ui", methods=["GET", "POST"])
def chat_ui():
    """
    Main chat interface.
    - GET: Render chat UI with chat history.
    - POST: Process user query, update chat log, and render updated chat UI.
    """
    user_id = session.get("user_id")
    if not user_id:
        # If user is not logged in, redirect to login page
        return redirect("/login")

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            # Process the user's query using the chat service
            result = process_user_query(user_id, query)
            # Append the user query and bot response to the chat log
            chat_memory[user_id].append(
                {
                    "user": query,
                    "bot": result["answer"],
                    "suggestions": result["suggested_next_steps"],
                }
            )

    # Render the chat UI template with the current chat log
    return render_template(
        "chat.html", user_id=user_id, chat_log=chat_memory.get(user_id, [])
    )

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("auth.login"))
