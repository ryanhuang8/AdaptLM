import os
import sys
from anthropic import Anthropic

class Claude(BaseLLM):
    def __init__(self, model_name: str, temperature: float = 0.5, token_limit: int = 1000, system_prompt: str = ""):
        super().__init__(model_name, temperature, token_limit, system_prompt)
        
        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.api_key)

    def extract_context(self, prompt: str) -> str:
        # For now, return empty string - you can implement vector search later
        return ""

    def ingest_context(self, context_id: str, context: str) -> None:
        # For now, do nothing - you can implement context storage later
        return "" 
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Claude model.
        
        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=self.token_limit,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text
            
        except Exception as e:
            return f"Error: {str(e)}"

# Test the class when run directly
if __name__ == "__main__":
    # Simple test
    try:
        claude = Claude("claude")
        print(f"✅ Claude initialized with model: {claude.model_name}")
        
        response = claude.generate_text("Hello! How are you?")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure ANTHROPIC_API_KEY is set in your environment variables.")
