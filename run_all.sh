#!/bin/bash
# Quick Start - Run all parsers in sequence

echo "🚀 Privacy Report - Quick Start"
echo "================================"
echo ""

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Run: source .venv/Scripts/activate"
    exit 1
fi

echo "✅ Virtual environment active"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Create .env and add: GEMINI_API_KEY=your-key-here"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Run parsers in sequence
echo "📸 Step 1: Parsing Instagram data..."
python parsers/instagram_parser.py
echo ""

echo "🔍 Step 2: Parsing Google data..."
python parsers/google_parser.py
echo ""

echo "🧠 Step 3: Generating demo AI data (replace with real data later)..."
python generate_demo_data.py
echo ""

echo "⚙️  Step 4: Building feature matrix..."
python parsers/feature_engineering.py
echo ""

echo "🔗 Step 5: Finding surveillance connections..."
python parsers/gemini_embeddings.py
echo ""

echo "================================"
echo "✅ ALL DONE!"
echo ""
echo "Check output/ folder for results:"
echo "  - instagram_data.json"
echo "  - google_data.json"
echo "  - ai_data.json"
echo "  - user_feature_matrix.json"
echo "  - embeddings.json"
echo ""
echo "🎯 Next: Build Layer 3 (Knowledge Graph)"
