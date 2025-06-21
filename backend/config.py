"""
Configuration settings for the Flask backend
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # LLM API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Vector Store settings
    FAISS_INDEX_PATH = os.getenv('FAISS_INDEX_PATH', './data/faiss_index')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # RAG settings
    MAX_CONTEXT_LENGTH = 2000
    TOP_K_RETRIEVAL = 5 