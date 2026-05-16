import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OUTPUT = "output"

def combine_and_report():
    # Load Instagram data
    ig_path = f"{OUTPUT}/instagram_data.json"
    google_path = f"{OUTPUT}/google_data.json"

    ig = {}
    google = {}

    if os.path.exists(ig_path):
        with open(ig_path, 'r', encoding='utf-8') as f:
            ig = json.load(f)
    else:
        print("⚠️ instagram_data.json not found")

    if os.path.exists(google_path):
        with open(google_path, 'r', encoding='utf-8') as f:
            google = json.load(f)
    else:
        print("⚠️ google_data.json not found")

    # Build combined profile
    combined = {
        # Instagram
        "total_advertisers": ig.get("total_advertisers", 0),
        "ad_categories": ig.get("ad_categories", []),
        "locations": ig.get("locations", []),
        "searches": ig.get("searches", []),
        "industries": ig.get("industries", {}),

        # Google
        "google_searches": google.get("google_searches", []),
        "youtube_watched": google.get("youtube_watched", []),
        "maps_locations": google.get("maps_locations", []),
        "youtube_searches": google.get("youtube_searches", []),
    }

    # Save combined JSON for the UI later
    with open(f"{OUTPUT}/combined_data.json", 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print("✅ Saved output/combined_data.json")

    # Build the prompt
    ig_searches = [s.get('query','') for s in combined['searches'][:5]]
    yt_watched  = [v.get('value','') for v in combined['youtube_watched'][:8]]
    g_searches  = [s.get('value','') for s in combined['google_searches'][:8]]
    maps        = [m.get('value','') for m in combined['maps_locations'][:5]]
    yt_searches = [s.get('value','') for s in combined['youtube_searches'][:5]]

    industry_summary = ", ".join(
        f"{k}: {v}"
        for k, v in combined['industries'].items()
        if v > 0 and k != "Other / Uncategorized"
    )

    prompt = f"""
You are a witty, slightly sarcastic data privacy expert writing a 
"Black Mirror"-style Privacy Wrapped report. Use emojis. Be punchy 
and direct. Address the user as "You". Make it feel personal and 
slightly unsettling — like you know them.

Here is the user's REAL data from Instagram AND Google combined:

INSTAGRAM:
- {combined['total_advertisers']} companies are actively tracking them
- Instagram put them in these categories: {', '.join(combined['ad_categories'][:6])}
- Locations Instagram profiled: {', '.join(combined['locations'][:4])}
- Recent Instagram searches: {', '.join(ig_searches)}
- Industry breakdown: {industry_summary}

GOOGLE / YOUTUBE:
- Recent Google searches: {', '.join(g_searches)}
- YouTube videos recently watched: {', '.join(yt_watched)}
- YouTube searches: {', '.join(yt_searches)}
- Places visited (Google Maps): {', '.join(maps)}

Write 5 sections:
1. 🔴 A dramatic scary title
2. 📊 The Numbers — how many companies track them, what that means in 
   human terms (e.g. "that's more than the population of...")
3. 🧠 Your Algorithm Personality — what Instagram + Google together 
   think they are. Be specific — mention cricket, Python, the maths 
   problems, Thakur College, Bollywood searches. Make it feel like 
   you're reading their mind.
4. 🫧 The Invisible Bubble — what they're NOT being shown and why
5. 🎯 The Punchline — one savage closing line about their digital life

Make it shareable. Make them want to screenshot it.
"""

    print("\n🤖 Sending combined data to AI...")

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Privacy Wrapped"
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1200
            }
        )

        result = response.json()
        if "error" in result:
            print(f"❌ OpenRouter error: {result['error']}")
            return

        report = result["choices"][0]["message"]["content"]

        with open(f"{OUTPUT}/combined_report.txt", 'w', encoding='utf-8') as f:
            f.write(report)

        print("\n" + "="*60)
        print("🔥 YOUR COMBINED PRIVACY WRAPPED REPORT 🔥")
        print("="*60 + "\n")
        print(report)
        print("\n" + "="*60)
        print("✅ Saved to output/combined_report.txt")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    combine_and_report()