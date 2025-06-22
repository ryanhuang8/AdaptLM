from .llm import BaseLLM
from prompts import get_prompt_for_model
from vector_store import PineconeVectorStore

import asyncio
import os
from hume import AsyncHumeClient
from hume.empathic_voice.chat.socket_client import ChatConnectOptions

class Hume(BaseLLM):
    def __init__(self, model_name: str, user_id: str, vector_store: PineconeVectorStore, previous_prompt: str = None, previous_output: str = None):
        super().__init__(model_name, 
                         system_prompt=get_prompt_for_model(model_name), 
                         user_id=user_id,
                         vector_store=vector_store)
        
        self.secret_key = os.getenv("HUME_SECRET_KEY", "")
        self.config_id = os.getenv("HUME_CONFIG_ID", "")
        self.client = AsyncHumeClient(api_key=self.api_key)
        self.previous_prompt = previous_prompt
        self.previous_output = previous_output

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Hume model.

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

            # Run the async function in a new event loop
            response_text = asyncio.run(self._generate_text_async(prompt))
            
            # Store the current output as previous output for next query
            self.previous_output = response_text
            self.previous_prompt = original_prompt  # Store original prompt, not enhanced one
            
            # Ingest the conversation pair (original prompt + response)
            conversation_pair = f"User: {original_prompt}\nAssistant: {response_text}"
            self.ingest_context(conversation_pair)

            return response_text
            
        except Exception as e:
            return f"Error: {str(e)}"

    async def _generate_text_async(self, prompt: str) -> str:
        """
        Async method to handle Hume API calls.
        """
        try:
            response_text = ""
            
            async def handle_response(response):
                nonlocal response_text
                text = response["message"]["text"]
                response_text = text
            
            full_prompt = f"{self.system_prompt}\n{prompt}"
            
            async with self.client.empathic_voice.chat.connect_with_callbacks(
                options=ChatConnectOptions(config_id=self.config_id),
                on_response=handle_response
            ) as socket:
                await socket.send_text(full_prompt)
                # Wait a bit for response to be processed
                await asyncio.sleep(1)
            
            return response_text if response_text else "No response received from Hume"
            
        except Exception as e:
            return f"Error in async generation: {str(e)}"