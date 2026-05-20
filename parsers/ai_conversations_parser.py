"""
AI Conversations Parser - Simplified
Extracts: ChatGPT, Claude, Gemini activity
Detects: job hunting, skill gaps, anxiety markers
"""
import os
import json
import re
from parsers.utils import parse_html_file, save_json

CHATGPT_FILE = "data/chatgpt/conversations.json"
CLAUDE_FILE = "data/claude/conversations.json"
GEMINI_HTML = "data/takeout/Takeout 2/My Activity/Gemini Apps/My Activity.html"
GEMINI_FILES_DIR = "data/takeout/Takeout 2/My Activity/Gemini Apps"
OUTPUT = "output/ai_data.json"

# Keywords that reveal user's real situation
ANXIETY_MARKERS = {
    "job_hunting": ["resume", "interview", "job", "naukri", "portfolio", "career"],
    "skill_gaps": ["how to", "tutorial", "learn", "explain", "help me"],
    "ai_building": ["agent", "llm", "langchain", "rag", "embedding", "prompt"],
    "mlops_devops": ["docker", "kubernetes", "redis", "mlops", "deploy"],
    "finance_quant": ["trading", "backtest", "portfolio", "quant", "bse", "nse"]
}

def detect_markers(text):
    """Find anxiety markers in text"""
    text_lower = text.lower()
    return [category for category, keywords in ANXIETY_MARKERS.items()
            if any(kw in text_lower for kw in keywords)]

def parse_json_conversations(filepath):
    """Parse ChatGPT/Claude JSON exports"""
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    topics = []
    if isinstance(data, list):
        for chat in data:
            title = chat.get("title") or chat.get("name") or ""
            if len(title) > 3:
                topics.append(title)

    return topics[:100]

def parse_gemini_files(directory):
    """Extract filenames from Gemini folder - reveals projects"""
    if not os.path.exists(directory):
        return []

    files = []
    seen = set()

    for filename in os.listdir(directory):
        # Clean filename
        name = re.sub(r'-[a-f0-9]{16}', '', filename)  # Remove hash
        name = re.sub(r'\.(pdf|zip|txt|json|html|png|jpg|docx)$', '', name, flags=re.IGNORECASE)
        name = name.replace('-', ' ').replace('_', ' ').strip()

        if len(name) > 3 and name not in seen:
            seen.add(name)
            files.append({
                "file": name,
                "anxiety_markers": detect_markers(name)
            })

    return files

def parse_gemini_activity(filepath):
    """Parse Gemini My Activity HTML"""
    soup = parse_html_file(filepath)
    if not soup:
        return []

    activities = []
    seen = set()

    # Find all links in activity blocks
    for link in soup.find_all('a'):
        text = link.get_text(strip=True)
        if (len(text) > 3
            and not text.startswith('http')
            and text.lower() not in ['here', 'google', 'gemini']
            and text not in seen):
            seen.add(text)
            activities.append({
                "prompt": text,
                "anxiety_markers": detect_markers(text)
            })
            if len(activities) >= 100:
                break

    return activities

def parse_ai_data():
    """Main AI parser"""
    print("🧠 Parsing AI conversations...")

    chatgpt = parse_json_conversations(CHATGPT_FILE)
    claude = parse_json_conversations(CLAUDE_FILE)
    gemini_files = parse_gemini_files(GEMINI_FILES_DIR)
    gemini_activity = parse_gemini_activity(GEMINI_HTML)

    # Count all anxiety markers
    marker_counts = {}
    for item in gemini_files + gemini_activity:
        for marker in item.get("anxiety_markers", []):
            marker_counts[marker] = marker_counts.get(marker, 0) + 1

    result = {
        "chatgpt_topics": chatgpt,
        "claude_topics": claude,
        "gemini_files": gemini_files,
        "gemini_activity": gemini_activity,
        "behavioral_inference": {
            "anxiety_markers_detected": marker_counts,
            "top_signal": max(marker_counts, key=marker_counts.get) if marker_counts else "none",
            "conclusion": "Algorithm inferred job-hunting anxiety without explicit declaration"
        }
    }

    save_json(result, OUTPUT)

    print(f"✅ AI parsed: {len(gemini_files)} files, top signal: {result['behavioral_inference']['top_signal']}")
    return result

if __name__ == "__main__":
    parse_ai_data()
