"""
Ollama Embeddings - LOCAL, NO API LIMITS!
Finds hidden cross-platform surveillance connections
"""
import os
import sys
import requests
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parsers.utils import load_json, save_json

def get_embeddings_ollama(texts, model="nomic-embed-text"):
    """Get embeddings from local Ollama"""
    embeddings = []

    print(f"   Using Ollama model: {model}")
    for i, text in enumerate(texts):
        if (i + 1) % 10 == 0:
            print(f"   Processed {i + 1}/{len(texts)} items...")

        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": model, "prompt": text}
        )

        if response.status_code == 200:
            embeddings.append(response.json()["embedding"])
        else:
            print(f"   ⚠️ Error on item {i+1}: {response.text}")
            embeddings.append([0] * 768)  # Fallback

    return embeddings

def cosine_similarity(vec1, vec2):
    """Calculate similarity between two vectors"""
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def prepare_data():
    """Load and prepare data for embedding"""
    ig = load_json("output/instagram_data.json")
    google = load_json("output/google_data.json")
    ai = load_json("output/ai_data.json")

    items = []

    # Instagram searches - ALL (no limits!)
    for s in ig.get('recent_searches', [])[:50]:  # Start with 50
        items.append({
            "text": s['query'],
            "source": "Instagram",
            "category": "search"
        })

    # YouTube videos - ALL
    for v in google.get('youtube_watched', [])[:50]:  # Start with 50
        items.append({
            "text": v['value'],
            "source": "YouTube",
            "category": "video"
        })

    # Google searches
    for s in google.get('google_searches', []):
        items.append({
            "text": s['value'],
            "source": "Google",
            "category": "search"
        })

    # AI projects (with anxiety markers)
    for f in ai.get('gemini_files', []):
        if f.get('anxiety_markers'):
            items.append({
                "text": f['file'],
                "source": "Gemini",
                "category": "project",
                "markers": f['anxiety_markers']
            })

    # Advertisers
    for ad in ig.get('advertisers_sample', [])[:20]:  # Start with 20
        items.append({
            "text": ad,
            "source": "Instagram Ads",
            "category": "advertiser"
        })

    return items

def find_connections(items, top_n=10):
    """Find top N cross-platform connections"""
    similarities = []

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            # Only compare across different sources
            if items[i]['source'] != items[j]['source']:
                sim = cosine_similarity(items[i]['embedding'], items[j]['embedding'])
                similarities.append({
                    "item1": {"text": items[i]['text'], "source": items[i]['source']},
                    "item2": {"text": items[j]['text'], "source": items[j]['source']},
                    "similarity": float(sim)
                })

    return sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:top_n]

def main():
    # Fix Windows console encoding
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("🧠 Finding hidden surveillance connections (LOCAL OLLAMA)...")

    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print("❌ Ollama not running! Start it with: ollama serve")
            return
    except:
        print("❌ Ollama not installed or not running!")
        print("   Install: https://ollama.com/download")
        print("   Then run: ollama pull nomic-embed-text")
        return

    # Prepare data
    items = prepare_data()
    print(f"📊 Prepared {len(items)} items")

    # Get embeddings
    print("🔄 Getting embeddings from Ollama (no limits!)...")
    texts = [f"{item['source']}: {item['text']}" for item in items]
    embeddings = get_embeddings_ollama(texts)

    for i, emb in enumerate(embeddings):
        items[i]['embedding'] = emb

    # Find connections
    print("🔍 Finding top 10 connections...")
    connections = find_connections(items)

    # Display
    print("\n🚨 HIDDEN SURVEILLANCE CONNECTIONS:\n")
    for idx, conn in enumerate(connections, 1):
        print(f"{idx}. SIMILARITY: {conn['similarity']:.3f}")
        print(f"   {conn['item1']['source']}: \"{conn['item1']['text']}\"")
        print(f"   ↕️")
        print(f"   {conn['item2']['source']}: \"{conn['item2']['text']}\"")
        print()

    # Save
    result = {
        "embeddings": items,
        "top_connections": connections,
        "total_items": len(items),
        "model": "ollama/nomic-embed-text"
    }
    save_json(result, "output/embeddings_ollama.json")

    print("✅ Saved to output/embeddings_ollama.json")

if __name__ == "__main__":
    main()
