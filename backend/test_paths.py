#!/usr/bin/env python3
"""
Test script to check system paths and current working directory.
Converted from Jupyter notebook cell.
"""

import sys
import os

class Config:
    def __init__(self, test_paths: bool = True, test_models: bool = True):
        self.test_paths = test_paths
        self.test_models = test_models

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

if __name__ == "__main__":
    config = Config(
        test_paths=True,
        test_models=True
    )
    main(config) 