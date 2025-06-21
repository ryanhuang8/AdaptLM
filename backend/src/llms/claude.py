from .llm import BaseLLM

class Claude(BaseLLM):
    def __init__(self, model_name: str):
        super().__init__(model_name)

    def extract_context(self, prompt: str) -> str:
        pass

    def ingest_context(self, context_id: str, context: str) -> None:
        pass    
    
    def generate_text(self, prompt: str) -> str:
        pass