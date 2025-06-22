import os
import threading
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv

from vector_store import PineconeVectorStore

# Load environment variables from .env
load_dotenv()

class BaseLLM(ABC):
    """
    Abstract base class for LLM implementations with context-aware features.
    """

    # Model configuration mappings
    MODEL_NAMES = {
        "gpt": "gpt-4o",
        "gemini": "gemini-2.0-flash",
        "groq": "meta-llama/llama-4-scout-17b-16e-instruct",
        "claude": "claude-opus-4-20250514"
    }

    API_KEY_NAMES = {
        "gpt": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY", 
        "groq": "GROQ_API_KEY",
        "claude": "ANTHROPIC_API_KEY"
    }

    def __init__(
            self, 
            model_name: str,
            temperature: float = 0.5, 
            token_limit: int = 1000,
            system_prompt: str = "",
            user_id: Optional[str] = None,
            vector_store: Optional[PineconeVectorStore] = None
            ):
        """
        Initialize the LLM.

        Args:
            model_name: The name of the model to use (gpt, gemini, groq, claude)
            temperature: Temperature for text generation (0.0 to 1.0)
            token_limit: Maximum tokens for responses
            system_prompt: System prompt for the model
            user_id: User identifier for vector store isolation
            vector_store: Vector store instance for context management

        Raises:
            ValueError: If model_name is invalid, user_id is None, or vector_store is None
        """

        if model_name not in self.MODEL_NAMES:
            raise ValueError(f"Model {model_name} not supported. Use: {', '.join(self.MODEL_NAMES.keys())}")
        
        # Initialize model configuration
        self.model_name = self.MODEL_NAMES[model_name]
        self.model_api_key_name = self.API_KEY_NAMES[model_name]
        self.api_key = self._get_api_key(self.model_api_key_name)
        
        if not self.api_key:
            raise ValueError(f"API key not found for {model_name}. Please set {self.model_api_key_name} environment variable.")
        
        # Validate required parameters
        if user_id is None:
            raise ValueError("User ID is required for this model.")
        self.user_id = user_id

        if vector_store is None:
            raise ValueError("Vector store is required for this model.")

        # Store the vector store instance
        self.vector_store = vector_store
        
        # Initialize generation parameters
        self.temperature = temperature
        self.token_limit = token_limit 
        self.system_prompt = system_prompt
    
    def extract_context(self, prompt: str) -> str:
        """
        Extract relevant context from the vector store based on the prompt.

        Args:
            prompt: The user's input prompt to search for context

        Returns:
            A string containing relevant context chunks, or empty string if none found
        """
        try:
            results = self.vector_store.query(prompt, top_k=7)
            
            if not results:
                return ""
            
            # Extract text from metadata
            context_parts = []
            for result in results:
                if 'metadata' in result and 'text' in result['metadata']:
                    context_parts.append(result['metadata']['text'])
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"Warning: Vector DB query failed: {e}")
            return ""

    def _ingest_context_async(self, context: str) -> None:
        """
        Ingest context into the vector store asynchronously.
        
        Args:
            context: The context data to ingest
        """
        if not context or not isinstance(context, str):
            return
            
        try:
            def ingest_worker():
                try:
                    self.vector_store.upsert_texts([context])
                    print(f"✅ Context ingested asynchronously: {context[:50]}...")
                except Exception as e:
                    print(f"❌ Error ingesting context asynchronously: {e}")
            
            # Start ingestion in background thread
            thread = threading.Thread(target=ingest_worker, daemon=True)
            thread.start()
            
        except Exception as e:
            print(f"Error starting async context ingestion: {e}")

    def ingest_context(self, context: str) -> None:
        """
        Ingest context into the vector store (non-blocking).

        Args:
            context: The context data to ingest
        """
        self._ingest_context_async(context)

    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Generate a text response from the LLM.

        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")
    
    def _get_api_key(self, api_key_name: str) -> str:
        """
        Get the API key from environment variables.

        Args:
            api_key_name: Name of the environment variable containing the API key.

        Returns:
            The API key value, or empty string if not found.
        """
        return os.getenv(api_key_name, "")