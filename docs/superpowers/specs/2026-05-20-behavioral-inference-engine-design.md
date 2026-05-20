# Privacy Wrapped: Behavioral Inference Engine + Active Defense System

**Date:** 2026-05-20  
**Project:** Privacy Wrapped v2.0  
**Goal:** Transform from passive data viewer into an active anti-surveillance defense system using ML inference + LangGraph agents

---

## Executive Summary

**The Problem with v1.0:** It just shows what data exists. It doesn't show what the data *means* to algorithms, and it doesn't *fight back*.

**The Solution:** Build a 3-layer system:
1. **Behavioral Inference Engine** - Reveals what algorithms infer about you (psychographic profiling, shadow networks, temporal vulnerabilities)
2. **Active Defense System** - LangGraph multi-agent system that generates countermeasures
3. **Web-Based Interface** - Keep it simple, no desktop app needed

**Core Innovation:** We don't need 1000 users' data. We extract deep ML insights from YOUR existing Google/Instagram exports using advanced graph algorithms and local LLMs.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER DATA EXPORTS                        │
│              (Instagram ZIP + Google Takeout)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              LAYER 1: BEHAVIORAL INFERENCE ENGINE           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Psychographic│  │    Shadow    │  │   Temporal   │     │
│  │  Profiling   │  │   Network    │  │ Vulnerability│     │
│  │  (Big Five)  │  │  (Link Pred) │  │   Mapping    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│         HIGH-CONFIDENCE VULNERABILITY REPORT                │
│  "You are 91% vulnerable to late-night impulse ads"        │
│  "Shadow profile links your Google + Instagram with 94%"   │
│  "Algorithm classifies you as highly neurotic"             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│        LAYER 2: LANGGRAPH ACTIVE DEFENSE SYSTEM             │
│                    (Local Ollama LLM)                       │
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │ Poisoning Vector │         │ Algorithmic      │        │
│  │     Agent        │         │ Blindspot Agent  │        │
│  │                  │         │                  │        │
│  │ Generates noise  │         │ Behavioral       │        │
│  │ queries to break │         │ interventions    │        │
│  │ tracking profile │         │ to break loops   │        │
│  └──────────────────┘         └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│           LAYER 3: ACTIVE MITIGATION OUTPUT                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Noise Script │  │  Ad-Shield   │  │  Behavioral  │     │
│  │  (Selenium)  │  │   Schedule   │  │ Interventions│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Behavioral Inference Engine

### 1.1 Shadow Network Profiling (Link Prediction)

**What It Does:**
Uses NetworkX Adamic-Adar algorithm to predict hidden connections between your Google and Instagram profiles that you never explicitly linked.

