from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.llm_chosen import llm_response

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

def initialize_model_router():
    """Initialize the model router asynchronously"""
    global model_router
    try:
        model_router = ModelRouter()
        model_router.initialize_model()
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
        results = vector_store.query(user_prompt, top_k=3)

        context_parts = []
        for result in results:
            if 'metadata' in result and 'text' in result['metadata']:
                context_parts.append(result['metadata']['text'])
        return jsonify({
            "context": "\n".join(context_parts)
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
        global model_router
        if model_router is None:
            chosen_llm = "gpt"
            print("Warning: Model router not initialized, using fallback LLM")
        else:
            try:
                chosen_llm = model_router.classify(user_prompt)
                print(f"Prompt classified to use: {chosen_llm}")
            except Exception as e:
                print(f"Error classifying prompt: {e}")
                chosen_llm = "gpt"  # Fallback to GPT
        print(f"Chosen LLM: {chosen_llm}")

        response = llm_response(chosen_llm, uid, vector_store, user_prompt, previous_prompt, previous_output)
        
        # Placeholder response
        response = {
            "answer": response,
            "chosen_llm": chosen_llm,
            "context_used": [],
            "confidence_score": 0.0,
            "processing_time": 0.0
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": "Failed to process query",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask server on port {port}")
    # Initialize model router on startupAdd commentMore actions
    initialize_model_router()
    initialize_vector_store()
    app.run(host='0.0.0.0', port=port, debug=debug) 