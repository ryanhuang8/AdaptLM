from .llm import BaseLLM

from anthropic import Anthropic
from prompts import get_prompt_for_model
from vector_store import PineconeVectorStore

class Claude(BaseLLM):
    def __init__(self, model_name: str, user_id: str, vector_store: PineconeVectorStore, previous_prompt: str = None, previous_output: str = None):
        super().__init__(model_name, 
                         system_prompt=get_prompt_for_model(model_name), 
                         user_id=user_id,
                         vector_store=vector_store)

        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.api_key)
        self.previous_prompt = previous_prompt
        self.previous_output = previous_output
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Claude model.
        
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

            # Get the response text
            response_text = response.content[0].text
            
            # Store the current output as previous output for next query
            self.previous_output = response_text
            self.previous_prompt = original_prompt  # Store original prompt, not enhanced one
            
            # Ingest the conversation pair (original prompt + response)
            conversation_pair = f"User: {original_prompt}\nAssistant: {response_text}"
            self.ingest_context(conversation_pair)

            return response_text
            
        except Exception as e:
            return f"Error: {str(e)}"