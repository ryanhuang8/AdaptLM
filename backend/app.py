from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.llm_chosen import llm_response
from classifier.model_classifier import ModelRouter

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the model router globally
model_router = None

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
        
        # Use the model router to classify the prompt and choose the appropriate LLM
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

        # TODO: Implement RAG pipeline
        # 2. Retrieve context from vector database
        context = f"This is a placeholder context. RAG pipeline not yet implemented. (uid: {uid})"
        # 3. Generate response using RAG
        response = llm_response(chosen_llm, user_prompt, context)
        
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
    # Initialize model router on startup
    initialize_model_router()
    app.run(host='0.0.0.0', port=port, debug=debug) 