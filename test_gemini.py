"""
Quick test to verify Gemini API key is working
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("\n🔑 Get your FREE key at: https://aistudio.google.com/app/apikey")
    print("Then add to .env: GEMINI_API_KEY=your-key-here")
    exit(1)

print("✅ GEMINI_API_KEY found in .env")
print(f"   Key starts with: {GEMINI_API_KEY[:10]}...")

try:
    genai.configure(api_key=GEMINI_API_KEY)

    # Test embedding
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=["Test embedding"],
        task_type="retrieval_document"
    )

    print("✅ Gemini API connection successful!")
    print(f"   Embedding dimension: {len(result['embedding'][0])}")
    print("\n🚀 Ready to run: python parsers/gemini_embeddings.py")

except Exception as e:
    print(f"❌ Error connecting to Gemini API: {e}")
    print("\n🔑 Check your API key at: https://aistudio.google.com/app/apikey")
