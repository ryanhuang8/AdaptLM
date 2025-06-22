from .llm import BaseLLM
from prompts import get_prompt_for_model

import asyncio
import os
from hume import AsyncHumeClient
from hume.empathic_voice.chat.socket_client import ChatConnectOptions

class Hume(BaseLLM):
    def __init__(self, model_name: str):
        # NOTE: self.system_prompt is default
        super().__init__(model_name, system_prompt=get_prompt_for_model(model_name))
        self.secret_key = os.getenv("HUME_SECRET_KEY", "")
        self.config_id = os.getenv("HUME_CONFIG_ID", "")
        
        self.client = AsyncHumeClient(api_key=self.api_key)

    def extract_context(self, prompt: str) -> str:
        # For now, return empty string - you can implement vector search later
        return ""

    def ingest_context(self, context_id: str, context: str) -> str:
        # For now, do nothing - you can implement context storage later
        return ""

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the Hume model.

        Args:
            prompt: The user's input prompt.

        Returns:
            The generated text response.
        """
        try:
            # Run the async function in a new event loop
            return asyncio.run(self._generate_text_async(prompt))
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
                print(f"AI: {text}")
            
            async with self.client.empathic_voice.chat.connect_with_callbacks(
                options=ChatConnectOptions(config_id=self.config_id),
                on_response=handle_response
            ) as socket:
                await socket.send_text(prompt)
                # Wait a bit for response to be processed
                await asyncio.sleep(2)
            
            return response_text if response_text else "No response received from Hume"
            
        except Exception as e:
            return f"Error in async generation: {str(e)}"