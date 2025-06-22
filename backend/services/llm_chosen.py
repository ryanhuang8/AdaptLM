from models import GPT, Gemini, DeepSeek, Claude, Hume
from vector_store import PineconeVectorStore

def llm_response(llm_name: str, prompt: str, context: str, previous_prompt: str, previous_output: str, vector_store: PineconeVectorStore):
    llm = GPT(llm_name, previous_prompt, previous_output, vector_store)
    return llm.generate_text(prompt, context, previous_prompt, previous_output)