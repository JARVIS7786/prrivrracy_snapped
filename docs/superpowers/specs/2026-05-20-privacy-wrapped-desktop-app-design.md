# Privacy Wrapped Desktop App - Design Specification

**Date:** 2026-05-20  
**Project:** Privacy Wrapped  
**Goal:** Transform Privacy Wrapped from a local Python script into a viral desktop app that collects real user data for ML analysis

---

## Executive Summary

Privacy Wrapped will become a portable Windows desktop application (.exe) that makes it dead simple for users to analyze their Instagram and Google data exports. The app features a dark "Gotham investigation board" aesthetic with dramatic animations. After users see their surveillance profile, they're prompted to share anonymized aggregate statistics. Once we collect data from 100+ users, we'll build real ML models (clustering, prediction, anomaly detection) on actual behavioral data.

**Core Strategy:** Make it viral first → collect real data → then do real ML.

---

## Technical Architecture

### Stack

- **Frontend:** Tauri (Rust-based) + HTML/CSS/JavaScript
- **Backend:** Python (existing parsers + FastAPI layer)
- **Communication:** Tauri IPC commands → Python subprocess via HTTP
- **Packaging:** Tauri bundler → portable .exe (~40-60MB)
- **Data Storage:** Supabase (PostgreSQL, free tier) for anonymous stats

### Project Structure

```
privacy-wrapped/
├── src-tauri/              # Rust backend (Tauri)
│   ├── src/
│   │   └── main.rs         # Tauri commands, Python subprocess management
│   ├── tauri.conf.json     # App configuration
│   ├── Cargo.toml          # Rust dependencies
│   └── icons/              # App icons
├── src/                    # Frontend (HTML/CSS/JS)
│   ├── index.html          # Investigation board UI
│   ├── styles.css          # Gotham dark theme
│   ├── app.js              # Frontend logic
│   └── assets/             # Images, fonts, animations
├── python-backend/         # New Python API layer
│   ├── main.py             # FastAPI server
│   ├── requirements.txt    # Python dependencies
│   └── build.py            # PyInstaller build script
├── parsers/                # Existing Python parsers (unchanged)
│   ├── instagram_parser.py
│   ├── google_parser.py
│   ├── feature_engineering.py
│   ├── gemini_embeddings.py
│   ├── knowledge_graph.py
│   └── rtb_simulator.py
├── docs/                   # Documentation
└── dist/                   # Built .exe output
```

---

## Component Design

### 1. Frontend - Investigation Board UI

