# app/main.py

from flask import Flask
from flask_cors import CORS
from app.api.chat_routes import chat_bp
from app.api.auth_routes import auth_bp
from app.config import FLASK_SECRET_KEY, FLASK_PORT

def create_app():
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY
    CORS(app)

    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        return {"message": "Insurance Chatbot API is running!"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=FLASK_PORT)
