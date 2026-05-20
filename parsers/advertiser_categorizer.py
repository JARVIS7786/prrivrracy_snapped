"""
Advertiser Categorization using Gemini Embeddings
Smart categorization that understands context (Tata Motors vs Tata Tea)
"""
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
from parsers.utils import load_json, save_json

load_dotenv()

def get_embeddings(texts, model="models/text-embedding-004"):
    """Get embeddings from Gemini API"""
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=texts,
        task_type="retrieval_document"
    )
    return result['embedding']

def cosine_similarity(vec1, vec2):
    """Calculate similarity between two vectors"""
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Category descriptions for better context understanding
CATEGORY_DESCRIPTIONS = {
    "Tech & Apps": "technology software applications mobile apps artificial intelligence cloud computing data analytics programming",
    "Fashion & Beauty": "clothing fashion beauty makeup cosmetics style apparel jewelry accessories skincare",
    "Finance": "banking finance insurance investment money payment wallet credit card loan stock market",
    "Food & Beverage": "food restaurant cafe beverage drinks tea coffee swiggy zomato dining cuisine",
    "Travel & Hospitality": "travel hotel airline booking vacation tourism flight accommodation resort",
    "Education & Career": "education academy course learning training career job recruitment naukri upskilling",
    "Entertainment & Media": "entertainment netflix spotify gaming movies music streaming media content",
    "Health & Fitness": "health clinic gym fitness wellness yoga medical healthcare hospital pharmacy",
    "E-commerce & Retail": "shopping online store retail marketplace ecommerce buy sell products",
    "Automotive": "car vehicle automobile bike motorcycle automotive motors driving transport",
    "Real Estate": "property real estate housing apartment flat home construction builder",
    "Telecom & Internet": "telecom internet mobile network broadband wifi data connection provider"
}

def categorize_advertisers_with_embeddings(advertisers, batch_size=20):
    """
    Categorize advertisers using semantic embeddings
    Handles ambiguous names like 'Tata' by understanding context
    Rate limited to avoid quota exhaustion
    """
    print(f"Categorizing {len(advertisers)} advertisers using AI embeddings...")

    # Setup API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return None
    genai.configure(api_key=api_key)

    # Get category embeddings (one-time)
    print("Getting category embeddings...")
    category_names = list(CATEGORY_DESCRIPTIONS.keys())
    category_texts = list(CATEGORY_DESCRIPTIONS.values())
    category_embeddings = get_embeddings(category_texts)

    # Categorize advertisers in batches
    categorized = {cat: [] for cat in category_names}
    categorized["Other"] = []

    total_batches = (len(advertisers) + batch_size - 1) // batch_size

    for batch_idx in range(0, len(advertisers), batch_size):
        batch = advertisers[batch_idx:batch_idx + batch_size]
        batch_num = batch_idx // batch_size + 1
        print(f"Processing batch {batch_num}/{total_batches}...")

        # Get advertiser embeddings
        advertiser_embeddings = get_embeddings(batch)

        # Find best category for each advertiser
        for ad, ad_emb in zip(batch, advertiser_embeddings):
            similarities = [
                cosine_similarity(ad_emb, cat_emb)
                for cat_emb in category_embeddings
            ]

            max_similarity = max(similarities)
            best_category_idx = similarities.index(max_similarity)

            # Only categorize if similarity is above threshold
            if max_similarity > 0.3:  # Confidence threshold
                best_category = category_names[best_category_idx]
                categorized[best_category].append({
                    "name": ad,
                    "confidence": float(max_similarity)
                })
            else:
                categorized["Other"].append({
                    "name": ad,
                    "confidence": float(max_similarity)
                })

        # Rate limiting: wait 60 seconds after every batch to avoid quota
        if batch_num < total_batches:
            print(f"Waiting 60s to avoid rate limit...")
            time.sleep(60)

    return categorized

def main():
    print("Smart Advertiser Categorization\n")

    # Load Instagram data
    ig_data = load_json("output/instagram_data.json")
    if not ig_data:
        print("❌ Instagram data not found. Run instagram_parser.py first.")
        return

    # Get all advertisers (not just sample)
    advertisers_file = "data/instagram/ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.html"
    from parsers.utils import parse_html_file, extract_text_from_tags
    soup = parse_html_file(advertisers_file)
    all_advertisers = extract_text_from_tags(soup)

    # TEST MODE: Use only first 100 advertisers
    test_advertisers = all_advertisers[:100]
    print(f"TEST MODE: Using {len(test_advertisers)} advertisers (out of {len(all_advertisers)} total)\n")

    # Categorize using embeddings
    categorized = categorize_advertisers_with_embeddings(test_advertisers)

    if not categorized:
        return

    # Generate summary
    summary = {cat: len(ads) for cat, ads in categorized.items()}

    # Display results
    print("\nCATEGORIZATION COMPLETE:\n")
    for category, count in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} advertisers")

    # Save detailed results
    result = {
        "total_advertisers": len(all_advertisers),
        "categories": categorized,
        "summary": summary,
        "top_advertisers_per_category": {
            cat: [ad["name"] for ad in ads[:10]]
            for cat, ads in categorized.items() if ads
        }
    }

    save_json(result, "output/advertiser_categories.json")
    print("\nSaved to output/advertiser_categories.json")

    # Show examples
    print("\nEXAMPLE CATEGORIZATIONS:\n")
    for category in list(CATEGORY_DESCRIPTIONS.keys())[:5]:
        if categorized[category]:
            top_3 = categorized[category][:3]
            print(f"{category}:")
            for ad in top_3:
                print(f"  • {ad['name']} (confidence: {ad['confidence']:.2f})")
            print()

if __name__ == "__main__":
    main()
