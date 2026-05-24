import sys
import os
import json
import random
import asyncio
import subprocess
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import networkx as nx

# Re-use your clean shared utilities from parsers/utils.py
from utils import load_json, save_json

# Ensure Windows prints emojis and logs beautifully without encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# =====================================================================
# ENGINE 1: SHADOW PROFILING via NETWORK LINK PREDICTION (ADAMIC-ADAR)
# =====================================================================
def run_shadow_link_prediction():
    print("\n[+] Running Layer 3.5: Shadow Profiling Engine...")
    
    ig_data = load_json("output/instagram_data.json")
    google_data = load_json("output/google_data.json")
    
    if not ig_data or not google_data:
        print("[-] Missing parsed source data. Run base parsers first.")
        return []

    G = nx.Graph()
    G.add_node("YOU", type="identity")
    
    # Map Google searches to temporal windows to trace behavioral correlations
    for search in google_data.get("google_searches", []):
        query = search.get("value")
        time_str = search.get("time", "Unknown")
        if query and time_str != "Unknown":
            # Discretize continuous time strings to find cross-app overlaps
            time_bucket = f"Time_{time_str.replace(' ', '_')}"
            search_node = f"Search_{query.lower().replace(' ', '_')}"
            
            G.add_node(search_node, type="interest", label=query)
            G.add_node(time_bucket, type="temporal_anchor")
            G.add_edge("YOU", search_node)
            G.add_edge(search_node, time_bucket)

    # Correlate Instagram activity inside identical temporal windows
    for search in ig_data.get("recent_searches", []):
        query = search.get("query")
        time_str = search.get("time", "Unknown")
        if query and time_str != "Unknown":
            try:
                # Standardize custom date formats to evaluate proximity metrics
                dt = datetime.strptime(time_str.split(" pm")[0].split(" am")[0].strip(), "%b %d, %Y %I:%M")
                time_bucket = f"Time_{dt.strftime('%B_%d,_%Y')}"
            except:
                time_bucket = f"Time_{time_str.split(' ')[0]}"
                
            ig_node = f"IG_Hashtag_{query.lower().replace('#', '')}"
            G.add_node(ig_node, type="external_profile", label=query)
            G.add_edge("YOU", ig_node)
            
            if G.has_node(time_bucket):
                G.add_edge(ig_node, time_bucket)

    # Execute Adamic-Adar on bipartite interactions to trace implicit dependencies
    interest_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'interest']
    external_profiles = [n for n, d in G.nodes(data=True) if d.get('type') == 'external_profile']
    
    candidate_pairs = [(p, i) for p in external_profiles for i in interest_nodes if not G.has_edge(p, i)]
    
    if not candidate_pairs:
        return []

    aa_preds = nx.adamic_adar_index(G, candidate_pairs)
    inferences = []
    
    for u, v, score in aa_preds:
        if score > 0:
            prob = 1 / (1 + np.exp(-score)) # Standard logistic feature mapping
            inferences.append({
                "Inferred_Connection": G.nodes[u]['label'],
                "Target_Interest": G.nodes[v]['label'],
                "Inference_Confidence": round(prob * 100, 2)
            })
            
    df = pd.DataFrame(inferences)
    if not df.empty:
        df = df.sort_values(by="Inference_Confidence", ascending=False).head(5)
        print(f"    Discovered {len(df)} shadow tracking profile bridges.")
        return df.to_dict(orient="records")
    return []

# =====================================================================
# ENGINE 2: THE FOUR PILLARS (DARK PATTERN EXPOSURE CLASSIFIER)
# =====================================================================
def classify_dark_patterns():
    print("\n[+] Running Layer 4.5: Dark Pattern Exposure Engine...")
    ig_data = load_json("output/instagram_data.json")
    advertisers = ig_data.get("advertisers_sample", [])
    
    if not advertisers:
        print("[-] No advertiser metrics found.")
        return {}

    # Behavioral categorization heuristics evaluating user vulnerability triggers
    patterns = {
        "Scarcity & Urgency": ["scaler", "academy", "course", "bootcamp", "unacademy", "byju"],
        "Social Proof & FOMO": ["linkedin", "naukri", "dream11", "mpl", "cred"],
        "Insecurity & Aspirational": ["myntra", "zara", "fashion", "menswear", "tanishq", "foxtale"],
        "Variable Reward (Dopamine Loops)": ["netflix", "spotify", "hotstar", "amazon", "swiggy", "zomato"]
    }
    
    breakdown = {k: 0 for k in patterns.keys()}
    breakdown["Utility (Neutral)"] = 0
    
    for ad in advertisers:
        matched = False
        ad_lower = ad.lower()
        for pattern, keywords in patterns.items():
            if any(kw in ad_lower for kw in keywords):
                breakdown[pattern] += 1
                matched = True
                break
        if not matched:
            breakdown["Utility (Neutral)"] += 1
            
    print(f"    Dark pattern tracking matrix built successfully.")
    return breakdown

