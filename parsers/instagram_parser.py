"""
Instagram Parser - Simplified
Extracts: advertisers, ad categories, locations, searches
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parsers.utils import parse_html_file, extract_text_from_tags, save_json

BASE = "data/instagram"
OUTPUT = "output/instagram_data.json"

def parse_searches(filepath):
    """Extract Instagram searches with timestamps"""
    soup = parse_html_file(filepath)
    if not soup:
        return []

    searches = []
    for table in soup.find_all('table'):
        query, time = "Unknown", "Unknown"
        for row in table.find_all('tr'):
            text = row.get_text(separator='|', strip=True)
            parts = text.split('|')
            if len(parts) >= 2:
                if parts[0] in ['Search query', 'Search', 'Search text']:
                    query = parts[1]
                elif parts[0] in ['Update time', 'Time']:
                    time = parts[1]
        if query != "Unknown":
            searches.append({"query": query, "time": time})
    return searches

def categorize_advertisers(advertisers):
    """Group advertisers by industry"""
    categories = {
        "Tech & Apps": ["tech", "software", "app", "ai", "data", "cloud"],
        "Fashion & Beauty": ["fashion", "clothing", "beauty", "makeup", "style"],
        "Finance": ["finance", "bank", "insurance", "invest", "paytm"],
        "Food": ["food", "restaurant", "swiggy", "zomato"],
        "Travel": ["travel", "hotel", "airline", "booking"],
        "Education": ["edu", "academy", "course", "scaler", "naukri"],
        "Entertainment": ["entertainment", "netflix", "spotify", "gaming"],
        "Health": ["health", "clinic", "gym", "fitness"]
    }

    result = {cat: [] for cat in categories}
    result["Other"] = []

    for ad in advertisers:
        matched = False
        ad_lower = ad.lower()
        for category, keywords in categories.items():
            if any(kw in ad_lower for kw in keywords):
                result[category].append(ad)
                matched = True
                break
        if not matched:
            result["Other"].append(ad)

    return {k: len(v) for k, v in result.items()}

def parse_instagram():
    """Main Instagram parser"""
    # Fix Windows console encoding
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("📸 Parsing Instagram data...")

    # Parse advertisers
    soup = parse_html_file(f"{BASE}/ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.html")
    advertisers = extract_text_from_tags(soup)

    # Parse ad categories
    soup = parse_html_file(f"{BASE}/ads_information/instagram_ads_and_businesses/other_categories_used_to_reach_you.html")
    ad_categories = extract_text_from_tags(soup, max_len=60)

    # Parse locations
    soup = parse_html_file(f"{BASE}/personal_information/information_about_you/locations_of_interest.html")
    locations = extract_text_from_tags(soup, max_len=50)

    # Parse searches
    searches = parse_searches(f"{BASE}/logged_information/recent_searches/recent_searches.html")

    # Build result with CONSISTENT key names
    result = {
        "advertiser_count": len(advertisers),
        "advertisers_sample": advertisers[:20],
        "industries": categorize_advertisers(advertisers),
        "ad_categories": ad_categories,
        "locations": locations,
        "recent_searches": searches
    }

    save_json(result, OUTPUT)

    print(f"✅ Instagram parsed: {result['advertiser_count']} advertisers, {len(searches)} searches")
    return result

if __name__ == "__main__":
    parse_instagram()