**Implementation:**
```python
# parsers/shadow_network_profiler.py
import networkx as nx
import pandas as pd
import numpy as np
from datetime import datetime

def build_shadow_network(google_data, instagram_data):
    """
    Simulates ad-network shadow profiling using local data exports.
    Uses Adamic-Adar link prediction to uncover hidden behavioral connections.
    """
    G = nx.Graph()
    
    # Core user identity anchor
    G.add_node("Primary_User", type="identity", label="Explicit Me")
    
    # 1. POPULATE GOOGLE DATA
    for g_record in google_data:
        g_time = datetime.fromisoformat(g_record['timestamp'])
        time_bucket = g_time.strftime("%Y-%m-%d_%H:00")  # Hourly discretization
        
        # Location node
        loc_node = f"Loc_{g_record['location_cluster']}"
        G.add_node(loc_node, type="location", label=g_record['location_cluster'])
        G.add_edge("Primary_User", loc_node, weight=1.0)
        
        # Temporal anchor
        G.add_node(time_bucket, type="temporal_anchor")
        G.add_edge(loc_node, time_bucket, weight=1.0)
        
        # Search node
        search_node = f"Search_{g_record['search_query'].lower().replace(' ', '_')}"
        G.add_node(search_node, type="interest", label=g_record['search_query'])
        G.add_edge("Primary_User", search_node, weight=1.0)
        G.add_edge(search_node, time_bucket, weight=1.0)
    
    # 2. POPULATE INSTAGRAM DATA
    for ig_record in instagram_data:
        ig_time = datetime.fromisoformat(ig_record['timestamp'])
        time_bucket = ig_time.strftime("%Y-%m-%d_%H:00")
        
        # Interacted account node
        target_node = f"IG_Profile_{ig_record['interacted_account']}"
        G.add_node(target_node, type="external_profile", label=ig_record['interacted_account'])
        G.add_edge("Primary_User", target_node, weight=1.0)
        
        # Co-occurrence bridge (THE KEY TO SHADOW PROFILING)
        if G.has_node(time_bucket):
            G.add_edge(target_node, time_bucket, weight=1.5)
        
        # Category node
        cat_node = f"Cat_{ig_record['category'].lower()}"
        G.add_node(cat_node, type="interest", label=ig_record['category'])
        G.add_edge(target_node, cat_node, weight=1.0)
    
    print(f"[+] Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # 3. LINK PREDICTION (Adamic-Adar)
    interest_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'interest']
    external_profiles = [n for n, d in G.nodes(data=True) if d.get('type') == 'external_profile']
    
    # Find unlinked pairs
    candidate_pairs = []
    for p in external_profiles:
        for i in interest_nodes:
            if not G.has_edge(p, i):
                candidate_pairs.append((p, i))
    
    # Compute Adamic-Adar scores
    shadow_inferences = []
    aa_preds = nx.adamic_adar_index(G, candidate_pairs)
    
    for u, v, score in aa_preds:
        if score > 0:
            # Normalize to probability [0, 1]
            prob_score = 1 / (1 + np.exp(-score))
            
            shadow_inferences.append({
                "Source_Entity": G.nodes[u]['label'],
                "Source_Type": G.nodes[u]['type'],
                "Inferred_Connection": G.nodes[v]['label'],
                "Connection_Type": G.nodes[v]['type'],
                "Inference_Confidence": round(prob_score * 100, 2),
                "Raw_AA_Score": round(score, 4)
            })
    
    df_results = pd.DataFrame(shadow_inferences)
    if not df_results.empty:
        df_results = df_results.sort_values(by="Raw_AA_Score", ascending=False).reset_index(drop=True)
    
    print(f"[+] Shadow profiling: {len(df_results)} high-probability inferences")
    return df_results, G
```

**Output Example:**
```
Source: music_store_mumbai (Instagram profile)
Inferred Connection: Acoustic Guitar Strings (Google search)
Confidence: 88.42%
Explanation: Both occurred within same 1-hour window at 11 PM
```

**Why This Matters:**
Shows users that platforms can link their separate accounts even without explicit connection, using temporal co-occurrence patterns.

---

### 1.2 Psychographic Profiling (Big Five Personality)

**What It Does:**
Uses semantic embeddings to cluster user behavior and map to Big Five personality traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).

**Implementation:**
```python
# parsers/psychographic_profiler.py
from sklearn.cluster import KMeans
import numpy as np
from parsers.gemini_embeddings import get_embeddings

def profile_personality(user_data, embeddings):
    """
    Maps user behavior clusters to Big Five personality traits.
    """
    # Extract embeddings for all user activities
    activity_embeddings = np.array([e['embedding'] for e in embeddings])
    
    # Cluster into 5 groups (Big Five)
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(activity_embeddings)
    
    # Map clusters to personality traits based on content
    cluster_labels = []
    for i in range(5):
        cluster_items = [embeddings[j]['text'] for j in range(len(embeddings)) if clusters[j] == i]
        
        # Analyze cluster content
        if any('stress' in item.lower() or 'anxiety' in item.lower() for item in cluster_items):
            cluster_labels.append(('Neuroticism', 'HIGH'))
        elif any('party' in item.lower() or 'friends' in item.lower() for item in cluster_items):
            cluster_labels.append(('Extraversion', 'HIGH'))
        elif any('plan' in item.lower() or 'organize' in item.lower() for item in cluster_items):
            cluster_labels.append(('Conscientiousness', 'HIGH'))
        elif any('art' in item.lower() or 'creative' in item.lower() for item in cluster_items):
            cluster_labels.append(('Openness', 'HIGH'))
        else:
            cluster_labels.append(('Agreeableness', 'MEDIUM'))
    
    return {
        "personality_profile": cluster_labels,
        "cluster_distribution": clusters.tolist(),
        "interpretation": generate_interpretation(cluster_labels)
    }

def generate_interpretation(traits):
    """Generate human-readable personality summary."""
    high_traits = [t[0] for t in traits if t[1] == 'HIGH']
    
    if 'Neuroticism' in high_traits:
        return "Algorithm classifies you as highly neurotic based on late-night searches and anxiety markers. You're a prime target for impulse-buy ad targeting."
    elif 'Extraversion' in high_traits:
        return "Algorithm sees you as highly social. Expect ads for events, social apps, and group experiences."
    else:
        return "Algorithm has a mixed read on your personality. Your behavior is less predictable."
```

