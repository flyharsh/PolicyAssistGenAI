# 🧠 PolicyAssistGenAI

_A modular, production-grade GenAI chatbot that understands your data—built with RAG and LLM-driven control flow._

---

## 📘 User Guide

### 🧩 Introduction

PolicyAssistGenAI is a smart, user-aware assistant that lets users interact with their insurance policy documents using natural language.  
The system uses **retrieval-augmented generation (RAG)** and **filtered semantic search** to generate contextual responses tailored to each user’s data.

It is designed with scalability and extensibility at its core—making it adaptable to any document-heavy domain beyond insurance.

---

### ❓ Problem It Solves

Insurance data is buried in dense PDFs, hard-to-navigate portals, or call center workflows. Most users:

- Don’t know what policy conditions they have
- Struggle to access premium or claim details
- Waste time parsing jargon-heavy policy documents
- Can’t get answers without policy numbers or form IDs

**PolicyAssistGenAI removes that friction by:**

- Letting users ask real questions in natural language
- Surfacing only **their own** relevant policy information
- Suggesting smart next actions using **LLM-driven control flow**
- Embedding privacy-aware RAG—your data stays in your control

---

### 🌱 Extensible by Design

This app isn’t just an insurance chatbot—it’s a **reusable framework** for document-based GenAI agents.

> **Plug and play with any data at any scale**—while you have complete control over your data.  
> The app can be extended to read from **any source**—local files, APIs, cloud buckets, or databases—**powered by private RAG**.

**Ideal for:**

- 📊 Finance – investment analysis bots  
- 🏥 Healthcare – policy explainers, eligibility assistants  
- 🏛️ Legal – contract clause Q&A agents  
- 🏫 Education – syllabus and catalog assistants  
- 🛠 Enterprise – HR handbooks, IT helpdesk bots

---

### 👤 Who It’s For

- **Insurance customers** who want instant, personalized answers  
- **Internal support agents** who need to reduce manual lookups  
- **Builders** exploring how to operationalize LLMs over private data  

---

## 🛠️ Developer Guide

### 🧰 Tech Stack & Methodologies

| Layer           | Stack                          |
|-----------------|--------------------------------|
| Web Framework   | Python + Flask + Jinja2        |
| Retrieval       | Qdrant Vector DB (filtered RAG)|
| Embeddings      | Sentence Transformers (MiniLM) |
| LLM Response    | OpenAI GPT-3.5 Turbo (via API) |
| Frontend        | HTML (Jinja2 Templates)        |
| Config          | `.env` (per environment)       |
| Container       | Docker                         |
| Testing         | `pytest`                       |

**Development Principles:**

- 🔁 **Modularity-first** — each layer is isolated, testable, and swappable.
- ✅ **Production-readiness** — environment-aware config, clean logs, and fallbacks.
- 🧩 **Plug-and-play** — works with any data source and can be adapted easily.
- 🔐 **Private RAG** — user-scoped chunk retrieval ensures data privacy.

---

### 🧠 Architecture Overview

```
[ UI ] <--→ [ Flask Server ]
                  ↓
         [ User Query Handler ]
                  ↓
         [ Embedding (MiniLM) ]
                  ↓
    [ Qdrant Vector Search w/ Filters ]
                  ↓
     [ Retrieved Chunks + Metadata ]
                  ↓
         [ LLM Prompt Builder ]
                  ↓
      [ OpenAI GPT-3.5 Turbo Response ]
                  ↓
     [ Answer + Suggested Next Steps ]
```

Each query passes through a modular pipeline that:

1. Embeds the user query
2. Filters chunks by policy_holder_id
3. Sends filtered context to the LLM
4. Returns a concise answer + LLM-suggested follow-ups

---

### 🔁 Query Lifecycle

1. User logs in using a simple form (sets user_id in session)
2. Enters a query in natural language
3. Query → Embedded using Sentence Transformers
4. Embedded vector → Sent to Qdrant, filtered by user_id
5. Top matching chunks → Passed to OpenAI GPT-3.5 Turbo

**LLM generates:**

- 🧠 A relevant answer
- 🧭 Up to 2 follow-up suggestions with action tags

Answer is displayed in chat UI with suggestions rendered below.

> 🧩 This flow is generic and can support finance, legal, healthcare, or enterprise FAQs etc — just by changing the documents and filters.

---

## ⚙️ Setup Instructions

### 🔧 Prerequisites

- Python 3.10+
- Docker (for Qdrant)
- A valid OpenAI API Key
- `git` installed

---

