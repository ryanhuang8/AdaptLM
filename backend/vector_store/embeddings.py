"""
Embedding Manager for generating text embeddings using SentenceTransformers.
"""

from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    """
    Manages text embedding generation using a SentenceTransformer model.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize Embedding Manager with a SentenceTransformer model.

        Args:
            model_name: Name of the SentenceTransformer model to use
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded successfully. Vector dimension: {self.dimension}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return [vec.tolist() for vec in embeddings]