**Output Example:**
```
Personality Profile:
- Neuroticism: HIGH (based on stress-related searches)
- Conscientiousness: MEDIUM
- Extraversion: LOW

Interpretation:
"You never told Google you were stressed, but based on semantic 
clustering of your late-night searches, the algorithm classifies 
you as highly neurotic—making you a prime target for impulse-buy 
ad targeting."
```

---

### 1.3 Temporal Vulnerability Mapping

**What It Does:**
Analyzes WHEN you do things to find patterns of weakness (e.g., "You're most vulnerable to ads on Thursday nights at 11 PM").

**Implementation:**
```python
# parsers/temporal_vulnerability_mapper.py
import pandas as pd
from datetime import datetime
from collections import defaultdict

def map_temporal_vulnerabilities(google_data, instagram_data):
    """
    Identifies time windows when user is most susceptible to manipulation.
    """
    # Combine all timestamped activities
    activities = []
    
    for g in google_data:
        activities.append({
            'timestamp': datetime.fromisoformat(g['timestamp']),
            'type': 'search',
            'content': g['search_query']
        })
    
    for ig in instagram_data:
        activities.append({
            'timestamp': datetime.fromisoformat(ig['timestamp']),
            'type': 'instagram',
            'content': ig['interacted_account']
        })
    
    df = pd.DataFrame(activities)
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    
    # Find peak activity times
    hourly_counts = df.groupby('hour').size()
    daily_counts = df.groupby('day_of_week').size()
    
    # Identify vulnerability windows (high activity = high engagement = vulnerable)
    peak_hour = hourly_counts.idxmax()
    peak_day = daily_counts.idxmax()
    
    # Calculate vulnerability score
    vulnerability_heatmap = df.groupby(['day_of_week', 'hour']).size().reset_index(name='activity_count')
    vulnerability_heatmap['vulnerability_score'] = vulnerability_heatmap['activity_count'] / vulnerability_heatmap['activity_count'].max() * 100
    
    # Find top 3 most vulnerable windows
    top_vulnerabilities = vulnerability_heatmap.nlargest(3, 'vulnerability_score')
    
    return {
        "peak_hour": peak_hour,
        "peak_day": peak_day,
        "vulnerability_heatmap": vulnerability_heatmap.to_dict('records'),
        "top_vulnerabilities": top_vulnerabilities.to_dict('records'),
        "interpretation": f"Your willpower is statistically lowest on {peak_day}s around {peak_hour}:00. This is exactly when platforms push their most aggressive targeted ads."
    }
```

**Output Example:**
```
Temporal Vulnerability Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Peak Vulnerability: Thursday, 11 PM (Vulnerability Score: 94%)

Top 3 Vulnerable Windows:
1. Thursday 23:00 - 94% vulnerable
2. Friday 22:00 - 87% vulnerable  
3. Sunday 21:00 - 82% vulnerable

Interpretation:
"Your data shows your willpower is statistically lowest on 
Thursdays after 11:00 PM—this is exactly when Instagram pushes 
its most aggressive targeted ads to your feed."
```

---

## Layer 2: LangGraph Active Defense System

### 2.1 Architecture

**Multi-Agent System:**
1. **Vulnerability Assessor** - Analyzes inference engine output
2. **Poisoning Vector Agent** - Generates noise queries to break tracking
3. **Blindspot Generator** - Creates behavioral interventions
4. **Compiler** - Assembles final defense plan

**Tech Stack:**
- LangGraph for agent orchestration
- Ollama (local LLM) for generating countermeasures
- No external API calls - runs entirely offline

### 2.2 Implementation

**Key Innovation: Semantic Divergence**

