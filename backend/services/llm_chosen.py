from models import GPT, Gemini, DeepSeek, Claude, Hume

def llm_response(llm_name: str, prompt: str, context: str):
    llm = GPT(llm_name)
    return llm.generate_text(prompt)