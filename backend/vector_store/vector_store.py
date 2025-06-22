"""
Pinecone Vector Store implementation for ContextLLM using SentenceTransformers embeddings.
"""

import os
import uuid
import time
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from .embeddings import EmbeddingManager

load_dotenv()

class PineconeVectorStore:
    """
    Pinecone Vector Store for storing and retrieving embeddings using SentenceTransformers.
    """
    
    def __init__(self, index_name: str = "contextllm-index",
                model_name: str = "all-MiniLM-L6-v2",
                environment: str = "us-east-1", 
                cloud: str = "aws"
                ):
        """
        Initialize Pinecone Vector Store.
        If the index does not exist, it will be created.
        Args:
            index_name: Name of the Pinecone index
            dimension: Dimension of the embeddings (auto-detected from model if None)
            model_name: Name of the SentenceTransformer model to use
            environment: Environment of the Pinecone index
            cloud: Cloud provider of the Pinecone index
        """
        self.index_name = index_name
        self.model_name = model_name
        self.environment = environment
        self.cloud = cloud

        self.api_key = os.getenv("PINECONE_API_KEY")
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.api_key)
        
        # Initialize embedding manager first to get the actual dimension
        self.embedding_manager = EmbeddingManager(model_name=model_name)
        
        # NOTE: Not used right now
        self.dimension = self.embedding_manager.dimension

        # Use the embedding model's actual dimension if not specified
        self.dimension = self.embedding_manager.dimension
            
        print(f"Using dimension: {self.dimension} (from model: {model_name})")
        
        # Get or create index
        self.index = self._get_or_create_index()
    
    def _get_or_create_index(self):
        """Get existing index or create a new one."""
        try:
            # Check if index exists
            if self.index_name in [idx.name for idx in self.pc.list_indexes()]:
                return self.pc.Index(self.index_name)
            else:
                # Create new index
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud=self.cloud, region=self.environment)
                )
                # Wait for index to be ready
                print(f"Creating index '{self.index_name}' with dimension {self.dimension}...")
                time.sleep(5)  # Give it a moment to start
                return self.pc.Index(self.index_name)
        except Exception as e:
            raise Exception(f"Failed to initialize Pinecone index: {e}")
    
    def upsert_texts(self, texts: List[str], 
                    ids: Optional[List[str]] = None) -> List[str]:
        """
        Upsert texts into the vector store using SentenceTransformers embeddings.
        
        Args:
            texts: List of text strings to embed and store
            ids: Optional list of IDs for the vectors
            
        Returns:
            List of vector IDs
        """
        if not texts:
            return []
        
        print(f"   Generating embeddings for {len(texts)} texts...")
        # Generate embeddings using SentenceTransformers
        embeddings = self.embedding_manager.embed_texts(texts)
        print(f"   Generated {len(embeddings)} embeddings with dimension {len(embeddings[0])}")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        # Prepare vectors for upsert
        vectors = []
        for i, (embedding, vector_id) in enumerate(zip(embeddings, ids)):
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {"text": texts[i]}
            })
        
        print(f"   Upserting {len(vectors)} vectors to Pinecone...")
        # Upsert to Pinecone
        try:
            self.index.upsert(vectors=vectors)
            print(f"   Successfully upserted {len(vectors)} vectors")
            return ids
        except Exception as e:
            print(f"   Error upserting vectors: {e}")
            raise Exception(f"Failed to upsert vectors: {e}")
    
    def query(self, query_text: str, top_k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Query the vector store for similar texts using SentenceTransformers embeddings.
        
        Args:
            query_text: Text to search for
            top_k: Number of results to return
            filter_dict: Optional filter for metadata
            
        Returns:
            List of dictionaries containing id, score, and metadata
        """
        print(f"   Generating query embedding for: '{query_text}'")
        # Generate query embedding using SentenceTransformers
        query_embedding = self.embedding_manager.embed_texts([query_text])[0]
        print(f"   Query embedding dimension: {len(query_embedding)}")
        
        # Query Pinecone
        try:
            print(f"   Querying Pinecone with top_k={top_k}...")
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            print(f"   Pinecone returned {len(results.matches)} matches")
            
            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"   Error querying Pinecone: {e}")
            raise Exception(f"Failed to query vectors: {e}")
    
    def delete(self, ids: List[str]) -> bool:
        """
        Delete vectors by IDs.
        
        Args:
            ids: List of vector IDs to delete
            
        Returns:
            True if successful
        """
        try:
            self.index.delete(ids=ids)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete vectors: {e}")
    

    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get index statistics.
        
        Returns:
            Dictionary with index statistics
        """
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            raise Exception(f"Failed to get index stats: {e}")
    
    def fetch(self, ids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch vectors by IDs.
        
        Args:
            ids: List of vector IDs to fetch
            
        Returns:
            List of dictionaries containing id, values, and metadata
        """
        try:
            results = self.index.fetch(ids=ids)
            return [
                {
                    "id": vector_id,
                    "values": vector.values,
                    "metadata": vector.metadata
                }
                for vector_id, vector in results.vectors.items()
            ]
        except Exception as e:
            raise Exception(f"Failed to fetch vectors: {e}") 