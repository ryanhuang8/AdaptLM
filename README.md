# AdaptLM

Your go-to LLM hosting platform — seamlessly harnessing the strengths of multiple models in a single session, powered by dynamic, intelligent services.

## 🚀 Inspiration  
What's your favorite LLM to use?  
✨ Mine is **Claude** — I love how well it handles coding.  
✨ Sometimes I switch to **Groq** — it's just so fast.  

But juggling between LLMs means:  
- Opening multiple tabs  
- Copy-pasting between models  
- Refeeding prior context over and over  

💡 No more. That's why we built **AdaptLM**.  

## ⚡ What it does  

**AdaptLM** is an intelligent LLM orchestrator that:  
- **Automatically selects the best LLM** for your prompt based on context and task  
- **Seamlessly integrates multiple LLMs in a single session** — with shared context and no manual switching  
- **Uses RAG to share context across models**, so every LLM stays informed  
- **Routes prompts using Vellum AI benchmarks and advanced NLP**, matching intent to the ideal model  
- **Provides agentic tools** to handle tasks like emailing and calendar setup — all within the same flow  
- **Supports voice interaction via Vapi**, so you can speak directly to your AI assistant  

### ✨ Key Features
- **Intelligent LLM Router**: Analyzes user prompts and selects the most appropriate LLM (GPT, Claude, Gemini, Groq)
- **Google Calendar Integration**: Schedule appointments and manage calendar events
- **Email Services**: Send emails with customizable templates
- **FAISS Vector Store**: Stores and retrieves context using vector similarity
- **RAG Pipeline**: Combines retrieved context with LLM generation
- **Model Classification**: Intelligent routing based on prompt analysis

### 🎤 Voice Control  
Too busy to type?  
✅ Simply enable **voice via Vapi** and interact with the selected LLM hands-free.  

## 🛠️ How we built it  

A visual diagram can be represented below:

![AdaptLM screenshot](https://i.imgur.com/lNf18bA.png)

### **Frontend**
- **React 19.1.0** with **Vite 6.3.5** for fast, modern development  
- **Firebase 11.9.1** for authentication and backend services  
- **Vapi AI Web SDK 2.3.6** for voice AI capabilities  
- **ESLint** for maintaining code quality  

### **Backend**
- **Flask 2.3.3** as the core web framework  
- **Multiple LLM APIs**: OpenAI (GPT), Anthropic (Claude), Google (Gemini), Groq  
- **Pinecone 7.2.0** as the vector database  
- **Sentence Transformers 4.1.0** for generating text embeddings  
- **Google APIs** for Calendar and Gmail integrations  

### **Key Architecture Features**
- **LLM Router** using advanced NLP techniques for intelligent model selection  
- **RAG pipeline** for context sharing across multiple LLMs within a session  
- **Voice AI integration** with speech-to-text and text-to-speech via Vapi  

## ⚙️ Setup

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

## 📡 API Endpoints

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

## 🛠️ Challenges we ran into  

- **Capturing the semantics and intent of the prompt**  
  Designing an NLP-based router that accurately understands both the task and subtle intent behind a prompt — and maps it to the right LLM — required significant fine-tuning and experimentation.  

- **Addressing the bottleneck of vector embedding ingestion**  
  Ingesting embeddings into a vector database can introduce latency — but users still need instant access to context. We tackled this by designing a solution that keeps the user experience smooth while embeddings process in the background. 

- **Integrating Vapi for voice control**  
  Ensuring smooth speech-to-text and text-to-speech conversion, while maintaining accurate model selection and context continuity, was a complex task involving both frontend and backend coordination.  

## 🏆 Accomplishments that we're proud of  

- **Innovative solution for dynamic LLM selection**  
  We successfully designed and implemented an architecture that tackles the challenge of choosing the right LLM for the task — without user intervention.  

- **Seamless handling of multiple LLMs with shared context**  
  AdaptLM can switch between models while maintaining context awareness, thanks to our RAG-powered pipeline.  

- **Integrated agentic services without extra steps**  
  Users can send emails, create calendar events, and more — all within the same flow, no manual setup or switching required!  

## 📚 What we learned  

- **Model selection is harder than it looks**  
  Understanding the true intent of a prompt and matching it to the best LLM requires more than just keywords — it demands careful NLP design and real-world testing.  

- **Context sharing across models is critical**  
  Without seamless context transfer (via RAG), switching between models breaks the user experience. We learned how vital it is to maintain continuity for a smooth workflow.  

- **Voice and agentic integration add huge value — but also complexity**  
  Combining voice interfaces and agentic services with multi-LLM orchestration taught us a lot about managing asynchronous systems and delivering a consistent, responsive UX.  

## 🔧 Development

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

## 🌟 What's next for AdaptLM  

- **Scale to more LLMs**  
  We plan to expand support to additional models, giving users even greater flexibility and performance options.  

- **Universal API**  
  Our goal is to build a single API layer that lets developers access multiple LLMs through one unified endpoint — no more juggling different APIs.  

- **Define a prompt taxonomy for smarter routing**  
  We aim to create a clear taxonomy for prompt types (e.g. cost-efficient, reasoning-heavy, simple language tasks) to enable faster, smarter, and more cost-effective model selection.  

## 📄 License

This project is licensed under the MIT License.
