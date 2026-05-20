"""
Feature Engineering - Simplified
Builds user profile from Instagram + Google data
"""
from parsers.utils import load_json, save_json

IG_FILE = "output/instagram_data.json"
GOOGLE_FILE = "output/google_data.json"
OUTPUT = "output/user_feature_matrix.json"

# Affinity keywords
CATEGORIES = {
    "cricket": ["csk", "ipl", "dhoni", "cricket", "match", "score"],
    "coding": ["python", "code", "github", "docker", "api"],
    "bollywood": ["kiara", "kareena", "movie", "bollywood"],
    "spiritual": ["sadhguru", "temple", "meditation", "yoga"],
    "mumbai": ["virar", "mumbai", "thakur", "maharashtra"],
    "shopping": ["buy", "shop", "store", "sale"],
    "entertainment": ["netflix", "youtube", "reel", "viral"]
}

def build_feature_matrix():
    """Build user affinity scores"""
    print("⚙️  Building feature matrix...")

    ig = load_json(IG_FILE)
    google = load_json(GOOGLE_FILE)

    # Collect all text
    all_text = []
    for search in ig.get('recent_searches', []):
        all_text.append(search.get('query', '').lower())
    for search in google.get('google_searches', []):
        all_text.append(search.get('value', '').lower())
    for video in google.get('youtube_watched', []):
        all_text.append(video.get('value', '').lower())

    # Score each category
    scores = {cat: 0 for cat in CATEGORIES}
    for text in all_text:
        for category, keywords in CATEGORIES.items():
            if any(kw in text for kw in keywords):
                scores[category] += 1

    # Normalize to 0-1
    max_score = max(scores.values()) or 1
    normalized = {k: round(v / max_score, 3) for k, v in scores.items()}

    # Demographics from ad categories
    ad_cats = [str(c).lower() for c in ig.get('ad_categories', [])]
    demographics = {
        "is_single": any("single" in c for c in ad_cats),
        "is_educated": any("degree" in c for c in ad_cats),
        "is_engaged_shopper": any("shopper" in c for c in ad_cats),
        "potential_device_change": any("device" in c for c in ad_cats)
    }

    result = {
        "affinity_scores": normalized,
        "demographics": demographics,
        "advertiser_pressure": ig.get('advertiser_count', 0),
        "total_data_points": len(all_text)
    }

    save_json(result, OUTPUT)

    print(f"✅ Feature matrix built: {result['advertiser_pressure']} advertisers tracking")
    return result

if __name__ == "__main__":
    build_feature_matrix()
