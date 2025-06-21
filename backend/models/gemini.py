from .llm import BaseLLM

import google.generativeai as genai

class Gemini(BaseLLM):
    def __init__(self, model_name: str, temperature: float = 0.5, token_limit: int = 1000, system_prompt: str = ""):
        super().__init__(model_name, temperature, token_limit, system_prompt)
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Get the model
        self.model = genai.GenerativeModel(self.model_name)

    def extract_context(self, prompt: str) -> str:
        # For now, return empty string - you can implement vector search later
        return ""

    def ingest_context(self, context_id: str, context: str) -> None:
        # For now, do nothing - you can implement context storage later
        return ""
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Gemini model.
        
        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        try:
            # Create generation config
            generation_config = genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.token_limit,
            )
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"

