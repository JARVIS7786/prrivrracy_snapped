import os
import json
import re

TAKEOUT1 = "data/takeout/Takeout 1"
TAKEOUT2 = "data/takeout/Takeout 2"
OUTPUT = "output"

def parse_fast(filepath, limit=50):
    if not os.path.exists(filepath):
        print(f"⚠️  Not found: {filepath}")
        return []

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"📂 Reading {os.path.basename(filepath)} ({size_mb:.1f} MB)...")

    # Broader time patterns to catch any format Google uses
    time_patterns = [
        re.compile(r'(\w{3} \d{1,2}, \d{4},?\s+\d{1,2}:\d{2}:\d{2}\s*[AP]M)'),
        re.compile(r'(\d{1,2} \w{3} \d{4}, \d{1,2}:\d{2}:\d{2}\s*[AP]M)'),
        re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})'),
        re.compile(r'(\w+ \d{1,2}, \d{4})'),
    ]
    link_pattern = re.compile(r'<a[^>]*href=[^>]*>([^<]{3,150})</a>')
    block_start  = re.compile(r'class="outer-cell')

    skip = {
        'here', 'google', 'google search', 'watched', 'youtube',
        'this general area', 'maps', 'search', 'used search',
        'searched for', 'visited', 'used maps'
    }

    # Split file into blocks at each outer-cell
    blocks = []
    current = []
    in_block = False

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if block_start.search(line):
                if current:
                    blocks.append(''.join(current))
                current = [line]
                in_block = True
            elif in_block:
                current.append(line)

    if current:
        blocks.append(''.join(current))

    results = []
    seen = set()

    for block in blocks:
        links = link_pattern.findall(block)

        # Try all time patterns
        timestamp = "Unknown"
        for tp in time_patterns:
            found = tp.findall(block)
            if found:
                timestamp = found[-1]
                break

        for raw in links:
            value = raw.strip()
            # Decode HTML entities
            value = (value.replace('&#39;', "'")
                         .replace('&amp;', '&')
                         .replace('&quot;', '"')
                         .replace('&lt;', '<')
                         .replace('&gt;', '>'))

            if (len(value) > 3
                    and value.lower() not in skip
                    and not value.startswith('http')
                    and not value.startswith('www')
                    and value not in seen):
                results.append({"value": value, "time": timestamp})
                seen.add(value)
                break  # one item per block

        if len(results) >= limit:
            break

    print(f"   ✅ Captured {len(results)} items")
    return results


def parse_google():
    result = {}

    result['google_searches'] = parse_fast(
        f"{TAKEOUT2}/My Activity/Search/My Activity.html", limit=50)

    result['youtube_watched'] = parse_fast(
        f"{TAKEOUT1}/YouTube and YouTube Music/history/watch-history.html", limit=50)

    result['maps_locations'] = parse_fast(
        f"{TAKEOUT2}/My Activity/Maps/My Activity.html", limit=50)

    result['youtube_searches'] = parse_fast(
        f"{TAKEOUT1}/YouTube and YouTube Music/history/search-history.html", limit=50)

    os.makedirs(OUTPUT, exist_ok=True)
    with open(f"{OUTPUT}/google_data.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"✅ Saved to output/google_data.json")
    print(f"🔍 Google searches:  {len(result.get('google_searches', []))}")
    print(f"📺 YouTube watched:  {len(result.get('youtube_watched', []))}")
    print(f"🗺️  Maps locations:   {len(result.get('maps_locations', []))}")
    print(f"🎵 YouTube searches: {len(result.get('youtube_searches', []))}")

    print("\n🔍 Sample Google searches:")
    for s in result.get('google_searches', [])[:8]:
        print(f"   - {s['value']}  ({s['time']})")

    print("\n📺 Sample YouTube watches:")
    for s in result.get('youtube_watched', [])[:5]:
        print(f"   - {s['value']}")

    print("\n🗺️  Sample Maps:")
    for s in result.get('maps_locations', [])[:5]:
        print(f"   - {s['value']}")

    print("\n🎵 Sample YouTube searches:")
    for s in result.get('youtube_searches', [])[:5]:
        print(f"   - {s['value']}")

    return result

if __name__ == "__main__":
    parse_google()