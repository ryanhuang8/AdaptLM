# ContextLLM Backend

A Flask backend that implements a Retrieval-Augmented Generation (RAG) system with intelligent LLM routing.

## Features

- **LLM Router**: Analyzes user prompts and selects the most appropriate LLM
- **FAISS Vector Store**: Stores and retrieves context using vector similarity
- **RAG Pipeline**: Combines retrieved context with LLM generation
- **RESTful API**: Clean endpoints for frontend integration

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── services/            # Core services
│   ├── __init__.py
│   ├── llm_router.py    # LLM selection logic
│   ├── vector_store.py  # FAISS vector database
│   └── rag_service.py   # RAG pipeline orchestration
└── models/              # Data models
    ├── __init__.py
    └── request_models.py # Request/response models
```

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file with:
   ```
   FLASK_DEBUG=False
   PORT=8080
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Run the server**:
   ```bash
   python app.py
   ```

## API Endpoints

### Health Check
- `GET /health` - Check if the backend is running

### Query Processing
- `POST /api/query` - Process user queries with RAG
  ```json
  {
    "user_prompt": "Your question here"
  }
  ```