"""
Run this to show exactly what HTML structure Google is using.
Paste the output back so we can fix the parser.
"""
import os

files = [
    "data/takeout/Takeout 2/My Activity/Search/My Activity.html",
    "data/takeout/Takeout 1/YouTube and YouTube Music/history/watch-history.html",
]

for filepath in files:
    if not os.path.exists(filepath):
        print(f"NOT FOUND: {filepath}")
        continue

    print(f"\n{'='*60}")
    print(f"FILE: {filepath}")
    print(f"{'='*60}")

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = []
        for i, line in enumerate(f):
            lines.append(line)
            if i > 3000:  # read first 3000 lines only
                break

    content = ''.join(lines)

    # Show unique class names found
    import re
    classes = re.findall(r'class="([^"]+)"', content)
    unique = list(dict.fromkeys(classes))
    print(f"\nUnique CSS classes found (first 30):")
    for c in unique[:30]:
        print(f"  - {c}")

    # Show first <a> tag with text
    links = re.findall(r'<a[^>]*>([^<]{3,80})</a>', content)
    print(f"\nFirst 10 link texts found:")
    for l in links[:10]:
        print(f"  - {l.strip()}")

    # Show a raw 20-line sample from middle of file
    mid = len(lines) // 4
    print(f"\nRaw HTML sample (lines {mid}-{mid+15}):")
    for line in lines[mid:mid+15]:
        stripped = line.strip()
        if stripped:
            print(f"  {stripped[:120]}")