Traditional privacy tools (like TrackMeNot) spam random dictionary words. Modern ad networks filter this out using anomaly detection. Instead, we use **Semantic Divergence** - the local LLM generates a highly credible, internally consistent "Anti-Persona" that executes alongside your real browsing.

If your data says you're an engineering student looking up deep learning, the poisoner creates a shadow trail making you look like a 45-year-old amateur botanist looking for real estate in Kerala.

#### LangGraph Multi-Agent System

```python
# parsers/active_defense_system.py
from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, END
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Initialize local LLM (optimized for VRAM constraints)
local_llm = Ollama(model="qwen:0.5b")  # Swap with your local model

class FirewallState(TypedDict):
    inferred_vulnerabilities: List[Dict]
    poisoning_strategy: Dict
    behavioral_interventions: List[str]
    final_shield_report: str

def vulnerability_assessor_node(state: FirewallState) -> Dict:
    """Analyze high-risk algorithmic links."""
    print("[+] Node 1: Assessing High-Risk Algorithmic Links...")
    vulns = state["inferred_vulnerabilities"]
    
    # Filter critical targets (>75% confidence)
    critical_targets = [v for v in vulns if v["Inference_Confidence"] > 75.0]
    
    return {"inferred_vulnerabilities": critical_targets}

def profile_poisoner_node(state: FirewallState) -> Dict:
    """
    Generate data poisoning vectors using Semantic Divergence.
    Creates credible anti-persona queries, not random noise.
    """
    print("[+] Node 2: Computing Profile Poisoning Decoys...")
    vulns = state.get("inferred_vulnerabilities", [])
    
    decoy_payloads = []
    
    # Prompt forces LLM to think like a human creating a specific, divergent profile
    poison_prompt = PromptTemplate(
        input_variables=["target_interest"],
        template="""
        You are a red-team privacy agent. The tracking algorithm thinks the user is highly interested in: '{target_interest}'.
        Generate 3 highly realistic, human-like Google search queries that suggest the exact OPPOSITE demographic or lifestyle. 
        The queries must look natural, not random.
        Output ONLY a valid JSON list of strings. No markdown, no explanations.
        """
    )
    
    for v in vulns:
        target = v["Inferred_Connection"]
        try:
            # Generate divergent queries locally
            response = local_llm.invoke(poison_prompt.format(target_interest=target))
            decoys = json.loads(response.strip())
            
            decoy_payloads.append({
                "target_to_dilute": target,
                "decoy_queries": decoys
            })
        except Exception as e:
            print(f"[-] Generation failed for {target}, using fallback noise.")
            decoy_payloads.append({
                "target_to_dilute": target,
                "decoy_queries": [
                    "best organic fertilizer for indoor plants",
                    "how to knit a scarf for beginners",
                    "retirement planning strategies for 50+"
                ]
            })
    
    return {"poisoning_strategy": {"status": "armed", "payloads": decoy_payloads}}

def blindspot_generator_node(state: FirewallState) -> Dict:
    """Generate behavioral modifications to bypass habit loops."""
    print("[+] Node 3: Mapping Temporal Blindspots...")
    
    # Use LLM to generate interventions
    prompt = """
    Based on the user's temporal vulnerability data, generate 3 specific 
    behavioral interventions to break algorithmic tracking patterns.
    
    Focus on:
    1. Separating cross-app sessions by 90+ minutes
    2. Introducing location noise during peak vulnerability windows
    3. Breaking time-based patterns with offline activities
    
    Format: Return actionable steps, one per line.
    """
    
    response = local_llm.invoke(prompt)
    interventions = response.strip().split('\n')
    
    return {"behavioral_interventions": interventions}

def compiler_node(state: FirewallState) -> Dict:
    """Compile final mitigation profile."""
    print("[+] Node 4: Compiling Active Defense Profile...")
    
    report = {
        "SHIELD_STATUS": "DEPLOYED",
        "MITIGATION_TARGETS": [v["Inferred_Connection"] for v in state["inferred_vulnerabilities"]],
        "POISONING_VECTORS": state["poisoning_strategy"]["payloads"],
        "BEHAVIORAL_COUNTER_MEASURES": state["behavioral_interventions"]
    }
    
    return {"final_shield_report": json.dumps(report, indent=2)}

# Build LangGraph workflow
workflow = StateGraph(FirewallState)

workflow.add_node("Assessor", vulnerability_assessor_node)
workflow.add_node("Poisoner", profile_poisoner_node)
workflow.add_node("Generator", blindspot_generator_node)
workflow.add_node("Compiler", compiler_node)

workflow.set_entry_point("Assessor")
workflow.add_edge("Assessor", "Poisoner")
workflow.add_edge("Assessor", "Generator")
workflow.add_edge("Poisoner", "Compiler")
workflow.add_edge("Generator", "Compiler")
workflow.add_edge("Compiler", END)

privacy_firewall_agent = workflow.compile()
```

