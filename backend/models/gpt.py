from .llm import BaseLLM

from openai import OpenAI
from prompts import get_prompt_for_model

class GPT(BaseLLM):
    def __init__(self, model_name: str):
        # NOTE: self.system_prompt is default
        super().__init__(model_name, system_prompt=get_prompt_for_model(model_name))

        print("DEBUGGING PURPOSES ONLY: GPT API KEY: ", self.api_key)
        
        self.client = OpenAI(api_key=self.api_key)

    def extract_context(self, prompt: str) -> str:
        # For now, return empty string - you can implement vector search later
        return ""

    def ingest_context(self, context_id: str, context: str) -> str:
        # For now, do nothing - you can implement context storage later
        return ""

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the GPT model.

        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                max_tokens=self.token_limit,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            # NOTE: should probably view the repsonse object
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error: {str(e)}"
    