### 📦 Installation & Running (Step-by-Step)

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourname/PolicyAssistGenAI.git
    cd PolicyAssistGenAI
    ```

2. **Create Virtual Environment**
    ```bash
    python -m venv .venv
    # For Windows:
    .venv\Scripts\activate
    # For Unix/Mac:
    source .venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Start Qdrant (Docker)**
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
    ```

5. **Configure Environment Variables**
    - Create a `.env` file in the root directory.
    - Use the `.env.example` as a reference.

6. **Run Ingestion Script**
    ```bash
    python app/rag/ingestion/ingest_pipeline.py
    ```

7. **Start the Application**
    ```bash
    python app/main.py
    ```

---

### 🧪 Testing

To run all test cases:
```bash
pytest tests/
```

---

### 🚀 App Runs At

- [http://localhost:8000/login](http://localhost:8000/login) → Login UI
- [http://localhost:8000/chat-ui](http://localhost:8000/chat-ui) → Chat interface

---

## 📦 Dependencies

### 🧰 Python Libraries

| Package                  | Purpose                                 |
|--------------------------|-----------------------------------------|
| `flask`                  | API server and web routing              |
| `jinja2`                 | HTML templating for frontend            |
| `openai`                 | ChatGPT API integration                 |
| `qdrant-client`          | Vector database client                  |
| `sentence-transformers`  | Embedding model for RAG                 |
| `python-dotenv`          | Load `.env` config across environments  |
| `tqdm`                   | Progress bars for ingestion             |
| `requests`               | HTTP utilities                          |
| `pytest`                 | Unit testing                            |

---

### 🐳 Container Dependencies

- **Docker** – required for running Qdrant locally

---

### 🧠 Models Used

| Model                      | Role           |
|----------------------------|----------------|
| `all-MiniLM-L6-v2` (SBERT) | Text embedding |
| `gpt-3.5-turbo` (OpenAI)   | LLM response   |

> All models and keys are environment-configurable via `.env`.

---

## 📷 Screenshots + UX Flow

> A guided walkthrough of the user experience, with screenshots and context.

1. **Login Screen**
![login page](docs\screenshots\image-login.png)
    - Simple form captures the `user_id` and a dummy password.
    - No real authentication—just session tracking.
    - This `user_id` is used to filter personalized policy responses.
![logged in](docs\screenshots\image-lgdin.png)

2. **Chat Interface**
![chat window](docs\screenshots\chat-window.png)

3. **RAG-Powered Answering**
![QA with bot](docs\screenshots\chat-context.png)
  
4. **Follow-up Suggestions**
![wherever relevant- suggests follow-up steps](docs\screenshots\follow_up-context.png)

5. **Data Isolation Preview**
![only responds with user specific data](docs\screenshots\context-chatui.png)

        -in all the screenshots and end session button is visible- that clears current session and send back to login screen


---

## 🧼 Code Design & Quality Principles

This project prioritizes **readability, modularity, and maintainability**—following clean architecture and 12-factor design principles.

---

### 🧩 Modular Architecture

The app is divided into logical, reusable layers:

| Module      | Responsibility                                 |
|-------------|------------------------------------------------|
| `api/`      | HTTP routes (chat, login)                      |
| `core/`     | Application logic (chat service, control flow) |
| `rag/`      | Ingestion + vector storage and retrieval       |
| `llm/`      | Prompt building and response handling          |
| `ui/`       | Jinja-based frontend (login + chat pages)      |
| `utils/`    | Logger, validators, formatting helpers         |


## 🗂 Project Structure & File Purpose (Detailed)

A well-organized, modular layout with each component documented.

---

### 🔧 Root Level

| File/Folder              | Description |
|--------------------------|-------------|
| `README.md`              | Complete project overview, instructions, and context |
| `Dockerfile`             | Production-ready container spec for the Flask app |
| `docker-compose.yml`     | Defines local services: app + Qdrant |
| `requirements.txt`       | All dependencies with pinned versions |
| `.env`                   | Environment-specific config (e.g., API keys, model names) |
| `data/policies/`         | JSON files representing mocked insurance policies per user |

---

### 🔁 Ingestion: `app/rag/ingestion/`

| File/Folder              | Description |
|--------------------------|-------------|
| `ingest_pipeline.py`     | Orchestrates full ingestion: load → chunk → embed → upload |
| `policy_loader.py`       | Reads and parses JSON policy files |
| `text_splitter.py`       | Chunks long policy texts into manageable segments |
| `collection_manager.py`  | Creates and indexes Qdrant collection with user-level filters |

---

### 📦 Vector Store: `app/rag/vectorstore/`

| File                     | Description |
|--------------------------|-------------|
| `model_loader.py`        | Loads and caches the sentence-transformer model |
| `embedder.py`            | Encodes text chunks into dense vector embeddings |
| `qdrant_client.py`       | Connects to and manages Qdrant client instance |
| `vector_uploader.py`     | Uploads embedded chunks with metadata into Qdrant |
| `vector_retriever.py`    | Performs vector search with user-specific filtering (RAG) |

---

### 🤖 LLM Layer: `app/llm/`

| File                     | Description |
|--------------------------|-------------|
| `responder.py`           | Sends user query + context to OpenAI and parses response |
| `prompt_builder.py`      | (Optional) Build advanced templated system prompts |

---

### 🧠 Core Logic: `app/core/`

| File                     | Description |
|--------------------------|-------------|
| `chat/chat_service.py`   | Central handler for query → retrieval → LLM → final answer |

---

### 🌐 API Routes: `app/api/`

| File                     | Description |
|--------------------------|-------------|
| `chat_routes.py`         | Exposes `/chat` POST endpoint for programmatic use |
| `auth_routes.py`         | Handles `/login` and `/chat-ui` UI logic and session state |

---

### 🎨 Frontend UI: `app/ui/`

| File                     | Description |
|--------------------------|-------------|
| `templates/login.html`   | Minimal login form (user_id + dummy password) |
| `templates/chat.html`    | Main chat interface for sending questions + viewing answers |
| `static/style.css`       | Optional custom styles for the frontend |

---

### 🛠 Utilities: `app/utils/`

| File                     | Description |
|--------------------------|-------------|
| `logger.py`              | Logging setup and abstraction (extendable) |
| `validators.py`          | Basic input validation or sanitization logic |
| `formatter.py`           | Response formatting and cleaning tools |

---

### 🧪 Tests: `tests/`

| File                     | Description |
|--------------------------|-------------|
| `test_auth.py`           | Validates UI/login flow behavior |
| `test_chat.py`           | Tests end-to-end query processing with mock LLM |
| `test_llm.py`            | Ensures correct LLM prompt handling + response structure |
| `test_retrieval.py`      | Verifies vector search + metadata filtering |

---


---

### 🧪 Testability

- Every layer is independently testable
- Mocked test cases using `pytest`
- No hard-coded secrets or stateful global logic

---
### 🧪 Quality Checks

- ✅ 100% passing unit tests (`pytest`)
- ✅ Code coverage tracked (`pytest-cov`)
- ✅ Lint clean (`flake8`)
- ✅ Auto-formatted with Black (`PEP8-compliant`)

### 📦 Config Management

- Environment-specific settings via `.env`
- Separate config for OpenAI, Qdrant, port, secrets, models

---

### 🧠 LLM Prompting

- System prompts are templated and modular
- Follow-up suggestions include action tags like:
  - `ask_clarification`
  - `show_details`
  - `initiate_process`

---

### 🛡️ Safety & Clean Code Practices

- No direct file reads without validation
- Every component has docstrings
- Proper logging in ingestion, vectoring, and API layers
- Error handling on all critical actions (file loads, API calls, Qdrant queries)

---

### 🧠 Reusability

- Vector embedding and search pipeline is abstracted
- Any document format can be added with new loaders
- Retrieval logic can work with any metadata filter (not just `policy_holder_id`)

> ✅ This codebase is audit-ready, and built with future extensibility in mind.

---

## 🚀 Future Scope

PolicyAssistGenAI is architected for long-term growth and multi-domain adaptability. The following enhancements are envisioned to take this from demo-grade to production-ready:

### 🔐 Authentication & Access Control

- Integrate OAuth2, JWT, or SSO for real authentication
- Role-based access (e.g., user vs. admin)

---

### 📚 Multi-Document Support

- Allow users to upload and query:
  - Claims documents
  - Bills
  - Policy amendments
- Support PDFs, CSVs, and scanned text via OCR

---

### 💬 Chat Memory + Context

- Persistent chat session storage (Redis, SQLite, or PostgreSQL)
- Use previous turns as LLM context to improve continuity

---

### 🧾 Admin Dashboard

- See logs of user interactions
- Upload and manage new policy document sets
- Track query patterns and suggestions used

---

### ⚙️ Advanced RAG Capabilities

- Document summarization
- Chunk ranking with confidence scores
- Hybrid search (keyword + vector + metadata)

---

### 📊 Analytics + Feedback Loop

- Rate the LLM response quality
- Track which actions are clicked most
- Close the feedback loop to improve the LLM’s guidance

---

### 🌍 Deployment Enhancements

- Docker Compose setup (Flask + Qdrant + Nginx)
- K8s-ready manifests
- CI/CD pipeline for test, lint, build

> 🚧 These features can be scoped based on production use case—whether customer-facing, internal support, or a data discovery tool.

---

## 🙌 Credits & Contact

This project was conceptualized, developed, and refined as part of a GenAI interview demonstration to showcase:

- Production-level coding patterns
- Clean RAG + LLM orchestration
- Extensible chatbot architecture
- Testable, maintainable code structure

---

### 👨‍💻 Author

**Harsh**  
Data Engineer | AI Builder | GenAI Developer  
📍 Toronto  
📫 flyharsh2@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/flyharsh/)

---

### 🔗 Project Link

GitHub: [github.com/yourname/PolicyAssistGenAI](https://github.com/yourname/PolicyAssistGenAI)

---

> If you'd like to collaborate, extend this project, or want a walkthrough, feel free to reach out.