#### Playwright Execution Engine

The poisoning agent generates queries, but we need to actually execute them. This is where **Playwright** comes in - it simulates human browsing behavior to inject the noise.

**Key Features:**
1. **Uses your actual browser profile** - so tracking cookies link to your real identity
2. **Simulates human behavior** - variable typing speed, random scrolling, dwell time
3. **Temporal jitter** - random delays between searches to evade anomaly detection
4. **Link traversal** - clicks into search results and reads content

```python
# parsers/shield_executor.py
import sys
import json
import asyncio
import random
from playwright.async_api import async_playwright

async def simulate_human_reading(page):
    """Simulates realistic dwell time by randomly scrolling down a page."""
    scroll_cycles = random.randint(2, 5)
    for _ in range(scroll_cycles):
        # Scroll down by variable pixels
        scroll_amount = random.randint(300, 700)
        await page.evaluate(f"window.scrollBy(0, {scroll_amount});")
        # Rest at new scroll position to simulate reading
        await asyncio.sleep(random.uniform(3.0, 12.0))

async def execute_poison_vector(query_list, user_profile_path=None):
    """
    Launches background browser session to execute semantic noise queries.
    
    Parameters:
    - query_list: List of string queries to execute
    - user_profile_path: Path to your local Chrome/Chromium user profile 
                         (Crucial so tracking cookies link to your actual profile)
    """
    async with async_playwright() as p:
        print("[+] Starting Headless Shield Engine...")
        
        # Launch persistent context to inherit active cookies
        if user_profile_path:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_profile_path,
                headless=True,  # Runs quietly in background
                args=["--disable-blink-features=AutomationControlled"]  # Evade bot detection
            )
        else:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        
        page = await context.new_page()
        
        for index, query in enumerate(query_list):
            try:
                print(f"[+] Injecting Noise Vector {index + 1}/{len(query_list)}: '{query}'")
                
                # Navigate to Google
                await page.goto("https://www.google.com", wait_until="networkidle")
                
                # Wait for search input
                search_box = await page.wait_for_selector("textarea[name='q']", state="visible")
                await search_box.click()
                
                # Type query with variable character delay (mimics human typing)
                for char in query:
                    await search_box.type(char)
                    await asyncio.sleep(random.uniform(0.05, 0.25))
                
                # Submit query
                await search_box.press("Enter")
                await page.wait_for_load_state("networkidle")
                
                # Extract first-page organic links (exclude Google internal links)
                await page.wait_for_selector("div.g")
                links = await page.locator("div.g a").all()
                
                valid_links = [
                    await link.get_attribute("href") 
                    for link in links 
                    if await link.get_attribute("href")
                ]
                valid_links = [l for l in valid_links if l and "google.com" not in l and "youtube.com" not in l]
                
                if valid_links:
                    # Select random destination from top results
                    target_link = random.choice(valid_links[:4])
                    print(f"    [->] Navigating to: {target_link}")
                    
                    # Open target page
                    await page.goto(target_link, wait_until="load", timeout=15000)
                    
                    # Dwell on site to confirm interest to tracking pixels
                    await simulate_human_reading(page)
                
            except Exception as e:
                print(f"    [-] Error executing vector: {str(e)}")
                continue
            
            # Anti-signature temporal jitter between searches
            inter_search_delay = random.uniform(15.0, 60.0)
            print(f"[+] Cooling down for {round(inter_search_delay, 2)}s...")
            await asyncio.sleep(inter_search_delay)
        
        await context.close()
        print("[+] Poisoning batch complete. Shield Engine sleeping.")

if __name__ == "__main__":
    # Accept queries via command line
    if len(sys.argv) > 1:
        queries = json.loads(sys.argv[1])
    else:
        queries = [
            "organic farming techniques",
            "how to build a greenhouse",
            "permaculture design basics"
        ]
    
    asyncio.run(execute_poison_vector(queries))
```

