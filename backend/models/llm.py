# standard imports
import os 
import threading
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from typing import Optional

# custom imports
from vector_store.vector_store import PineconeVectorStore

# Load environment variables
load_dotenv()

class BaseLLM(ABC):
    """
    Base class for LLM implementations.
    """

    def __init__(self, model_name: str,
                temperature: float = 0.5, 
                token_limit: int = 1000,
                system_prompt: str = "",
                user_id: Optional[str] = None,
                vector_store: Optional[PineconeVectorStore] = None
                ):
        """
        Initialize the LLM.

        Args:
            model_name: The name of the model to use.
        """

        if model_name not in ["gpt", "deepseek", "gemini", "hume", "claude"]:
            raise ValueError(f"Model {model_name} not found, please only use gpt, deepseek, gemini, hume, or claude")
        
        # get model name and api key
        model_dict = {
            "gpt": "gpt-4o",
            "deepseek": "deepseek-chat",
            "gemini": "gemini-2.0-flash",
            "hume": "hume-voice",
            "claude": "claude-opus-4-20250514"
        }

        model_api_key_dict = {
            "gpt": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "hume": "HUME_API_KEY",
            "claude": "ANTHROPIC_API_KEY"
        }

        # initialize model name, api key name, and api key
        self.model_name = model_dict[model_name]
        self.model_api_key_name = model_api_key_dict[model_name]
        self.api_key = self._get_api_key(self.model_api_key_name)
        
        if not self.api_key:
            raise ValueError(f"API key not found for {model_name}. Please set {self.model_api_key_name} environment variable.")
        
        self.temperature = temperature
        self.token_limit = token_limit 
        self.system_prompt = system_prompt

        # get the user id
        if user_id is None:
            raise ValueError("User ID is required for this model.")
        self.user_id = user_id

        # get the vector store
        if vector_store is None:
            raise ValueError("Vector store is required for this model.")

        # Create a new vector store instance with user_id as index name
        self.vector_store = vector_store(index_name=user_id)
        
        # Cache for previous message to avoid vector DB bottleneck
        self.previous_message = None

    def extract_context(self, prompt: str) -> str:
        """
        Extract relevant context from the prompt through a vector database.

        Args:
            prompt: The user's input prompt.

        Returns:
            A string representing the relevant context chunks.
            If no context is found, return an empty string.
        """
        try:
            # First, check if we have a previous message that might be relevant
            context_parts = []
            
            # Add previous message if it exists and might be relevant
            if self.previous_message:
                context_parts.append(f"Previous conversation: {self.previous_message}")
            
            # Query the vector store for relevant context (non-blocking)
            try:
                results = self.vector_store.query(prompt, top_k=3)
                
                if results:
                    for result in results:
                        if 'metadata' in result and 'text' in result['metadata']:
                            context_parts.append(result['metadata']['text'])
            except Exception as e:
                print(f"Warning: Vector DB query failed, using only previous message: {e}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"Error extracting context: {e}")
            return ""

    def _ingest_context_async(self, context: str) -> None:
        """
        Ingest context into the vector store asynchronously (non-blocking).
        
        Args:
            context: The context data to ingest.
        """
        if context and isinstance(context, str):
            try:
                # Run ingestion in a separate thread to avoid blocking
                def ingest_worker():
                    try:
                        self.vector_store.upsert_texts([context])
                        print(f"   ✅ Context ingested asynchronously: {context[:50]}...")
                    except Exception as e:
                        print(f"   ❌ Error ingesting context asynchronously: {e}")
                
                # Start ingestion in background thread
                thread = threading.Thread(target=ingest_worker, daemon=True)
                thread.start()
                
            except Exception as e:
                print(f"Error starting async context ingestion: {e}")

    def ingest_context(self, context: str) -> None:
        """
        Ingest context into the LLM or a backing store (non-blocking).

        Args:
            context: The context data to ingest.
        """
        # Store in cache immediately for next query
        self.previous_message = context
        
        # Ingest the model's response asynchronously
        self._ingest_context_async(context)
        
        # If we have a user input, also store the conversation pair
        if self.last_user_input:
            conversation_pair = f"User: {self.last_user_input}\nAssistant: {context}"
            self._ingest_context_async(conversation_pair)
            
            # Clear the user input after storing
            self.last_user_input = None
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Generate a text response from the LLM.

        Args:
            prompt: The user's input prompt.
            conversation_id: Optional conversation ID for tracking and context.

        Returns:
            The generated text response.
        """
        raise NotImplementedError("This method is not implemented for this model.")
    
    def _get_api_key(self, api_key_name: str) -> str:
        """
        Get the API key from the environment variables.
        """
        return os.getenv(api_key_name, "")