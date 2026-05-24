"""
Dark Patterns Engine
Exposes psychological manipulation tactics used by advertisers
Uses local Ollama (no API costs, no data sent externally)
"""
import json
import os
import sys
import pandas as pd
import requests

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load from correct location
OUTPUT_DIR = "output"
IG_FILE = f"{OUTPUT_DIR}/instagram_data.json"
OUTPUT_CSV = f"{OUTPUT_DIR}/dark_pattern_matrix.csv"
OUTPUT_JSON = f"{OUTPUT_DIR}/dark_pattern_matrix.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma2:2b"  # Change to whatever model you have

# The 5 dark pattern categories with descriptions
DARK_PATTERNS = {
    "Scarcity & Urgency":
        "Limited time offers, countdown timers, 'only X left'",
    "Social Proof & FOMO":
        "X people bought this, trending now, your friends use this",
    "Insecurity & Aspirational":
        "You could look better, be smarter, earn more",
    "Outrage & Emotional Engagement":
        "Fear, anger, controversy to drive clicks",
    "Utility (Neutral)":
        "Genuine product/service with no manipulation"
}

def check_ollama():
    """Check if Ollama is running"""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except:
        return False

def classify_with_ollama(advertiser):
    """Ask local LLM to classify the dark pattern"""
    prompt = f"""You are a consumer protection AI.
Analyze the advertiser: '{advertiser}'

Which psychological dark pattern do they primarily use?
Choose EXACTLY ONE:
- Scarcity & Urgency
- Social Proof & FOMO  
- Insecurity & Aspirational
- Outrage & Emotional Engagement
- Utility (Neutral)

Respond ONLY with valid JSON, nothing else:
{{"Trigger_Category": "chosen category", "Explanation": "one sentence reason"}}"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code != 200:
            return None

        raw = response.json().get("response", "").strip()

        # Bulletproof JSON extraction
        if "{" in raw and "}" in raw:
            raw = raw[raw.find("{"):raw.rfind("}")+1]

        result = json.loads(raw)
        return {
            "Trigger_Category": result.get("Trigger_Category", "Utility (Neutral)"),
            "Explanation": result.get("Explanation", "No explanation provided")
        }

    except Exception as e:
        return None

def classify_with_keywords(advertiser):
    """
    Fallback: rule-based classification when Ollama unavailable
    Good enough for portfolio demo
    """
    ad_lower = advertiser.lower()

    rules = {
        "Scarcity & Urgency": [
            "scaler", "academy", "course", "bootcamp", "unacademy",
            "byju", "upgrad", "testbook", "naukri", "internshala"
        ],
        "Social Proof & FOMO": [
            "linkedin", "dream11", "mpl", "cred", "groww",
            "zerodha", "coinswitch", "fantasy"
        ],
        "Insecurity & Aspirational": [
            "myntra", "zara", "fashion", "tanishq", "foxtale",
            "mamaearth", "nykaa", "dermaco", "skin", "hair"
        ],
        "Outrage & Emotional Engagement": [
            "news", "republic", "ndtv", "times", "india today",
            "viral", "breaking", "shocking"
        ]
    }

    for pattern, keywords in rules.items():
        if any(kw in ad_lower for kw in keywords):
            return {
                "Trigger_Category": pattern,
                "Explanation": f"Keyword match: {advertiser} targets this pattern"
            }

    return {
        "Trigger_Category": "Utility (Neutral)",
        "Explanation": "No dark pattern detected"
    }

def expose_psychological_triggers():
    print("=" * 55)
    print("🧠 DARK PATTERN EXPOSURE ENGINE")
    print("=" * 55)

    # Load Instagram data
    if not os.path.exists(IG_FILE):
        print(f"❌ {IG_FILE} not found. Run instagram_parser.py first.")
        return

    with open(IG_FILE, 'r', encoding='utf-8') as f:
        ig_data = json.load(f)

    advertisers = ig_data.get("advertisers_sample", [])
    if not advertisers:
        print("❌ No advertisers found.")
        return

    # Check if Ollama available
    use_ollama = check_ollama()
    if use_ollama:
        print(f"✅ Ollama running — using {OLLAMA_MODEL} for AI classification")
        limit = 20  # LLM is slower
    else:
        print("⚠️  Ollama not running — using keyword fallback")
        print("   To use AI: ollama serve && ollama pull gemma3:4b")
        use_ollama = False
        limit = len(advertisers)  # Keywords are instant

    print(f"📊 Analyzing {min(limit, len(advertisers))} advertisers...\n")

    results = []
    pattern_counts = {k: 0 for k in DARK_PATTERNS.keys()}

    for i, ad in enumerate(advertisers[:limit]):
        print(f"  [{i+1}/{min(limit, len(advertisers))}] {ad[:50]}")

        if use_ollama:
            result = classify_with_ollama(ad)
            if not result:  # Fallback if LLM fails
                result = classify_with_keywords(ad)
        else:
            result = classify_with_keywords(ad)

        category = result["Trigger_Category"]
        pattern_counts[category] = pattern_counts.get(category, 0) + 1

        results.append({
            "Advertiser": ad,
            "Psychological_Trigger": category,
            "Mechanism": result["Explanation"],
            "Method": "AI" if use_ollama else "Rules"
        })

    # Build DataFrame
    df = pd.DataFrame(results)

    # Find primary vulnerability
    top_pattern = max(pattern_counts, key=pattern_counts.get)
    top_count = pattern_counts[top_pattern]

    print(f"\n{'='*55}")
    print(f"🎯 PSYCHOLOGICAL VULNERABILITY REPORT")
    print(f"{'='*55}")
    print(f"\nPattern breakdown:")
    for pattern, count in sorted(pattern_counts.items(),
                                  key=lambda x: -x[1]):
        if count > 0:
            pct = (count / sum(pattern_counts.values())) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {pattern:<35} {bar} {count} ({pct:.0f}%)")

    print(f"\n⚠️  PRIMARY VULNERABILITY: {top_pattern}")
    print(f"   {top_count} of your advertisers exploit this pattern")
    print(f"\n   What this means:")
    print(f"   {DARK_PATTERNS[top_pattern]}")

    # Sample advertisers per category
    print(f"\n📋 Sample advertisers by pattern:")
    for pattern in DARK_PATTERNS.keys():
        matching = [r["Advertiser"] for r in results
                   if r["Psychological_Trigger"] == pattern][:3]
        if matching:
            print(f"  {pattern}: {', '.join(matching)}")

    # Save outputs
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    summary = {
        "total_analyzed": len(results),
        "pattern_breakdown": pattern_counts,
        "primary_vulnerability": top_pattern,
        "top_advertisers_per_pattern": {
            pattern: [r["Advertiser"] for r in results
                     if r["Psychological_Trigger"] == pattern][:5]
            for pattern in DARK_PATTERNS.keys()
        },
        "detailed_results": results
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved to {OUTPUT_CSV}")
    print(f"✅ Saved to {OUTPUT_JSON}")
    return summary

if __name__ == "__main__":
    expose_psychological_triggers()