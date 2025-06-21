#!/usr/bin/env python3
"""
Simple example of using the ContextLLM system.
"""

from src.llms.gpt import GPT

def main():
    print("=== ContextLLM Example ===\n")
    
    try:
        # Initialize GPT
        print("1. Initializing GPT...")
        gpt = GPT("gpt")
        print(f"✅ GPT initialized with model: {gpt.model_name}")
        
        # Generate some text
        print("\n2. Generating text...")
        prompts = [
            "What is the capital of France?",
            "Explain quantum computing in simple terms",
            "Write a short poem about AI"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n   Prompt {i}: {prompt}")
            response = gpt.generate_text(prompt)
            print(f"   Response: {response[:100]}..." if len(response) > 100 else f"   Response: {response}")
        
        # Test context methods
        print("\n3. Testing context methods...")
        context_id = gpt.extract_context("test prompt")
        print(f"   Extracted context ID: {context_id}")
        
        gpt.ingest_context("test_id", "This is some test context")
        print("   ✅ Context ingested successfully")
        
        print("\n🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Installed all dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 