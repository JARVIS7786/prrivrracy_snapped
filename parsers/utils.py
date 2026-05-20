"""
Shared utilities - DRY principle
All parsers use these instead of duplicating code
"""
import json
import os
import re
from bs4 import BeautifulSoup

def load_json(filepath):
    """Load JSON file, return empty dict if missing"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(data, filepath):
    """Save JSON with consistent formatting"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_html_file(filepath):
    """Parse HTML file, return BeautifulSoup object"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def extract_text_from_tags(soup, tags=['div', 'td', 'li'], min_len=3, max_len=100):
    """Extract clean text from HTML tags, remove duplicates"""
    if not soup:
        return []

    # Remove script and style tags
    for tag in soup(['script', 'style']):
        tag.decompose()

    items = []
    for tag in soup.find_all(tags):
        text = tag.get_text(strip=True)
        if min_len < len(text) < max_len and text[0].isupper():
            items.append(text)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(items))

def count_keyword_matches(text, keywords):
    """Count how many keywords appear in text"""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw in text_lower)

def decode_html_entities(text):
    """Decode common HTML entities"""
    return (text.replace('&#39;', "'")
                .replace('&amp;', '&')
                .replace('&quot;', '"')
                .replace('&lt;', '<')
                .replace('&gt;', '>'))
