from .llm import BaseLLM

from anthropic import Anthropic
from prompts import get_prompt_for_model
from vector_store.vector_store import PineconeVectorStore

class Claude(BaseLLM):
    def __init__(self, model_name: str, user_id: str, vector_store: PineconeVectorStore):
        super().__init__(model_name, 
                         system_prompt=get_prompt_for_model(model_name), 
                         user_id=user_id,
                         vector_store=vector_store
                         )
        print("DEBUGGING PURPOSES ONLY: Claude API KEY: ", self.api_key)

        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.api_key)
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Claude model.
        
        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        try:
            # EXTRACT CONTEXT
            # NOTE: identify the number of chunks to return
            context = self.extract_context(prompt)
            if context:
                prompt = f"Given the following context and previous message, answer the question: {context}\n\n{self.previous_message}\n\n{prompt}"

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

            # INGEST CONTEXT
            self.ingest_context(response.content[0].text)

            return response.content[0].text
            
        except Exception as e:
            return f"Error: {str(e)}"