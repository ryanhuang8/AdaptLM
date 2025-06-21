import os
from openai import OpenAI
from .llm import BaseLLM

class GPT(BaseLLM):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.client = OpenAI(api_key=self.api_key)

    def extract_context(self, prompt: str) -> str:
        # For now, return empty string - you can implement vector search later
        return ""

    def ingest_context(self, context_id: str, context: str) -> None:
        # For now, do nothing - you can implement context storage later
        pass

    def generate_text(self, prompt: str, conversation_id: str = "") -> str:
        """
        Generate text using the GPT model.

        Args:
            prompt: The user's input prompt.
            conversation_id: Optional conversation ID for context.

        Returns:
            The generated text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error: {str(e)}"
