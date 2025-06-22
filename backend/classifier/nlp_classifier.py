from sentence_transformers import SentenceTransformer, util
import torch
import os
from .vellum_scraper import run_vellum_scraper
import json
from pathlib import Path

class ModelRouter:
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
        self.model = None
        self.category_embeddings = torch.tensor([])
    

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
            # "llama": ["llama", "meta"],
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

    def initialize_model(self):
        self.model = SentenceTransformer("thenlper/gte-base")
        self.category_embeddings = torch.tensor(self.model.encode(self.categories, normalize_embeddings=True))
    
    def classify(self, prompt: str) -> str:
        if self.model is None:
            self.initialize_model()
        assert self.model is not None
        prompt_embedding = torch.tensor(self.model.encode([prompt], normalize_embeddings=True))
        
        # classify prompt
        print("Classifying prompt...")
        scores = util.dot_score(prompt_embedding, self.category_embeddings)[0]
        best_idx = scores.argmax()
        return self.model_categories[self.categories[best_idx]]