**Design Philosophy:**
- Dark Gotham aesthetic (#050505 background, red/green accents)
- Feels like a detective's conspiracy board
- Dramatic reveals with animations
- Screenshot-friendly for social sharing

**Screen Flow:**

#### Landing Screen
```
┌─────────────────────────────────────────────────┐
│                                                 │
│              PRIVACY WRAPPED                    │
│         "What They Know About You"              │
│                                                 │
│        [Dark room with spotlight effect]        │
│                                                 │
│      ┌─────────────────────────────────┐       │
│      │   DROP EVIDENCE HERE            │       │
│      │                                 │       │
│      │   📁 Instagram ZIP              │       │
│      │   📁 Google Takeout ZIP         │       │
│      │                                 │       │
│      │   Drag files or click to browse │       │
│      └─────────────────────────────────┘       │
│                                                 │
│        [Try Demo]    [How It Works]            │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Features:**
- Drag-and-drop zones with hover effects
- Auto-detect file types (Instagram vs Google)
- "Try Demo" loads pre-generated Rahul's data
- "How It Works" shows 3-step explainer

#### Processing Screen
```
┌─────────────────────────────────────────────────┐
│   ANALYZING DIGITAL FOOTPRINT...                │
│                                                 │
│   [Animated scan lines moving across screen]   │
│   [Matrix-style data streams in background]    │
│                                                 │
│   ✓ Parsing Instagram data...                  │
│   ✓ Extracting advertiser network...           │
│   ⟳ Building surveillance graph...             │
│   ⏳ Calculating your worth...                  │
│   ⏳ Generating AI roast...                     │
│                                                 │
│   [Progress bar: 67%]                           │
└─────────────────────────────────────────────────┘
```

**Features:**
- Real-time progress updates from Python backend
- Animated checkmarks as tasks complete
- Glitch effects during transitions
- Takes 30-60 seconds (builds anticipation)

#### Investigation Board (Results)
```
┌─────────────────────────────────────────────────┐
│   YOUR SURVEILLANCE PROFILE                     │
│                                                 │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│   │  5,881   │  │ ₹165,402 │  │ 14 DAYS  │    │
│   │ TRACKERS │  │  VALUE   │  │  EARLY   │    │
│   └──────────┘  └──────────┘  └──────────┘    │
│                                                 │
│   [Red strings connecting data points]         │
│   [Interactive knowledge graph]                 │
│   [RTB auction visualization]                   │
│   [AI-generated roast text]                     │
│                                                 │
│   ┌─────────────────────────────────────────┐  │
│   │ "By day: solving for x.                 │  │
│   │  By night: the algorithm solved for YOU"│  │
│   └─────────────────────────────────────────┘  │
│                                                 │
│   [Share Anonymously] [Download Report] [Tweet]│
└─────────────────────────────────────────────────┘
```

**Interactive Elements:**
- Hover over nodes to see details
- Click advertisers to see what they know
- Scroll to reveal more sections
- Animated counters (0 → 5,881)
- Pulsing red alerts for shocking stats

**Visual Effects:**
- Particle system (floating data points)
- Glitch effects on reveal
- Red "surveillance strings" animate in
- Fade-in transitions for each section
- CRT monitor scan lines

---

### 2. Backend Architecture

#### Python API Layer (`python-backend/main.py`)

FastAPI server that Tauri calls via HTTP:

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import sys
import os
import tempfile
import shutil
import json

sys.path.append('../parsers')
from instagram_parser import parse_instagram
from google_parser import parse_google
from feature_engineering import build_feature_matrix
from gemini_embeddings import generate_embeddings
from knowledge_graph import build_knowledge_graph
from rtb_simulator import simulate_auction
from ai_roast_generator import generate_roast

app = FastAPI()

@app.post("/analyze")
async def analyze_data(
    instagram_zip: UploadFile = File(None),
    google_zip: UploadFile = File(None)
):
    """
    Main analysis endpoint.
    Returns: JSON with all results + progress updates via SSE
    """
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1. Extract ZIPs
        yield {"status": "extracting", "progress": 10}
        
        # 2. Run parsers
        yield {"status": "parsing_instagram", "progress": 25}
        ig_data = parse_instagram(temp_dir)
        
        yield {"status": "parsing_google", "progress": 40}
        google_data = parse_google(temp_dir)
        
        # 3. Feature engineering
        yield {"status": "building_features", "progress": 55}
        features = build_feature_matrix(ig_data, google_data)
        
        # 4. Knowledge graph
        yield {"status": "building_graph", "progress": 70}
        graph = build_knowledge_graph(ig_data, google_data, features)
        
        # 5. RTB simulation
        yield {"status": "simulating_auction", "progress": 85}
        rtb_results = simulate_auction(features)
        
        # 6. AI roast
        yield {"status": "generating_roast", "progress": 95}
        roast = generate_roast(ig_data, google_data, features)
        
        # 7. Return complete results
        yield {
            "status": "complete",
            "progress": 100,
            "data": {
                "instagram": ig_data,
                "google": google_data,
                "features": features,
                "graph": graph,
                "rtb": rtb_results,
                "roast": roast
            }
        }
        
    finally:
        shutil.rmtree(temp_dir)

@app.post("/submit-anonymous")
async def submit_stats(data: dict):
    """
    Submit anonymized aggregate statistics to Supabase.
    """
    # Validate data structure
    required_fields = ["country", "region", "stats"]
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields"}
    
    # Send to Supabase
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    result = supabase.table("user_stats").insert({
        "timestamp": datetime.now().isoformat(),
        "country": data["country"],
        "region": data["region"],
        "advertiser_count": data["stats"]["advertiser_count"],
        "top_industries": data["stats"]["top_industries"],
        "affinity_scores": data["stats"]["affinity_scores"],
        "demographics": data["stats"]["demographics"],
        "platforms": data["stats"]["platforms"],
        "annual_value_inr": data["stats"]["annual_value_inr"]
    }).execute()
    
    return {"success": True}

@app.get("/demo")
async def get_demo_data():
    """
    Return pre-generated demo data (Rahul's profile).
    """
    demo_files = [
        "../output/demo_instagram_data.json",
        "../output/demo_google_data.json",
        "../output/demo_user_feature_matrix.json",
        "../output/demo_rtb_results.json"
    ]
    
    demo_data = {}
    for file in demo_files:
        with open(file) as f:
            key = os.path.basename(file).replace("demo_", "").replace(".json", "")
            demo_data[key] = json.load(f)
    
    return demo_data

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

**Key Design Decisions:**
- Server-Sent Events (SSE) for progress streaming
- Temp directory for file processing, auto-cleanup
- All existing parsers work unchanged
- Graceful error handling with cleanup

#### Tauri Commands (`src-tauri/src/main.rs`)

```rust
use tauri::command;
use std::process::{Command, Stdio};
use reqwest;

// Start Python FastAPI server as subprocess
fn start_python_server() -> std::process::Child {
    Command::new("python-backend/main.exe")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("Failed to start Python backend")
}

#[command]
async fn process_files(
    instagram_path: String,
    google_path: String
) -> Result<String, String> {
    // 1. Ensure Python server is running
    let server_url = "http://localhost:8000";
    
    // 2. Upload files via multipart form
    let client = reqwest::Client::new();
    let form = reqwest::multipart::Form::new()
        .file("instagram_zip", instagram_path)
        .map_err(|e| e.to_string())?
        .file("google_zip", google_path)
        .map_err(|e| e.to_string())?;
    
    // 3. Stream progress updates
    let response = client
        .post(format!("{}/analyze", server_url))
        .multipart(form)
        .send()
        .await
        .map_err(|e| e.to_string())?;
    
    // 4. Return final JSON
    let result = response.text().await.map_err(|e| e.to_string())?;
    Ok(result)
}

#[command]
async fn submit_anonymous_data(stats: String) -> Result<(), String> {
    let client = reqwest::Client::new();
    client
        .post("http://localhost:8000/submit-anonymous")
        .body(stats)
        .send()
        .await
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[command]
async fn load_demo() -> Result<String, String> {
    let client = reqwest::Client::new();
    let response = client
        .get("http://localhost:8000/demo")
        .send()
        .await
        .map_err(|e| e.to_string())?;
    
    let result = response.text().await.map_err(|e| e.to_string())?;
    Ok(result)
}

fn main() {
    // Start Python server on app launch
    let _python_server = start_python_server();
    
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            process_files,
            submit_anonymous_data,
            load_demo
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Data Flow:**
```
User drops files
     ↓
Frontend (JS) calls Tauri command
     ↓
Rust receives files → HTTP POST to Python FastAPI
     ↓
Python parsers process data (existing code)
     ↓
JSON results stream back: Rust → Frontend
     ↓
Investigation board renders with animations
```

---

### 3. Anonymous Data Collection

**What Gets Collected:**

```json
{
  "timestamp": "2026-05-20T16:08:17Z",
  "country": "IN",
  "region": "Maharashtra",
  "stats": {
    "advertiser_count": 5881,
    "top_industries": ["Tech & Apps", "Fashion", "Education"],
    "affinity_scores": {
      "cricket": 0.455,
      "coding": 0.545,
      "bollywood": 1.0,
      "spiritual": 0.273,
      "shopping": 0.818
    },
    "demographics": {
      "is_single": true,
      "is_educated": true,
      "is_engaged_shopper": true,
      "potential_device_change": false
    },
    "platforms": ["instagram", "google"],
    "annual_value_inr": 165401
  }
}
```

**What's NOT Collected:**
- No actual search queries
- No advertiser names
- No locations
- No timestamps of activity
- No personal identifiers

**Storage: Supabase**

Table schema:
```sql
CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    country VARCHAR(2),
    region VARCHAR(100),
    advertiser_count INTEGER,
    top_industries JSONB,
    affinity_scores JSONB,
    demographics JSONB,
    platforms JSONB,
    annual_value_inr INTEGER
);

CREATE INDEX idx_timestamp ON user_stats(timestamp);
CREATE INDEX idx_country ON user_stats(country);
```

**Consent Flow:**

After report loads, wait 2 seconds, then show modal:

```
┌─────────────────────────────────────────────────┐
│   Help Improve Privacy Wrapped                  │
│                                                 │
│   You just discovered 5,881 companies          │
│   tracking you. Share your anonymized stats    │
│   to help others understand surveillance?      │
│                                                 │
│   ✓ No personal data shared                    │
│   ✓ Just counts and categories                 │
│   ✓ Helps build real ML models                 │
│   ✓ View exactly what gets sent                │
│                                                 │
│   [View Data] [Share Anonymously] [No Thanks]  │
└─────────────────────────────────────────────────┘
```

**"View Data" shows:**
```json
{
  "country": "IN",
  "advertiser_count": 5881,
  "top_industries": ["Tech", "Fashion", "Education"],
  ...
}
```

**Privacy Guarantees:**
- No IP addresses stored
- No device fingerprinting
- No tracking cookies
- Open source (users can verify)

---

### 4. Social Sharing Features

#### Auto-Generated Share Cards

**Twitter/X Card:**
```
🔴 PRIVACY WRAPPED 2026

5,881 companies are tracking me
💰 My data is worth ₹165,402/year
🎯 They knew I was job hunting 14 days early

The algorithm already solved for you.

Get your report: privacy-wrapped.app

[Dark card image with key stats]
```

**Instagram Story Template:**
```
┌─────────────────┐
│  PRIVACY        │
│  WRAPPED        │
│                 │
│  5,881          │
│  TRACKERS       │
│                 │
│  ₹165K          │
│  ANNUAL VALUE   │
│                 │
│  Get yours →    │
└─────────────────┘
```

**Implementation:**
```javascript
function generateShareCard(stats) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Dark background
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, 1200, 630);
    
    // Red accent
    ctx.fillStyle = '#ff2a2a';
    ctx.font = 'bold 72px Space Grotesk';
    ctx.fillText('PRIVACY WRAPPED', 100, 150);
    
    // Stats
    ctx.fillStyle = '#ffffff';
    ctx.font = '48px Space Grotesk';
    ctx.fillText(`${stats.advertiser_count} TRACKERS`, 100, 300);
    ctx.fillText(`₹${stats.annual_value} VALUE`, 100, 400);
    
    return canvas.toDataURL();
}
```

#### Comparison Mode (v1.1)

```
YOU vs AVERAGE USER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Advertisers:     5,881  vs  2,340  (+151%)
Data Value:    ₹165K   vs  ₹78K   (+112%)
Top Category:  Bollywood vs Tech
Tracking Days:   847    vs  412    (+106%)
```

**Requires 100+ submissions to calculate averages.**

#### Leaderboard (v1.1)

```
TOP 10 MOST TRACKED USERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. User_8f3a2  →  12,847 trackers  →  ₹412K
2. User_9d1b7  →  11,203 trackers  →  ₹387K
3. User_2c5e9  →  10,891 trackers  →  ₹356K
...
```

**Privacy:** Users are anonymized (random IDs), opt-in only.

---

### 5. AI-Generated Roast

**Using Gemini API:**

```python
def generate_roast(instagram_data, google_data, features):
    """
    Generate a Spotify Wrapped-style roast using Gemini.
    """
    prompt = f"""
You are a sarcastic AI analyzing someone's digital surveillance profile.

Data:
- {features['advertiser_pressure']} companies tracking them
- Top interests: {', '.join(get_top_interests(features))}
- Demographics: {format_demographics(features['demographics'])}
- Annual data value: ₹{features.get('annual_value', 0)}
- Top advertiser categories: {instagram_data.get('top_categories', [])}

Write a 3-paragraph roast in the style of Spotify Wrapped:

1. **Algorithm Personality** - What their digital behavior reveals about them (day vs night persona)
2. **The Invisible Bubble** - What they're NOT being shown due to filter bubbles
3. **The Punchline** - A savage but funny conclusion about how predictable they are

Tone: Slightly terrifying but entertaining. Make it personal but not mean.
Length: 150-200 words total.

Example style:
"By day: a high-functioning logic machine sweating over Python tuples. By night: the mask slips. The math stops. The thirst begins."
"""
    
    response = genai.generate_content(prompt)
    return response.text
```

**Example Output:**

> **YOUR ALGORITHM PERSONALITY**
> 
> By day: a high-functioning logic machine sweating over Python tuples and complex algebraic expressions. By night: the mask slips. The math stops. The thirst begins. Instagram has you filed under "Engaged Shopper" and "Relationship Status: Single" — they're not guessing, they're watching.
> 
> **THE INVISIBLE BUBBLE**
> 
> Because you're trapped in the feedback loop the algorithm built for you, here's what you're NOT being shown: original thoughts outside your niche, content that might make you question your habits, silence. If we let you be bored, you might delete the app. We can't have that.
> 
> **THE PUNCHLINE**
> 
> The algorithm already solved for you — and it turns out you're just a predictable mix of algebra, cricket stats, and a very specific Bollywood crush. 5,881 companies bid on you every day. You were paid ₹0.00.

---

### 6. Deployment & Distribution

#### Build Process

**1. Bundle Python Backend:**
```bash
cd python-backend
pip install pyinstaller
pyinstaller --onefile --add-data "../parsers:parsers" main.py
# Output: dist/main.exe (~30MB)
```

**2. Build Tauri App:**
```bash
cd ..
npm install
cargo tauri build
# Output: src-tauri/target/release/privacy-wrapped.exe (~50MB total)
```

**3. Create Portable .exe:**
- Tauri bundles Python .exe inside
- Single file, no installation needed
- Just download and double-click

#### Distribution Strategy

**GitHub Releases:**
- Host .exe on GitHub Releases
- Automatic versioning
- Download stats tracking

**Landing Page:**
- Domain: `privacy-wrapped.app` (or `.vercel.app`)
- One-page site with:
  - Hero: "What do Instagram and Google know about you?"
  - Demo video (30 seconds)
  - Download button (Windows .exe)
  - How it works (3 steps)
  - FAQ
  - GitHub link

**Social Launch:**
- Post on Twitter/X with demo video
- Reddit: r/privacy, r/india, r/dataisbeautiful
- Product Hunt launch
- WhatsApp/Telegram groups (college, tech communities)

**File Size Optimization:**
- Target: Under 100MB (WhatsApp limit: 100MB)
- Compress Python runtime
- Remove unnecessary dependencies
- Use UPX for .exe compression

#### Auto-Updates

**Tauri Built-in Updater:**
```rust
// tauri.conf.json
{
  "updater": {
    "active": true,
    "endpoints": [
      "https://github.com/username/privacy-wrapped/releases/latest/download/latest.json"
    ],
    "dialog": true,
    "pubkey": "YOUR_PUBLIC_KEY"
  }
}
```

**Update Flow:**
1. App checks for updates on launch
2. If new version available, show dialog
3. Download in background
4. Prompt to restart and install

---

### 7. Development Phases

#### Week 1-2: Core App Foundation

**Tasks:**
- [ ] Set up Tauri project structure
- [ ] Create basic UI (landing screen, drop zones)
- [ ] Implement Python subprocess management
- [ ] Build FastAPI server with /analyze endpoint
- [ ] Test file upload and processing pipeline
- [ ] Create investigation board HTML/CSS
- [ ] Implement progress streaming (SSE)

**Deliverable:** Working app that processes files and shows basic results.

#### Week 3: Social Features

**Tasks:**
- [ ] Implement anonymous data submission
- [ ] Set up Supabase database
- [ ] Create consent modal UI
- [ ] Build share card generator
- [ ] Add demo mode
- [ ] Implement AI roast generation
- [ ] Create Twitter/Instagram share templates

**Deliverable:** App with full social sharing and data collection.

#### Week 4: Polish & Launch

**Tasks:**
- [ ] Add animations and visual effects
- [ ] Implement error handling and edge cases
- [ ] Create landing page
- [ ] Write documentation
- [ ] Test on multiple Windows versions
- [ ] Build portable .exe
- [ ] Create demo video
- [ ] Launch on Product Hunt, Reddit, Twitter

**Deliverable:** Production-ready app ready for viral distribution.

---

## Success Metrics

### Phase 1: Launch (Week 1-4)
- [ ] 100 downloads in first week
- [ ] 50 anonymous data submissions
- [ ] 10 social shares (Twitter/Instagram)

### Phase 2: Growth (Month 2-3)
- [ ] 1,000 total downloads
- [ ] 500 anonymous data submissions
- [ ] 100 social shares
- [ ] Featured on 1 tech blog/publication

### Phase 3: ML Ready (Month 4+)
- [ ] 5,000+ downloads
- [ ] 2,000+ data submissions
- [ ] Enough data for real ML models:
  - User clustering (identify personas)
  - Advertiser targeting prediction
  - Anomaly detection (unusual tracking patterns)
  - Geographic surveillance differences

---

## Future Enhancements (Post-Launch)

### v1.1 - Comparison & Leaderboard
- Compare your stats vs average user
- Leaderboard of most tracked users
- Regional comparisons (Mumbai vs Delhi vs Bangalore)

### v1.2 - More Platforms
- Twitter/X data export parser
- LinkedIn data export parser
- Facebook data export parser

### v1.3 - Real ML Models
- User clustering (K-means, DBSCAN)
- Advertiser targeting prediction (Random Forest)
- Anomaly detection (Isolation Forest)
- Time series forecasting (LSTM)

### v1.4 - Web Version
- Browser-based version (no download needed)
- Client-side processing (JavaScript parsers)
- Hosted on Vercel/Netlify

### v2.0 - Mobile App
- React Native or Flutter
- iOS + Android
- Direct integration with Instagram/Google APIs (if possible)

---

## Technical Risks & Mitigations

### Risk 1: Python Subprocess Fails
**Mitigation:** 
- Bundle Python runtime with PyInstaller
- Test on clean Windows VMs
- Provide detailed error messages
- Fallback to demo mode if processing fails

### Risk 2: Large File Processing (>500MB)
**Mitigation:**
- Stream file processing (don't load entire ZIP into memory)
- Show progress bar
- Set timeout limits (5 minutes max)
- Provide file size warnings

### Risk 3: Gemini API Rate Limits
**Mitigation:**
- Cache roast results
- Implement exponential backoff
- Fallback to pre-written roasts if API fails
- Consider local LLM (Ollama) for offline mode

### Risk 4: Low Adoption Rate
**Mitigation:**
- Make demo mode prominent (no data upload needed)
- Create viral demo video
- Incentivize sharing (unlock features after sharing)
- Partner with privacy advocates/influencers

### Risk 5: Privacy Concerns
**Mitigation:**
- Open source the entire codebase
- Clear privacy policy
- Show exactly what data gets collected
- No tracking, no analytics (except anonymous stats)
- Verifiable builds (reproducible)

---

## Open Questions

1. **Gemini API Costs:** How many free API calls do we get? Need to budget for roast generation.
2. **Supabase Limits:** Free tier allows 500MB database. Will this be enough for 1,000+ submissions?
3. **Windows Defender:** Will the .exe get flagged as malware? Need to sign the binary.
4. **File Size:** Can we get under 100MB for WhatsApp sharing?
5. **Mac/Linux Support:** Should we prioritize cross-platform from day 1, or Windows-only first?

---

## Conclusion

This design transforms Privacy Wrapped from a local Python script into a viral desktop app that:

1. **Makes it dead simple** for users to analyze their data (drag-and-drop, no terminal)
2. **Looks stunning** (Gotham investigation board aesthetic, dramatic animations)
3. **Collects real data** (anonymized aggregate stats from real users)
4. **Enables real ML** (once we have 100+ submissions, build actual models)

The strategy is: **viral first, ML second**. This is how real data products work.

**Next Steps:** Write implementation plan and start building.
