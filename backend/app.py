from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.llm_chosen import llm_response

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Backend is running"})

@app.route('/api/query', methods=['POST'])
def process_query():
    """Main endpoint to process user queries with RAG"""
    try:
        data = request.get_json()
        user_prompt = data.get('user_prompt', '')
        uid = data.get('uid', '')
        
        if not user_prompt:
            return jsonify({"error": "No user prompt provided"}), 400
        
        # TODO: Implement RAG pipeline
        # 1. Route query to appropriate LLM
        chosen_llm = "gpt"
        # 2. Retrieve context from vector database
        context = f"This is a placeholder context. RAG pipeline not yet implemented. (uid: {uid})"
        # 3. Generate response using RAG
        response = llm_response(chosen_llm, user_prompt, context)
        
        # Placeholder response
        response = {
            "answer": response,
            "chosen_llm": "placeholder",
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
    app.run(host='0.0.0.0', port=port, debug=debug) 