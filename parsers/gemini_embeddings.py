"""
Gemini Embeddings - Simplified
Finds hidden cross-platform surveillance connections
"""
import os
import sys
from dotenv import load_dotenv
import google.genai as genai
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parsers.utils import load_json, save_json

load_dotenv()

def get_embeddings(texts, model="models/gemini-embedding-2", batch_size=50):
    """Get embeddings from Gemini API in batches"""
    import time
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    all_embeddings = []

    # Process in batches of 50 (safer for rate limits)
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_num = i//batch_size + 1
        total_batches = (len(texts) + batch_size - 1) // batch_size
        print(f"   Processing batch {batch_num}/{total_batches} ({len(batch)} items)...")

        result = client.models.embed_content(
            model=model,
            contents=batch
        )
        all_embeddings.extend(result.embeddings)

        # Wait 15 seconds between batches to avoid rate limit
        if i + batch_size < len(texts):
            print(f"   ⏳ Waiting 15s to avoid rate limit...")
            time.sleep(15)

    return all_embeddings

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

    # Instagram searches
    for s in ig.get('recent_searches', []):
        items.append({
            "text": s['query'],
            "source": "Instagram",
            "category": "search"
        })

    # YouTube videos
    for v in google.get('youtube_watched', []):
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
    for ad in ig.get('advertisers_sample', []):
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

    print("🧠 Finding hidden surveillance connections...")

    # Setup API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Get one at: https://aistudio.google.com/app/apikey")
        return

    # Prepare data
    items = prepare_data()
    print(f"📊 Prepared {len(items)} items")

    # Get embeddings
    print("🔄 Getting embeddings...")
    texts = [f"{item['source']}: {item['text']}" for item in items]
    embeddings = get_embeddings(texts)

    for i, emb in enumerate(embeddings):
        items[i]['embedding'] = emb.values

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
        "total_items": len(items)
    }
    save_json(result, "output/embeddings.json")

    print("✅ Saved to output/embeddings.json")

if __name__ == "__main__":
    main()
