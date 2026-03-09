#!/usr/bin/env python3
"""Quick broken-link checker for the wiki pages."""
import re
from pathlib import Path

PAGES = Path(__file__).resolve().parent.parent / "pages"
broken = []


def find_markdown_links(text):
    """Find markdown links handling parentheses in filenames."""
    results = []
    # Match [text]( then manually find the balanced closing )
    for m in re.finditer(r'\[([^\]]*)\]\(', text):
        link_text = m.group(1)
        start = m.end()  # position right after the opening (
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
            i += 1
        if depth == 0:
            target = text[start:i-1]
            results.append((link_text, target))
    return results


for md_file in sorted(PAGES.rglob("*.md")):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    for text, target in find_markdown_links(content):
        
        # Skip external links, anchors, mailto, etc.
        if target.startswith(('http://', 'https://', 'mailto:', '#', 'ftp://')):
            continue
        
        # Strip anchor and title
        target_clean = re.split(r'[#"\s]', target)[0]
        if not target_clean:
            continue
        
        # Resolve relative to the file's directory
        resolved = (md_file.parent / target_clean).resolve()
        if not resolved.exists():
            rel = md_file.relative_to(PAGES)
            broken.append((str(rel), text, target_clean))

if broken:
    print(f"Found {len(broken)} broken links:\n")
    for src, text, target in broken:
        print(f"  {src}: [{text}]({target})")
else:
    print("No broken internal links found!")