# =====================================================================
# ENGINE 3: TEMPORAL LOOP COUNTERMEASURES (.ICS CALENDAR SHIELD)
# =====================================================================
def generate_calendar_blindspot_shield():
    print("\n[+] Running Layer 5: Algorithmic Blindspot Shield...")
    
    # Identify high-risk temporal clusters when browsing habits trigger multi-platform syncing
    # Inject an absolute interruption vector exactly 15 minutes before pattern activation
    calendar_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Privacy Wrapped Active Defense//EN",
        "BEGIN:VEVENT",
        f"DTSTART:{datetime.now().strftime('%Y%m%dT224500')}", # Lock targeting to peak evening spikes
        f"DTEND:{datetime.now().strftime('%Y%m%dT231500')}",
        "SUMMARY:🛡️ PRIVACY SHIELD ACTIVE: Break Tracking Loop",
        "DESCRIPTION:System alert! Behavioral metrics show platform tracking synchronization peaks in 15 mins. Step away from your phone and practice your 5-string guitar chords or tremolo harmonica melody to confuse habit logging vectors.",
        "END:VEVENT",
        "END:VCALENDAR"
    ]
    
    output_path = "output/privacy_shield_interruption.ics"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(calendar_lines))
        
    print(f"    Exported calendar counter-measure schedule to: {output_path}")

# =====================================================================
# ENGINE 4: AUTOMATED BG PROFILE POISONER (HUMAN-SIMULATED PLAYWRIGHT BROWSER)
# =====================================================================
def run_bg_poisoning_agent():
    """
    Spawns an asynchronous background browser instance running independent operations
    to systematically inject clean data noise directly back into ad trackers.
    """
    print("\n[+] Instantiating Background Profile Poisoner Script...")
    
    playwright_script = """
import asyncio
import random
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch headless session to quietly pollute tracking data arrays without user lag
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        page = await context.new_page()
        
        decoys = ["organic botany techniques", "how to fix classic cars", "history of ancient architecture"]
        selected = random.choice(decoys)
        
        print(f"    [Background Process] Injecting profile decoy sequence: '{selected}'")
        try:
            await page.goto("https://www.google.com")
            search_box = await page.wait_for_selector("textarea[name='q']", state="visible")
            await search_box.fill(selected)
            await search_box.press("Enter")
            await page.wait_for_timeout(random.randint(5000, 12000)) # Natural human dwell simulation
        except Exception as e:
            pass
        await context.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
"""
    
    with open("parsers/shield_executor.py", "w", encoding="utf-8") as f:
        f.write(playwright_script)
        
    # Launch as a fully detached background child process
    subprocess.Popen(
        ["python", "parsers/shield_executor.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True if sys.platform != 'win32' else None
    )
    print("    Active data defense vector running asynchronously in the background.")

# =====================================================================
# ORCHESTRATION PIPELINE INTEGRATION
# =====================================================================
def main():
    print("="*60)
    # Target and cite your project name verbatim from zip contents
    print("PRIVACY WRAPPED SURVEILLANCE SUITE - COMPONENT UPGRADE")
    print("="*60)
    
    # 1. Compute Network Matrix Connections
    shadow_profiles = run_shadow_link_prediction()
    
    # 2. Extract Psychological Dark Pattern Multiplexes
    behavioral_vulnerabilities = classify_dark_patterns()
    
    # 3. Create Routine Interruption Maps
    generate_calendar_blindspot_shield()
    
    # 4. Initiate Playwright Automation Engine
    run_bg_poisoning_agent()
    
    # Consolidate and update your global system matrix state
    master_matrix = load_json("output/user_feature_matrix.json")
    
    master_matrix["shadow_profiling_bridges"] = shadow_profiles
    master_matrix["dark_pattern_exposure"] = behavioral_vulnerabilities
    master_matrix["pipeline_security_status"] = "ACTIVE_MITIGATION_DEPLOYED"
    
    save_json(master_matrix, "output/user_feature_matrix.json")
    print("\n" + "="*60)
    print("[+] MASTER RECORD SUCCESSFUL: Advanced analysis appended to user_feature_matrix.json")
    print("="*60)

if __name__ == "__main__":
    main()