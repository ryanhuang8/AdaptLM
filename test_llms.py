#!/usr/bin/env python3
"""
Test script to verify all LLM imports work correctly.
"""

import os
import sys

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all LLM imports work correctly."""
    print("=== Testing LLM Imports ===\n")
    
    try:
        # Test GPT import
        print("1. Testing GPT import...")
        from llms.gpt import GPT
        print("✅ GPT imported successfully")
        
        # Test Claude import
        print("2. Testing Claude import...")
        from llms.claude import Claude
        print("✅ Claude imported successfully")
        
        # Test Gemini import
        print("3. Testing Gemini import...")
        from llms.gemini import Gemini
        print("✅ Gemini imported successfully")
        
        # Test DeepSeek import
        print("4. Testing DeepSeek import...")
        from llms.deepseek import DeepSeek
        print("✅ DeepSeek imported successfully")
        
        # Test Hume import
        print("5. Testing Hume import...")
        from llms.hume import Hume
        print("✅ Hume imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_initialization():
    """Test that LLMs can be initialized."""
    print("\n=== Testing LLM Initialization ===\n")
    
    try:
        from llms.gpt import GPT
        from llms.claude import Claude
        
        # Check environment variables
        api_keys = {
            "OPENAI_API_KEY": "OpenAI/GPT",
            "ANTHROPIC_API_KEY": "Anthropic/Claude"
        }
        
        for key, provider in api_keys.items():
            value = os.getenv(key)
            if value:
                print(f"✅ {provider} API key: SET")
            else:
                print(f"❌ {provider} API key: NOT SET")
        
        # Try to initialize GPT if API key is available
        if os.getenv("OPENAI_API_KEY"):
            print("\n1. Testing GPT initialization...")
            gpt = GPT("gpt")
            print(f"✅ GPT initialized with model: {gpt.model_name}")
        else:
            print("\n1. Skipping GPT test (no API key)")
        
        # Try to initialize Claude if API key is available
        if os.getenv("ANTHROPIC_API_KEY"):
            print("2. Testing Claude initialization...")
            claude = Claude("claude")
            print(f"✅ Claude initialized with model: {claude.model_name}")
        else:
            print("2. Skipping Claude test (no API key)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function."""
    print("ContextLLM Import and Initialization Test\n")
    
    # Test imports
    import_success = test_imports()
    
    if not import_success:
        print("\n❌ Import tests failed. Please check your setup.")
        return
    
    # Test initialization
    init_success = test_initialization()
    
    if init_success:
        print("\n🎉 All tests passed!")
        print("\nTo test text generation, make sure your API keys are set in the .env file:")
        print("- OPENAI_API_KEY for GPT")
        print("- ANTHROPIC_API_KEY for Claude")
        print("- GEMINI_API_KEY for Gemini")
    else:
        print("\n❌ Some tests failed. Please check your API keys and setup.")

if __name__ == "__main__":
    main() 