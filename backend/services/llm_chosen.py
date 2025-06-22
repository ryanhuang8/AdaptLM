from models import GPT, Gemini, Claude, Hume
from vector_store import PineconeVectorStore

def llm_response(llm_name: str, uid: str, vector_store: PineconeVectorStore, prompt: str, previous_prompt: str, previous_output: str):
    if llm_name == "gpt":
        llm = GPT(llm_name, uid, vector_store, previous_prompt, previous_output)
    elif llm_name == "gemini":
        llm = Gemini(llm_name, uid, vector_store, previous_prompt, previous_output)
    elif llm_name == "claude":
        llm = Claude(llm_name, uid, vector_store, previous_prompt, previous_output)
    # elif llm_name == "hume":
    #     llm = Hume(llm_name, uid, vector_store, previous_prompt, previous_output)
    else:
        raise ValueError(f"Invalid LLM name: {llm_name}")
    return llm.generate_text(prompt)