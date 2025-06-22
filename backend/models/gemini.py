from .llm import BaseLLM

import google.generativeai as genai
from prompts import get_prompt_for_model
from vector_store import PineconeVectorStore

class Gemini(BaseLLM):
    def __init__(self, model_name: str, user_id: str, vector_store: PineconeVectorStore, previous_prompt: str = None, previous_output: str = None):
        super().__init__(model_name, 
                         system_prompt=get_prompt_for_model(model_name), 
                         user_id=user_id,
                         vector_store=vector_store)
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        self.previous_prompt = previous_prompt
        self.previous_output = previous_output

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Gemini model.
        
        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        if self.previous_prompt is None and self.previous_output is None:
            print("this is the first time we are generating text")
        
        try:
            # Store the original user prompt (before enhancement)
            original_prompt = prompt

            # EXTRACT CONTEXT
            # NOTE: identify the number of chunks to return
            context = self.extract_context(prompt)

            # context should include previous output and messages
            if self.previous_prompt:
                context = f"Previous prompt: {self.previous_prompt}\n\n{context}"
            if self.previous_output:
                context = f"Previous output: {self.previous_output}\n\n{context}"

            if context:
                prompt = f"Given the following context and previous message, answer the question: {context}\n\n{prompt}"

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.token_limit
                )
            )

            # Get the response text
            response_text = response.text
            
            # Store the current output as previous output for next query
            self.previous_output = response_text
            self.previous_prompt = original_prompt  # Store original prompt, not enhanced one
            
            # Ingest the conversation pair (original prompt + response)
            conversation_pair = f"User: {original_prompt}\nAssistant: {response_text}"
            self.ingest_context(conversation_pair)

            return response_text

            
        except Exception as e:
            return f"Error: {str(e)}"

