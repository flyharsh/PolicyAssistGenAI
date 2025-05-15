# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "insurance_policies")

# Flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev")
FLASK_PORT = int(os.getenv("FLASK_PORT", 8000))
