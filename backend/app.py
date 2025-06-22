import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.llm_chosen import LLMRouter

from classifier.model_classifier import ModelRouter
from vector_store import PineconeVectorStore

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize global variables
model_router = None
previous_prompt = ""
previous_output = ""
vector_store = None # TODO: replace with uid
llm_router = None

def initialize_model_router():
    """Initialize the model router asynchronously"""
    global model_router
    try:
        model_router = ModelRouter()
        print("Model router initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing model router: {e}")
        model_router = None
        return False

def initialize_vector_store():
    global previous_prompt
    global previous_output
    global vector_store

    try:
        vector_store = PineconeVectorStore(index_name=f"alerihglhiuaerg")
        return True
    except Exception as e:
        vector_store = None
        return False

def initialize_llm_router():
    """Initialize the LLM router"""
    global llm_router
    try:
        llm_router = LLMRouter()
        print("LLM router initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing LLM router: {e}")
        llm_router = None
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    global model_router
    router_status = "initialized" if model_router is not None else "not_initialized"
    return jsonify({
        "status": "healthy", 
        "message": "Backend is running",
        "model_router": router_status
    })

@app.route('/api/get_voice_llm', methods=['GET'])
def get_llm():
    """Get the LLM for """
    global model_router
    if model_router is None:
        chosen_llm = "gpt"
        print("Warning: Model router not initialized, using fallback LLM")
    else:
        try:
            user_prompt = "Help me answer general questions"
            chosen_llm = model_router.classify(user_prompt)
            print(f"Prompt classified to use: {chosen_llm}")
        except Exception as e:
            print(f"Error classifying prompt: {e}")
            chosen_llm = "gpt"  # Fallback to GPT
    print(f"Chosen LLM: {chosen_llm}")
    response = {
        "chosen_llm": chosen_llm
    }
    return jsonify(response)

@app.route('/api/get_context', methods=['GET'])
def get_context():
    """Get the context for the user"""
    global vector_store
    if vector_store is None:
        return jsonify({
            "context": ["This is a placeholder context."]
        })
    else:
        user_prompt = "Help me answer general questions"
        results = vector_store.query(user_prompt, top_k=7)

        context_parts = []
        for result in results:
            if 'metadata' in result and 'text' in result['metadata']:
                context_parts.append(result['metadata']['text'])
        return jsonify({
            "context": "\n".join(context_parts)
        })

@app.route('/api/post_context', methods=['POST'])
def post_context():
    """Post the context for the user"""
    global vector_store
    if vector_store is None:
        return jsonify({
            "error": "Vector store not initialized"
        }), 500
    else:
        data = request.get_json()
        context = data.get('context', '')
        try:
            def ingest_worker():
                try:
                    assert vector_store is not None
                    vector_store.upsert_texts([context])
                    print(f"✅ Context ingested asynchronously: {context[:50]}...")
                except Exception as e:
                    print(f"❌ Error ingesting context asynchronously: {e}")
            
            # Start ingestion in background thread
            thread = threading.Thread(target=ingest_worker, daemon=True)
            thread.start()
            
        except Exception as e:
            print(f"Error starting async context ingestion: {e}")
            
        return jsonify({
            "success": True,
            "message": "Context posted successfully"
        })

@app.route('/api/initialize', methods=['POST'])
def initialize_router():
    """Manual endpoint to initialize the model router"""
    success = initialize_model_router()
    return jsonify({
        "success": success,
        "message": "Model router initialized" if success else "Failed to initialize model router"
    })

@app.route('/api/query', methods=['POST'])
def process_query():
    """Main endpoint to process user queries with RAG"""
    try:
        data = request.get_json()
        user_prompt = data.get('user_prompt', '')
        uid = data.get('uid', '')
        
        if not user_prompt:
            return jsonify({"error": "No user prompt provided"}), 400
        
        # Use the model router to classify the prompt and choose the appropriate LLMAdd commentMore actions
        global model_router, llm_router
        if model_router is None:
            chosen_llm = "gpt"
            actual_llm = chosen_llm
            print("Warning: Model router not initialized, using fallback LLM")
        else:
            try:
                chosen_llm = model_router.classify(user_prompt)
                print(f"Prompt classified to use: {chosen_llm}")
            except Exception as e:
                print(f"Error classifying prompt: {e}")
                chosen_llm = "gpt"  # Fallback to GPT
        print(f"Chosen LLM: {chosen_llm}")

        # Use LLM router if available, otherwise fallback to legacy function
        if llm_router is not None and vector_store is not None:
            response = llm_router.llm_response(chosen_llm, uid, vector_store, user_prompt, previous_prompt, previous_output)
            conversation_state = llm_router.get_conversation_state()
            
            # Determine the actual LLM being used
            if conversation_state.get('is_in_agent_mode', False):
                actual_llm = "gpt"  # Agent is handling the request
            else:
                actual_llm = chosen_llm  # Original LLM is being used
        else:
            # Fallback to legacy function
            from services.llm_chosen import llm_response
            response = llm_response(chosen_llm, uid, vector_store, user_prompt, previous_prompt, previous_output)
            conversation_state = {"is_in_agent_mode": False, "original_llm": chosen_llm}
            actual_llm = chosen_llm
        
        print(f"Actual LLM------------HIGHLIGHT: {actual_llm}")
        # Placeholder response
        response = {
            "answer": response,
            "chosen_llm": chosen_llm,
            "context_used": [],
            "confidence_score": 0.0,
            "processing_time": 0.0,
            "conversation_state": conversation_state
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": "Failed to process query",
            "message": str(e)
        }), 500

@app.route('/api/conversation-state', methods=['GET'])
def get_conversation_state():
    """Get the current conversation state"""
    global llm_router
    if llm_router is not None:
        state = llm_router.get_conversation_state()
        return jsonify(state)
    else:
        return jsonify({"error": "LLM router not initialized"}), 500

@app.route('/api/reset-conversation', methods=['POST'])
def reset_conversation():
    """Reset the conversation state"""
    global llm_router
    if llm_router is not None:
        llm_router.reset_conversation_state()
        return jsonify({"message": "Conversation reset successfully"})
    else:
        return jsonify({"error": "LLM router not initialized"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask server on port {port}")
    # Initialize model router on startupAdd commentMore actions
    initialize_model_router()
    initialize_vector_store()
    initialize_llm_router()
    app.run(host='0.0.0.0', port=port, debug=debug) 