#### Deployment Controller

Connects LangGraph output to Playwright execution:

```python
# parsers/deploy_defense.py
import subprocess
import json
from pathlib import Path

def deploy_active_defense(state: dict):
    """
    Extracts semantic decoys from LangGraph state and dispatches
    background Playwright automation process.
    """
    strategy = state.get("poisoning_strategy", {})
    if strategy.get("status") != "armed":
        print("[-] Active poisoning system not armed. Aborting.")
        return state
    
    payloads = strategy.get("payloads", [])
    
    # Flatten all decoy queries into single batch
    all_decoy_queries = []
    for payload in payloads:
        all_decoy_queries.extend(payload.get("decoy_queries", []))
    
    if not all_decoy_queries:
        print("[-] No valid decoy vectors found.")
        return state
    
    # Serialize for shell arguments
    queries_json_str = json.dumps(all_decoy_queries)
    
    # Locate script path
    script_path = Path(__file__).parent / "shield_executor.py"
    
    print(f"[+] Dispatching Shield Automation with {len(all_decoy_queries)} payloads...")
    
    # Launch as detached subprocess (non-blocking)
    subprocess.Popen(
        ["python", str(script_path), queries_json_str],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True  # Detaches execution
    )
    
    return state
```

**Why This Evades Detection:**

1. **Dynamic Dwell Time** - Variable scrolling + reading time satisfies scroll-depth tracking
2. **Link Traversal** - Clicks into results, not just searches (higher value to ad bidders)
3. **Temporal Jitter** - Random delays between actions break pattern matching
4. **Profile Persistence** - Uses your actual cookies so noise attaches to your real profile

---

## Layer 3: Active Mitigation Output

### 3.1 Noise Injection Script

**What It Does:**
Generates a Selenium script that automatically searches for decoy queries to poison your ad profile.

**Output:**
```python
# output/noise_injector.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

# Decoy queries generated by Poisoning Vector Agent
DECOY_QUERIES = [
    "luxury yacht rentals",
    "private jet charter services",
    "golf club memberships",
    # ... (opposite of your actual interests)
]

def inject_noise():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    
    for query in DECOY_QUERIES:
        search_box = driver.find_element("name", "q")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Random delay to appear human
        time.sleep(random.uniform(5, 15))
    
    driver.quit()
    print("[+] Noise injection complete. Ad profile poisoned.")

if __name__ == "__main__":
    inject_noise()
```

### 3.2 Ad-Shield Schedule

**What It Does:**
Creates a calendar of specific times to avoid using apps based on vulnerability mapping.

**Output:**
```
AD-SHIELD SCHEDULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 HIGH RISK WINDOWS (Avoid Instagram/Google):
   - Thursday 23:00-00:00 (Vulnerability: 94%)
   - Friday 22:00-23:00 (Vulnerability: 87%)
   - Sunday 21:00-22:00 (Vulnerability: 82%)

🟡 MEDIUM RISK WINDOWS (Use with caution):
   - Weekday evenings 19:00-21:00
   - Weekend mornings 10:00-12:00

🟢 SAFE WINDOWS (Normal usage):
   - Weekday mornings 08:00-12:00
   - Weekday afternoons 14:00-17:00
```

### 3.3 Behavioral Interventions

**What It Does:**
Specific actions to break tracking patterns.

**Output:**
```
BEHAVIORAL COUNTER-MEASURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. CROSS-APP SEPARATION
   Action: Separate Google and Instagram sessions by 90+ minutes
   Why: Breaks temporal co-occurrence bridges used for shadow profiling
   
2. LOCATION NOISE
   Action: Disable location services during peak vulnerability windows
   Why: Prevents location-based targeting during weak moments
   
3. HABIT LOOP DISRUPTION
   Action: Replace Thursday 11 PM screen time with 20 min offline activity
   Why: Breaks the strongest tracking pattern in your data
   
4. SEARCH DIVERSIFICATION
   Action: Run noise injection script 2x per week
   Why: Dilutes your true behavioral matrix
```

