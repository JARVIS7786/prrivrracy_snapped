from bs4 import BeautifulSoup
import os
import json

BASE = os.path.join(os.path.dirname(__file__), '..', 'data', 'instagram')
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'output')

def extract_text_items(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    items = []
    for div in soup.find_all(['div', 'td', 'li']):
        text = div.get_text(strip=True)
        if 2 < len(text) < 100 and not text.startswith('{') and not text.startswith('.'):
            items.append(text)
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def extract_clean_searches(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    clean_searches = []
    tables = soup.find_all('table')
    for table in tables:
        search_data = {"query": "Unknown", "time": "Unknown"}
        rows = table.find_all('tr')
        for row in rows:
            row_text = row.get_text(separator='|', strip=True)
            parts = row_text.split('|')
            if len(parts) >= 2:
                if parts[0] in ['Search query', 'Search', 'Search text']:
                    search_data["query"] = parts[1]
                elif parts[0] in ['Update time', 'Time']:
                    search_data["time"] = parts[1]
        if search_data["query"] != "Unknown":
            clean_searches.append(search_data)
    return clean_searches

def categorize_advertisers(advertiser_list):
    categories = {
        "Tech & Apps": ["tech", "software", "app", "digital", "ai ", "web", "lenovo", "microsoft", "adobe", "cisco", "dell", "hp", "data", "cloud", "mobile", "cyber", "internet", "hosting", "truecaller"],
        "Fashion & Beauty": ["fashion", "clothing", "apparel", "wear", "shoe", "cosmetic", "beauty", "makeup", "salon", "myntra", "ajio", "snitch", "h&m", "zara", "puma", "adidas", "style", "vogue", "jewel", "skin", "derma", "nykaa"],
        "Finance & Banking": ["finance", "bank", "insurance", "wealth", "invest", "capital", "paytm", "hdfc", "icici", "sbi", "kotak", "money", "fund", "razorpay", "trading", "credit", "tax", "broker"],
        "Food & Dining": ["food", "restaurant", "cafe", "kitchen", "dining", "swiggy", "zomato", "pizza", "burger", "kfc", "mcdonald", "tea", "coffee", "cook", "chef", "bake", "eats", "recipe", "snack"],
        "Travel & Hotels": ["travel", "hotel", "resort", "trip", "airway", "airline", "indigo", "makemytrip", "goibibo", "booking", "airbnb", "tour", "cruise", "ticket", "holiday", "rooms"],
        "Education & Career": ["edu", "university", "academy", "school", "college", "learn", "course", "udemy", "testbook", "scaler", "physics wallah", "vedantu", "institute", "study", "naukri", "job", "career", "intern"],
        "Entertainment & Media": ["entertainment", "media", "studio", "picture", "cinema", "news", "music", "film", "tv", "video", "netflix", "prime", "spotify", "pvr", "zee5", "hotstar", "game", "gaming", "bookmyshow"],
        "Health & Fitness": ["health", "clinic", "doctor", "hospital", "wellness", "pharma", "gym", "fitness", "yoga", "dental", "med", "cure", "fit"]
    }
    categorized = {key: [] for key in categories.keys()}
    categorized["Other / Uncategorized"] = []
    for ad in advertiser_list:
        ad_lower = ad.lower()
        matched = False
        for category, keywords in categories.items():
            if any(kw in ad_lower for kw in keywords):
                categorized[category].append(ad)
                matched = True
                break
        if not matched:
            categorized["Other / Uncategorized"].append(ad)
    return categorized

def parse_instagram():
    result = {}

    advertisers = extract_text_items(
        os.path.join(BASE, "ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.html")
    )
    clean_advertisers = [i for i in advertisers if len(i) > 3 and i[0].isupper()]
    categorized = categorize_advertisers(clean_advertisers)

    # Keys match the HTML UI exactly
    result["total_advertisers"] = len(clean_advertisers)
    result["advertisers_sample"] = clean_advertisers[:20]
    result["industries"] = {k: len(v) for k, v in categorized.items()}

    categories = extract_text_items(
        os.path.join(BASE, "ads_information/instagram_ads_and_businesses/other_categories_used_to_reach_you.html")
    )
    result["ad_categories"] = [c for c in categories if 3 < len(c) < 60 and c[0].isupper()]

    locations = extract_text_items(
        os.path.join(BASE, "personal_information/information_about_you/locations_of_interest.html")
    )
    result["locations"] = [l for l in locations if 3 < len(l) < 50 and l[0].isupper()]

    result["searches"] = extract_clean_searches(
        os.path.join(BASE, "logged_information/recent_searches/recent_searches.html")
    )

    os.makedirs(OUTPUT, exist_ok=True)
    with open(os.path.join(OUTPUT, 'instagram_data.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to output/instagram_data.json")
    print(f"🔴 Advertisers: {result['total_advertisers']}")
    print(f"🎯 Categories: {result['ad_categories']}")
    print(f"📍 Locations: {result['locations']}")
    print(f"🔍 Searches: {len(result['searches'])} found")
    return result

if __name__ == "__main__":
    parse_instagram()