"""
Prompts package for ContextLLM.
This package contains system prompts for different LLM models and use cases.
"""

# Import all prompts from the default module
from .default import (
    SYSTEM_PROMPT,
    CODING_PROMPT,
    CREATIVE_PROMPT,
    ANALYTICAL_PROMPT,
    GPT_PROMPT,
    CLAUDE_PROMPT,
    DEEPSEEK_PROMPT,
    GEMINI_PROMPT,
    HUME_PROMPT
)

# Define what gets imported when someone does "from prompts import *"
__all__ = [
    'SYSTEM_PROMPT',
    'CODING_PROMPT',
    'CREATIVE_PROMPT',
    'ANALYTICAL_PROMPT',
    'GPT_PROMPT',
    'CLAUDE_PROMPT',
    'DEEPSEEK_PROMPT',
    'GEMINI_PROMPT',
    'HUME_PROMPT'
]

# You can also add convenience functions here
def get_prompt_for_model(model_name: str) -> str:
    """
    Get the default system prompt for a specific model.
    
    Args:
        model_name: The name of the model (gpt, claude, deepseek, gemini, hume)
    
    Returns:
        The appropriate system prompt for the model
    """
    prompt_map = {
        "gpt": GPT_PROMPT,
        "claude": CLAUDE_PROMPT,
        "deepseek": DEEPSEEK_PROMPT,
        "gemini": GEMINI_PROMPT,
        "hume": HUME_PROMPT
    }
    
    return prompt_map.get(model_name.lower(), SYSTEM_PROMPT)

def get_prompt_for_use_case(use_case: str) -> str:
    """
    Get a specialized prompt for a specific use case.
    
    Args:
        use_case: The use case (coding, creative, analytical)
    
    Returns:
        The appropriate specialized prompt
    """
    prompt_map = {
        "coding": CODING_PROMPT,
        "creative": CREATIVE_PROMPT,
        "analytical": ANALYTICAL_PROMPT
    }
    
    return prompt_map.get(use_case.lower(), SYSTEM_PROMPT)
