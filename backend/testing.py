#!/usr/bin/env python3
"""
Test script to check system paths and current working directory.
Converted from Jupyter notebook cell.
"""

import sys
import os
import time

class Config:
    def __init__(self, test_paths: bool = True, 
                 test_models: bool = True,
                 test_embeddings: bool = True,
                 test_index_manager: bool = True,
                 test_pinecone: bool = True):
        self.test_paths = test_paths
        self.test_models = test_models
        self.test_embeddings = test_embeddings
        self.test_index_manager = test_index_manager
        self.test_pinecone = test_pinecone

def test_paths():
    """Test and display system paths and current working directory."""
    print("=== System Paths and Directory Test ===\n")
    
    # Check system paths
    print("1. System Paths:")
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    
    # Check current working directory
    print(f"\n2. Current Working Directory:")
    print(f"   {os.getcwd()}")
    
    # Check if we're in a virtual environment
    print(f"\n3. Virtual Environment Status:")
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"   Virtual environment active: {in_venv}")
    
    if in_venv:
        print(f"   Virtual environment path: {sys.prefix}")
    
    # Check environment variables
    print(f"\n4. Environment Variables:")
    venv_path = os.getenv('VIRTUAL_ENV')
    if venv_path:
        print(f"   VIRTUAL_ENV: {venv_path}")
    else:
        print(f"   VIRTUAL_ENV: Not set")
    

def test_models(model_name: str):
    from models import GPT, Gemini, DeepSeek, Claude, Hume
    print("=== Model Test ===\n")

    model_options = {
        "gpt": GPT(model_name),
        "gemini": Gemini(model_name),
        "deepseek": DeepSeek(model_name),
        "claude": Claude(model_name),
        "hume": Hume(model_name)
    }

    model = model_options[model_name]
    response = model.generate_text(prompt="What is the capital of France?")
    print(f"Model: {model_name}, Response: {response}")

def test_embeddings():
    from vector_store import EmbeddingManager
    print("=== Embedding Test ===\n")
    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.embed_texts(["Hello, world!", "This is a test."])
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {len(embeddings[0])}")
    print(f"First embedding (first 5 values): {embeddings[0][:5]}")


