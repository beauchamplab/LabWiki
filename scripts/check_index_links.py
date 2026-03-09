#!/usr/bin/env python3
"""Check all links in pages/Beauchamp/index.md for broken targets."""
import re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
idx = ROOT / "pages" / "Beauchamp" / "index.md"
base_dir = idx.parent

with open(idx) as f:
    content = f.read()

broken = []
total = 0

for m in re.finditer(r'\[([^\]]*)\]\(', content):
    link_text = m.group(1)
    start = m.end()
    depth = 1
    i = start
    while i < len(content) and depth > 0:
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
        i += 1
    if depth != 0:
        continue
    target = content[start:i-1]
    if target.startswith(('http', 'mailto', '#', 'ftp')):
        continue
    clean = re.split(r'[#"\s]', target)[0]
    if not clean:
        continue
    total += 1
    resolved = (base_dir / clean).resolve()
    if not resolved.exists():
        broken.append((link_text, clean, str(resolved)))

print(f"Total internal links: {total}")
print(f"Broken: {len(broken)}")
if broken:
    print()
    for text, link, resolved in broken:
        print(f"  [{text}]({link})")
        print(f"    -> {resolved}")
