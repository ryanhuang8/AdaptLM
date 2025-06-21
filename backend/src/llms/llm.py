from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseLLM(ABC):
    """
    Base class for LLM implementations.
    """

    def __init__(self, model_name: str):
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
            "claude": "claude-3-5-sonnet-20240620"
        }

        model_api_key_dict = {
            "gpt": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "hume": "HUME_API_KEY",
            "claude": "CLAUDE_API_KEY"
        }

        # initialize model name, api key name, and api key
        self.model_name = model_dict[model_name]
        self.model_api_key_name = model_api_key_dict[model_name]
        self.api_key = self._get_api_key(self.model_api_key_name)
        
        if not self.api_key:
            raise ValueError(f"API key not found for {model_name}. Please set {self.model_api_key_name} environment variable.")

    @abstractmethod
    def extract_context(self, prompt: str) -> str:
        """
        Extract relevant context from the prompt through a vector database.

        Args:
            prompt: The user's input prompt.

        Returns:
            A string representing the ID of the relevant context chunks.
            If no context is found, return an empty string.
        """
        pass

    @abstractmethod
    def ingest_context(self, context_id: str, context: str) -> None:
        """
        Ingest context into the LLM or a backing store.

        Args:
            context_id: The ID of the context.
            context: The context data to ingest.
        """
        pass

    @abstractmethod
    def generate_text(self, prompt: str, conversation_id: Optional[str] = None) -> str:
        """
        Generate a text response from the LLM.

        Args:
            prompt: The user's input prompt.
            conversation_id: Optional conversation ID for tracking and context.

        Returns:
            The generated text response.
        """
        pass

    def _get_api_key(self, api_key_name: str) -> str:
        """
        Get the API key from the environment variables.
        """
        return os.getenv(api_key_name, "")