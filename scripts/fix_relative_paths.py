#!/usr/bin/env python3
"""
Fix relative paths in pages that were moved one directory deeper.
Files in Beauchamp/{Category}/ need paths adjusted:
  - index.md -> ../index.md
  - ../../attachments/ -> ../../../attachments/
  - ../RAVE/ -> ../../RAVE/ (and CAMRI, YAEL, Karas_Lab)
  - Obsolete/ -> ../Obsolete/
"""

import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
BEAUCHAMP = WORKSPACE / "pages" / "Beauchamp"

CATEGORY_DIRS = [
    "Publications_and_Talks",
    "Resources_and_Data_Sharing",
    "Lab_Meetings_and_Notes",
    "Data_Processing",
    "Internal_Notes",
]

fixes_made = 0
files_fixed = 0

for cat_dir_name in CATEGORY_DIRS:
    cat_dir = BEAUCHAMP / cat_dir_name
    if not cat_dir.exists():
        continue

    for md_file in sorted(cat_dir.rglob("*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        # Determine depth relative to Beauchamp/
        rel = md_file.relative_to(BEAUCHAMP)
        depth = len(rel.parts) - 1  # 1 for Category/file.md, 2 for Category/Sub/file.md

        # Fix: index.md -> ../index.md (for depth=1) or ../../index.md (depth=2)
        prefix = "../" * depth
        content = re.sub(r'\]\(index\.md\)', f']({prefix}index.md)', content)

        # Fix: ../../attachments/ -> ../../../attachments/ (add one ../ per extra depth)
        # Original files were at Beauchamp/ depth, using ../../attachments/
        # Now at Beauchamp/Category/ (depth+1), need one more ../
        # Pattern: already has ../../attachments/ -> need to add ../ for each depth level
        # But some files already have correct paths, so be careful
        # Check: from Beauchamp/Category/file.md, attachments is at ../../../attachments/
        # From Beauchamp/Category/Sub/file.md, attachments is at ../../../../attachments/
        # The original path was ../../attachments/ (from Beauchamp/file.md)
        for i in range(depth):
            content = content.replace('](../../attachments/', '](../../../attachments/')
            content = content.replace('](../../attachments/', '](../../../attachments/')

        # Fix cross-namespace links: ../RAVE/ -> ../../RAVE/, ../CAMRI/ -> ../../CAMRI/, etc.
        for ns in ['RAVE', 'CAMRI', 'YAEL', 'Karas_Lab']:
            old_pattern = f'](../{ns}/'
            new_pattern = f']({"../" * depth}../{ns}/'
            content = content.replace(old_pattern, new_pattern)

        # Fix Obsolete/ references: Obsolete/file.md -> ../Obsolete/file.md
        if depth == 1:
            content = re.sub(r'\]\(Obsolete/', '](../Obsolete/', content)
        elif depth == 2:
            content = re.sub(r'\]\(Obsolete/', '](../../Obsolete/', content)

        if content != original:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(content)
            change_count = sum(1 for a, b in zip(original, content) if a != b)
            files_fixed += 1
            fixes_made += 1
            print(f"  ✓ Fixed: {rel}")

print(f"\nFixed {files_fixed} files")