---

## Web Interface Design

### Landing Page

```
┌─────────────────────────────────────────────────┐
│                                                 │
│         🔴 PRIVACY WRAPPED 2.0                  │
│    "They Don't Just Track You. They Know You."  │
│                                                 │
│      ┌─────────────────────────────────┐       │
│      │   DROP YOUR DATA EXPORTS        │       │
│      │                                 │       │
│      │   📁 Instagram ZIP              │       │
│      │   📁 Google Takeout ZIP         │       │
│      └─────────────────────────────────┘       │
│                                                 │
│   [Analyze My Surveillance Profile]            │
│   [Try Demo]                                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Results Dashboard

**3 Tabs:**

**Tab 1: Inference Report**
- Shadow network visualization (NetworkX graph)
- Psychographic profile (Big Five traits)
- Temporal vulnerability heatmap

**Tab 2: Active Defense**
- Poisoning vectors (decoy queries)
- Ad-shield schedule
- Behavioral interventions

**Tab 3: Download Tools**
- Noise injection script (Python)
- Browser extension (Chrome/Firefox)
- Calendar file (.ics) with shield schedule

---

## Implementation Plan

### Week 1: Inference Engine
- [ ] Implement shadow network profiler (NetworkX + Adamic-Adar)
- [ ] Implement psychographic profiler (embeddings + clustering)
- [ ] Implement temporal vulnerability mapper
- [ ] Test with real Instagram/Google data
- [ ] Create JSON output format

### Week 2: Active Defense System
- [ ] Set up LangGraph workflow
- [ ] Install Ollama locally
- [ ] Implement 4 agent nodes
- [ ] Test poisoning vector generation
- [ ] Test behavioral intervention generation

### Week 3: Web Interface
- [ ] Build HTML/CSS/JS frontend
- [ ] Implement file upload and processing
- [ ] Create 3-tab results dashboard
- [ ] Add NetworkX graph visualization (D3.js)
- [ ] Add download buttons for tools

### Week 4: Polish & Launch
- [ ] Generate noise injection script automatically
- [ ] Create browser extension (optional)
- [ ] Write documentation
- [ ] Create demo video
- [ ] Launch on Reddit, Twitter, Product Hunt

---

## Success Metrics

### Technical Excellence
- [ ] Shadow profiling achieves >80% confidence on real data
- [ ] Psychographic profiling maps to at least 3 Big Five traits
- [ ] Temporal vulnerability identifies top 3 weak windows
- [ ] LangGraph agents generate actionable countermeasures

### Portfolio Impact
- [ ] Demonstrates advanced ML (graph algorithms, clustering, embeddings)
- [ ] Shows multi-agent system design (LangGraph)
- [ ] Proves real-world problem solving (active defense)
- [ ] Includes research citations (academic rigor)

### Viral Potential
- [ ] 1000+ users in first month
- [ ] Featured on privacy blogs/subreddits
- [ ] GitHub stars >500
- [ ] Media coverage (TechCrunch, Wired, etc.)

---

## Why This Is Better Than Desktop App

1. **No installation barrier** - runs in browser
2. **Real ML on existing data** - no need to collect from 1000 users first
3. **Active defense** - not just passive reporting
4. **Portfolio gold** - shows advanced DS/ML skills
5. **Research-backed** - cites academic papers
6. **Ethical impact** - actually helps people fight surveillance

---

## Tech Stack Summary

**Backend:**
- Python 3.11+
- NetworkX (graph algorithms)
- scikit-learn (clustering)
- pandas, numpy (data processing)
- LangGraph (multi-agent orchestration)
- Ollama (local LLM)

**Frontend:**
- HTML/CSS/JavaScript
- D3.js (graph visualization)
- Chart.js (heatmaps)

**Deployment:**
- Vercel/Netlify (static hosting)
- Client-side processing (no server needed)

---

## Next Steps

1. Review this spec
2. Invoke writing-plans skill to create implementation plan
3. Start building Layer 1 (Inference Engine)
4. Test with your real data
5. Build Layer 2 (Active Defense)
6. Create web interface
7. Launch and go viral

**This is the real project. This is what goes on your resume.**
