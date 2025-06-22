import os
import json
from openai import OpenAI
from .vellum_scraper import run_vellum_scraper

class ModelRouter:
    SYSTEM_PROMPT = """
You are an expert at classifying user queries into the most appropriate task categories for LLM selection.

You should output ONLY one of the following (without explanation):
- "gpt" 
- "gemini"
- "claude"
- "groq"

Selection rules:
- gpt: use for general purpose queries, math, or when broad knowledge is needed
- claude: use for code-related queries
- groq: use for speed or when a low-latency response is preferred
- gemini: use for reasoning-heavy or complex thought tasks

Examples:
user: what is 123 + 456?
output: gpt

user: write me a python function to sort a list
output: claude

user: give me a quick summary of the news
output: groq

user: solve this logic puzzle for me
output: gemini

user: what is two plus two?
output: gpt
    """
    def __init__(self):
        # Get the directory where this file is located and construct the path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(current_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")
        
        self.classifier_path = os.path.join(data_dir, "vellum_leaderboard_data.json")
        if not os.path.exists(self.classifier_path):
            run_vellum_scraper(self.classifier_path)
        
        with open(self.classifier_path, "r") as f:
            data = json.load(f)
            model_categories = data["task_categories"]
        
        self.model_categories = self.preprocess_model_categories(model_categories)
        self.categories = list(self.model_categories.keys())
        
        # Initialize OpenAI client for LLM-based classification
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required for LLM-based classification")
        self.client = OpenAI(api_key=api_key)
        
        # Classification prompt template
        self.classification_prompt = self._create_classification_prompt()
        self.system_prompt = self.SYSTEM_PROMPT

    def _create_classification_prompt(self) -> str:
        """Create the classification prompt for the LLM"""
        categories_text = "\n".join([f"- {category}" for category in self.categories])
        
        return f"""You are an expert at classifying user queries into the most appropriate task categories for LLM selection.
            Available task categories:
            {categories_text}

            Your task is to analyze the user's query and select the SINGLE most appropriate category from the list above. Consider the intent, complexity, and nature of the query.

            Respond with ONLY the exact category name from the list above, nothing else. Do not add explanations, quotes, or any other text.

            Examples:
            - Query: "What is the capital of France?" → "Best in General Knowledge"
            - Query: "Write a Python function to sort a list" → "Best in Code Generation"
            - Query: "Analyze this dataset and create visualizations" → "Best in Data Analysis"
            - Query: "Help me write a creative story about a robot" → "Best in Creative Writing"
            - Query: "What are the latest developments in AI?" → "Best in Research and Analysis"

            User query: """

    def preprocess_model_categories(self, model_categories: dict) -> dict:
        """
        Convert Vellum leaderboard data to category_to_model_family mapping.
        Analyzes the top models in each category to determine the dominant model family.
        """
        category_to_model_family = {}
        
        # Define model family patterns
        model_family_patterns = {
            "gemini": ["gemini", "google"],
            "gpt": ["gpt", "openai", "o3", "o4"],
            "claude": ["claude", "anthropic"],
            "groq": ["groq", "llama"]
        }
        
        for category, models in model_categories.items():
            # Count model families in this category
            model_family = None
            
            for model in models:
                model_lower = model.lower()
                for family, patterns in model_family_patterns.items():
                    if any(pattern in model_lower for pattern in patterns):
                        model_family = family
                        break
            
            # Determine the dominant model family
            if model_family:
                category_to_model_family[category] = model_family
            else:
                # Default to gemini if no clear pattern
                category_to_model_family[category] = "gemini"
        return category_to_model_family

    def classify(self, prompt: str) -> str:
        """
        Classify a prompt using LLM-based classification.
        
        Args:
            prompt: The user's input prompt to classify
            
        Returns:
            The selected LLM model family (gpt, gemini, claude, groq)
        """
        try:
            # Create the full classification prompt
            full_prompt = prompt
            
            # Get classification from LLM
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                max_tokens=50,
                temperature=0.001  # Low temperature for consistent classification
            )

            appointment_keywords = [
            'appointment', 'schedule', 'booking', 'meeting', 'calendar',
            'reserve', 'book', 'arrange', 'set up', 'organize',
            'tomorrow', 'next week', 'this week', 'today at',
            '2 pm', '3 pm', '4 pm', '5 pm', 'morning', 'afternoon', 'evening'
            ]
            if any(keyword in prompt.lower() for keyword in appointment_keywords):
                return "gpt"
            
            # Keywords that trigger email routing
            email_keywords = [
                'email', 'send email', 'mail'
            ]
            if any(keyword in prompt.lower() for keyword in email_keywords):
                return "gpt"
            # Extract the classified category
            response_content = response.choices[0].message.content
            if response_content is None:
                print("Warning: LLM returned empty response, using fallback")
                return "gpt"
            
            classified_model = response_content.strip()
            print(f"LLM classified prompt as: {classified_model}")
            
            # Map the category to model family
            if classified_model in self.model_categories.values():
                print(f"LLM classified prompt as: {classified_model}")
                return classified_model
            else:
                # Fallback if classification doesn't match any category
                print(f"Warning: LLM returned unknown category '{classified_model}', using fallback")
                return "gpt"  # Default fallback
                
        except Exception as e:
            print(f"Error in LLM classification: {e}")
            return "gpt"  # Fallback to GPT on error