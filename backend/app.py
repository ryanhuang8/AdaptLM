from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

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
        
        if not user_prompt:
            return jsonify({"error": "No user prompt provided"}), 400
        
        # TODO: Implement RAG pipeline
        # 1. Route query to appropriate LLM
        # 2. Retrieve context from vector database
        # 3. Generate response using RAG
        
        # Placeholder response
        response = {
            "answer": "This is a placeholder response. RAG pipeline not yet implemented.",
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