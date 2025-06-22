"""
Index Manager for Pinecone using the new API
"""

import os
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, PodSpec

load_dotenv()

class IndexManager:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        self.pc = Pinecone(api_key=self.api_key)

    def list_indexes(self) -> List[Dict[str, Any]]:
        try:
            indexes = []
            for idx in self.pc.list_indexes():
                index_info = {
                    "name": idx.name,
                    "dimension": idx.dimension,
                    "metric": idx.metric,
                    "status": idx.status,
                    "host": idx.host,
                    "created_at": idx.created_at
                }
                indexes.append(index_info)
            return indexes
        except Exception as e:
            raise Exception(f"Failed to list indexes: {e}")

    def create_index(self, name: str, metric: str = "cosine",
                     serverless: bool = True, cloud: str = "aws", region: str = "us-east-1",
                     pod_type: Optional[str] = None, pods: Optional[int] = None,
                     model_name: str = "all-MiniLM-L6-v2") -> bool:
        try:
            # Auto-detect dimension from embedding model if not specified
            from .embeddings import EmbeddingManager
            embedding_manager = EmbeddingManager(model_name=model_name)
            dimension = embedding_manager.dimension
            print(f"Auto-detected dimension: {dimension} (from model: {model_name})")
            
            if serverless:
                spec = ServerlessSpec(cloud=cloud, region=region)
            else:
                spec = PodSpec(pod_type=pod_type or "p1.x1", pods=pods or 1)
            
            self.pc.create_index(
                name=name, 
                dimension=dimension, 
                metric=metric, 
                spec=spec
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to create index: {e}")

    def delete_index(self, name: str) -> bool:
        try:
            self.pc.delete_index(name)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete index: {e}")

    def describe_index(self, name: str) -> Dict[str, Any]:
        try:
            idx = self.pc.describe_index(name)
            return {
                "name": idx.name,
                "dimension": idx.dimension,
                "metric": idx.metric,
                "status": idx.status,
                "host": idx.host,
                "created_at": idx.created_at
            }
        except Exception as e:
            raise Exception(f"Failed to describe index: {e}")

    def wait_for_ready(self, name: str, timeout: int = 300) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            try:
                status = self.describe_index(name)["status"]
                print(f"Current status for '{name}': {status} (type: {type(status)})")
                
                # Handle Pinecone IndexModelStatus object
                if hasattr(status, 'ready') and status.ready:
                    print(f"Index '{name}' is ready!")
                    return True
                elif hasattr(status, 'state') and status.state == "Ready":
                    print(f"Index '{name}' is ready!")
                    return True
                
                print(f"Waiting for index '{name}' to be ready. Current status: {status}")
                time.sleep(10)
            except Exception as e:
                print(f"Error checking index status: {e}")
                time.sleep(10)
        print(f"Timeout reached for index '{name}'")
        return False

    def index_stats(self, name: str) -> Dict[str, Any]:
        try:
            index = self.pc.Index(name)
            stats = index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            raise Exception(f"Failed to get index stats: {e}")

    def get_index(self, name: str):
        """Get a Pinecone index instance."""
        try:
            return self.pc.Index(name)
        except Exception as e:
            raise Exception(f"Failed to get index '{name}': {e}")

    def index_exists(self, name: str) -> bool:
        """Check if an index exists."""
        try:
            return name in [idx.name for idx in self.pc.list_indexes()]
        except Exception as e:
            raise Exception(f"Failed to check if index exists: {e}")
        

