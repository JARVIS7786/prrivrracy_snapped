#!/bin/bash
# Setup script for Privacy Report project

echo "🚀 Setting up Privacy Report..."

# Activate virtual environment
source .venv/Scripts/activate

# Verify installation
echo "✅ Virtual environment activated"
python --version

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file..."
    cat > .env << EOF
OPENROUTER_API_KEY=your-openrouter-key-here
GEMINI_API_KEY=your-gemini-key-here
EOF
    echo "📝 Please edit .env and add your API keys"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your API keys to .env"
echo "2. Run: python parsers/instagram_parser.py"
echo "3. Run: python parsers/google_parser.py"
echo "4. Run: python parsers/ai_conversations_parser.py"
echo "5. Run: python parsers/feature_engineering.py"
echo "6. Run: python parsers/gemini_embeddings.py"
