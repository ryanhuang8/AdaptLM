#!/bin/bash

# ContextLLM Backend Installation Script
echo "🚀 Installing ContextLLM Backend Dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "contextllm_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv contextllm_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source contextllm_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install basic dependencies
echo "📚 Installing basic dependencies..."
pip install -r requirements.txt

# Create data directory for FAISS index
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir data
    echo "✅ Data directory created"
else
    echo "✅ Data directory already exists"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Create the .env file with your API keys"
    echo "2. Activate the virtual environment: source contextllm_env/bin/activate"
    echo "3. Run the server: python app.py"
    echo "4. Test the health endpoint: curl http://localhost:5000/health"
    echo ""
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi 