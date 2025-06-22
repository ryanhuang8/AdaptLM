from .llm import BaseLLM

import google.generativeai as genai
from prompts import get_prompt_for_model
from vector_store.vector_store import PineconeVectorStore

class Gemini(BaseLLM):
    def __init__(self, model_name: str, user_id: str, vector_store: PineconeVectorStore):
        super().__init__(model_name, 
                         system_prompt=get_prompt_for_model(model_name), 
                         user_id=user_id,
                         vector_store=vector_store
                         )
        print("DEBUGGING PURPOSES ONLY: GEMINI API KEY: ", self.api_key)
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Gemini model.
        
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
                prompt = f"Given the following context, answer the question: {context}\n\n{prompt}"

            # Combine system prompt with user prompt
            full_prompt = f"{self.system_prompt}\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.token_limit
                )
            )

            # INGEST CONTEXT
            self.ingest_context(context)

            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"

