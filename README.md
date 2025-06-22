# AdaptLM

A comprehensive AI assistant platform with intelligent LLM routing, calendar integration, email services, and Retrieval-Augmented Generation (RAG) capabilities.

## Features

- **Intelligent LLM Router**: Analyzes user prompts and selects the most appropriate LLM (GPT, Claude, Gemini, Groq)
- **Google Calendar Integration**: Schedule appointments and manage calendar events
- **Email Services**: Send emails with customizable templates
- **FAISS Vector Store**: Stores and retrieves context using vector similarity
- **RAG Pipeline**: Combines retrieved context with LLM generation
- **Model Classification**: Intelligent routing based on prompt analysis

## Setup

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   chmod +x ./install.sh
   ./install.sh
   ```

2. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```bash
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

3. **Google Calendar Setup** (Optional):
   - Download `credentials.json` from Google Cloud Console
   - Place it in the backend directory
   - The first run will authenticate via OAuth

4. **Run the server**:
   ```bash
   source adaptlm_env/bin/activate  # Activate virtual environment
   python app.py
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env` file in the frontend directory:
   ```bash
   VITE_VAPI_API_KEY=your_vapi_api_key_here
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

## API Endpoints

### Health Check
- `GET /health` - Check if the backend is running

### Query Processing
- `POST /api/query` - Process user queries with intelligent LLM routing
  ```json
  {
    "user_prompt": "Your question here"
  }
  ```

### Calendar Management
- `POST /api/schedule` - Schedule calendar appointments
  ```json
  {
    "summary": "Meeting Title",
    "description": "Meeting Description",
    "start_time": "2024-01-15T10:00:00",
    "end_time": "2024-01-15T11:00:00",
    "timezone": "America/New_York"
  }
  ```

### Email Services
- `POST /api/send-email` - Send emails
  ```json
  {
    "to": "recipient@example.com",
    "subject": "Email Subject",
    "body": "Email content"
  }
  ```

## Key Features

### Intelligent LLM Routing
The system automatically selects the best LLM based on:
- Prompt complexity and type
- Required capabilities
- Cost considerations
- Response quality requirements

### Google Calendar Integration
- Schedule appointments programmatically
- Cross-platform compatibility
- Configurable via environment variables
- OAuth 2.0 authentication

### Email Services
- SMTP integration
- Customizable templates
- Secure authentication
- Multi-provider support

### Vector Store
- FAISS-based similarity search
- Context retrieval for RAG
- Efficient indexing and querying
- Scalable architecture

## Development

### Running Tests
```bash
cd backend
python testing.py
```

### Adding New LLM Models
1. Create a new model class in `models/`
2. Inherit from the base `LLM` class
3. Implement required methods
4. Add to the classifier logic

### Configuration
All settings are configurable via environment variables or the `config.py` file. See the setup section for available options.

## License

This project is licensed under the MIT License.