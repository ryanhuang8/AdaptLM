from .llm import BaseLLM

from openai import OpenAI
from prompts import get_prompt_for_model
from vector_store.vector_store import PineconeVectorStore

class GPT(BaseLLM):
    def __init__(self, model_name: str, user_id: str, vector_store: PineconeVectorStore):
        super().__init__(model_name, 
                         system_prompt=get_prompt_for_model(model_name), 
                         user_id=user_id,
                         vector_store=vector_store
                         )
        print("DEBUGGING PURPOSES ONLY: GPT API KEY: ", self.api_key)
        
        self.client = OpenAI(api_key=self.api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the GPT model.

        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        try:
            # Store user input for later ingestion
            self.store_user_input(prompt)
            
            # EXTRACT CONTEXT
            # NOTE: identify the number of chunks to return
            context = self.extract_context(prompt)
            if context:
                prompt = f"Given the following context, answer the question: {context}\n\n{prompt}"

            response = self.client.chat.completions.create(
                model=self.model_name,
                max_tokens=self.token_limit,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Get the response text
            response_text = response.choices[0].message.content or "No response generated"

            # INGEST CONTEXT (non-blocking, includes both response and conversation pair)
            self.ingest_context(response_text)
            
            return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
