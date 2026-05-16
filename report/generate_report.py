import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def generate_privacy_report():
    json_path = "output/instagram_data.json"

    if not os.path.exists(json_path):
        print(f"❌ Could not find {json_path}. Run instagram_parser.py first!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        user_data = json.load(f)

    ad_count = user_data.get('advertiser_count', 0)
    categories = user_data.get('ad_categories', [])
    locations = user_data.get('locations', [])
    searches = user_data.get('recent_searches', [])
    industry_breakdown = user_data.get('industry_breakdown', {})

    search_terms = [s.get('query', '') for s in searches] if isinstance(searches, list) else []

    industry_summary = ", ".join(
        f"{cat}: {len(ads)} companies"
        for cat, ads in industry_breakdown.items()
        if ads and cat != "Other / Uncategorized"
    ) if industry_breakdown else "multiple industries"

    prompt = f"""
You are a witty, slightly sarcastic, but insightful data privacy expert. 
Your job is to take raw data exported from a user's Instagram account and 
turn it into a highly shareable, eye-opening, "Black Mirror"-style 
'Privacy Wrapped' report.

Make it punchy, use emojis, and make it easy for a regular person to understand. 
Make them realize how much they are being tracked without sounding like a 
boring legal document. Address the user directly as "You".

Here is the user's real data:
- Total companies actively tracking them: {ad_count}
- Industry breakdown: {industry_summary}
- Locations Instagram has profiled: {', '.join(locations[:5])}
- Their recent searches: {', '.join(search_terms[:5])}
- How Instagram categorizes them: {', '.join(categories[:7])}

Write a report with 4 sections:
1. A catchy slightly scary title
2. Opening hook — how many companies paid to track them and what that means
3. Their "Algorithm Personality" — what Instagram thinks they are based on 
   their categories, relationship status, education level and searches
4. The "Invisible Bubble" — how this profiling traps them and what they 
   are NOT being shown because of it

End with one line: "Want to see what YouTube and Spotify know? Upload those next."
"""

    print("🤖 Sending your data to OpenRouter... bracing for impact...")

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
                "model": "openrouter/free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
        )

        result = response.json()

        if "error" in result:
            print(f"❌ OpenRouter error: {result['error']}")
            return

        report = result["choices"][0]["message"]["content"]

        os.makedirs('output', exist_ok=True)
        with open('output/scary_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)

        print("\n" + "="*60)
        print("🔥 YOUR PRIVACY WRAPPED REPORT 🔥")
        print("="*60 + "\n")
        print(report)
        print("\n" + "="*60)
        print("✅ Saved to output/scary_report.txt")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_privacy_report()