def test_index_manager():
    # Import from the local vector_store folder
    from vector_store import IndexManager
    print("=== Index Manager Test ===\n")
    
    test_index_name = "test-index-manager"
    
    try:
        index_manager = IndexManager()
        
        # 1. List indexes
        print("1. Listing indexes...")
        indexes = index_manager.list_indexes()
        print(f"Found {len(indexes)} indexes:")
        for idx in indexes:
            print(f"  - {idx['name']} (Status: {idx['status']})")

        # 2. Create a test index
        print(f"\n2. Creating test index '{test_index_name}'...")
        if not index_manager.index_exists(test_index_name):
            created = index_manager.create_index(
                name=test_index_name,
                dimension=768,
                metric="cosine",
                serverless=True,
                cloud="aws",
                region="us-east-1"
            )
            print(f"Test index created: {created}")
        else:
            print(f"Test index '{test_index_name}' already exists.")

        # 3. Wait for index to be ready
        print(f"\n3. Waiting for index '{test_index_name}' to be ready...")
        ready = index_manager.wait_for_ready(test_index_name, timeout=60)
        print(f"Index ready: {ready}")
        
        if not ready:
            print("❌ Index did not become ready, skipping remaining tests")
            return

        # 4. Describe the index
        print(f"\n4. Describing index '{test_index_name}'...")
        desc = index_manager.describe_index(test_index_name)
        print(f"Description: {desc}")

        # 5. Get index stats
        print(f"\n5. Getting stats for index '{test_index_name}'...")
        stats = index_manager.index_stats(test_index_name)
        print(f"Stats: {stats}")

        # 6. Get index instance
        print(f"\n6. Getting index instance for '{test_index_name}'...")
        idx_instance = index_manager.get_index(test_index_name)
        print(f"Index instance: {idx_instance}")

        # 7. Check index existence
        print(f"\n7. Checking if index '{test_index_name}' exists...")
        exists = index_manager.index_exists(test_index_name)
        print(f"Index exists: {exists}")

        # 8. Delete the test index
        print(f"\n8. Deleting test index '{test_index_name}'...")
        deleted = index_manager.delete_index(test_index_name)
        print(f"Test index deleted: {deleted}")

        print("\n🎉 Index Manager comprehensive test completed!\n")
        
    except Exception as e:
        print(f"❌ Error with Index Manager: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to clean up the test index if it exists
        try:
            if 'index_manager' in locals() and index_manager.index_exists(test_index_name):
                print(f"Cleaning up test index '{test_index_name}'...")
                index_manager.delete_index(test_index_name)
        except:
            pass

def test_pinecone():
    # Import from the local vector_store folder
    from vector_store import PineconeVectorStore
    print("=== Pinecone Vector Store Test ===\n")
    
    test_index_name = "test-vector-store"
    
    try:
        # Initialize vector store
        print("1. Initializing Pinecone Vector Store...")
        vector_store = PineconeVectorStore(index_name=test_index_name)
        print(f"✅ Vector Store initialized successfully!")
        print(f"   Index name: {vector_store.index_name}")
        print(f"   Dimension: {vector_store.dimension}")
        print(f"   Model: {vector_store.model_name}")

        # 2. Test upserting texts
        print(f"\n2. Testing upsert_texts...")
        test_texts = [
            "The quick brown fox jumps over the lazy dog",
            "Machine learning is a subset of artificial intelligence",
            "Python is a popular programming language for data science",
            "Vector databases store high-dimensional data efficiently",
            "Natural language processing helps computers understand human language"
        ]
        
        vector_ids = vector_store.upsert_texts(test_texts)
        print(f"✅ Upserted {len(vector_ids)} texts with IDs: {vector_ids[:3]}...")
        
        # Add a small delay to ensure vectors are indexed
        print("   Waiting for vectors to be indexed...")
        time.sleep(10)

        # 3. Test querying
        print(f"\n3. Testing query...")
        query_text = "What is machine learning?"
        results = vector_store.query(query_text, top_k=3)
        print(f"✅ Query results for '{query_text}':")
        if results:
            for i, result in enumerate(results):
                print(f"   {i+1}. Score: {result['score']:.4f}, Text: {result['metadata']['text'][:50]}...")
        else:
            print("   No results found - this might indicate an indexing issue")
            
        # Try a simpler query to debug
        print(f"\n3b. Testing simple query...")
        simple_results = vector_store.query("machine learning", top_k=5)
        print(f"✅ Simple query results: {len(simple_results)} results")
        for i, result in enumerate(simple_results):
            print(f"   {i+1}. Score: {result['score']:.4f}, Text: {result['metadata']['text'][:30]}...")

        # 4. Test get_stats
        print(f"\n4. Testing get_stats...")
        stats = vector_store.get_stats()
        print(f"✅ Index stats: {stats}")

        # 5. Test fetch
        print(f"\n5. Testing fetch...")
        if vector_ids:
            fetched_vectors = vector_store.fetch(vector_ids[:2])
            print(f"✅ Fetched {len(fetched_vectors)} vectors:")
            for i, vector in enumerate(fetched_vectors):
                print(f"   {i+1}. ID: {vector['id']}, Text: {vector['metadata']['text'][:30]}...")

        # 6. Test delete
        print(f"\n6. Testing delete...")
        if vector_ids:
            deleted = vector_store.delete(vector_ids[:1])
            print(f"✅ Deleted first vector: {deleted}")
            
            # Verify deletion
            remaining_stats = vector_store.get_stats()
            print(f"   Remaining vectors: {remaining_stats['total_vector_count']}")

        # 7. Clean up - delete the test index
        print(f"\n7. Cleaning up test index '{test_index_name}'...")
        from vector_store import IndexManager
        index_manager = IndexManager()
        if index_manager.index_exists(test_index_name):
            deleted = index_manager.delete_index(test_index_name)
            print(f"✅ Test index deleted: {deleted}")

        print("\n🎉 Pinecone Vector Store comprehensive test completed!\n")
        
    except Exception as e:
        print(f"❌ Error with Pinecone Vector Store: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to clean up the test index if it exists
        try:
            from vector_store import IndexManager
            index_manager = IndexManager()
            if index_manager.index_exists(test_index_name):
                print(f"Cleaning up test index '{test_index_name}'...")
                index_manager.delete_index(test_index_name)
        except:
            pass

def main(config: Config):
    """Main function to run the path test."""
    if config.test_paths:
        try:
            test_paths()
            print("\n🎉 Path test completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during path test: {e}")

    if config.test_models:
        try:
            test_models("gemini")
            print("\n🎉 Model test completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during model test: {e}")
    
    if config.test_embeddings:
        try:
            test_embeddings()
            print("\n🎉 Embedding test completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during embedding test: {e}")
    
    if config.test_index_manager:
        try:
            test_index_manager()
            print("\n🎉 Index Manager test completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during Index Manager test: {e}")
    
    if config.test_pinecone:
        try:
            test_pinecone()
            print("\n🎉 Pinecone test completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during Pinecone test: {e}")

if __name__ == "__main__":
    config = Config(
        test_paths=False,
        test_models=False,
        test_embeddings=False,
        test_index_manager=False,
        test_pinecone=True,
    )
    main(config) 