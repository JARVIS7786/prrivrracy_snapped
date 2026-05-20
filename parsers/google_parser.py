"""
Google Parser - Simplified
Extracts: Google searches, YouTube history, Maps locations
"""
import os
import re
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parsers.utils import save_json, decode_html_entities

TAKEOUT1 = "data/takeout/Takeout 1"
TAKEOUT2 = "data/takeout/Takeout 2"
OUTPUT = "output/google_data.json"

def parse_activity_html(filepath, limit=50):
    """Parse Google My Activity HTML files"""
    if not os.path.exists(filepath):
        print(f"⚠️  Not found: {filepath}")
        return []

    print(f"📂 Parsing {os.path.basename(filepath)}...")

    # Regex patterns
    time_pattern = re.compile(r'(\w+ \d{1,2}, \d{4})')
    link_pattern = re.compile(r'<a[^>]*>([^<]{3,150})</a>')
    block_pattern = re.compile(r'class="outer-cell')

    # Skip generic phrases
    skip_words = {'here', 'google', 'youtube', 'maps', 'search', 'watched', 'visited'}

    # Split into blocks
    blocks = []
    current = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if block_pattern.search(line):
                if current:
                    blocks.append(''.join(current))
                current = [line]
            elif current:
                current.append(line)
    if current:
        blocks.append(''.join(current))

    # Extract data
    results = []
    seen = set()

    for block in blocks[:limit]:
        # Find timestamp
        time_match = time_pattern.search(block)
        timestamp = time_match.group(1) if time_match else "Unknown"

        # Find link text
        links = link_pattern.findall(block)
        for raw in links:
            value = decode_html_entities(raw.strip())
            if (len(value) > 3
                and value.lower() not in skip_words
                and not value.startswith('http')
                and value not in seen):
                results.append({"value": value, "time": timestamp})
                seen.add(value)
                break

    print(f"   ✅ Found {len(results)} items")
    return results

def parse_google():
    """Main Google parser"""
    # Fix Windows console encoding
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("🔍 Parsing Google data...")

    result = {
        "google_searches": parse_activity_html(f"{TAKEOUT2}/My Activity/Search/My Activity.html"),
        "youtube_watched": parse_activity_html(f"{TAKEOUT1}/YouTube and YouTube Music/history/watch-history.html"),
        "maps_locations": parse_activity_html(f"{TAKEOUT2}/My Activity/Maps/My Activity.html"),
        "youtube_searches": parse_activity_html(f"{TAKEOUT1}/YouTube and YouTube Music/history/search-history.html")
    }

    save_json(result, OUTPUT)

    print(f"✅ Google parsed: {len(result['google_searches'])} searches, {len(result['youtube_watched'])} videos")
    return result

if __name__ == "__main__":
    parse_google()
