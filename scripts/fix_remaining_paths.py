#!/usr/bin/env python3
"""
Fix remaining relative path issues for moved files.
Handles links with title attributes like: [Home](index.md "Beauchamp")
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

files_fixed = 0

for cat_dir_name in CATEGORY_DIRS:
    cat_dir = BEAUCHAMP / cat_dir_name
    if not cat_dir.exists():
        continue

    for md_file in sorted(cat_dir.rglob("*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        rel = md_file.relative_to(BEAUCHAMP)
        depth = len(rel.parts) - 1
        prefix = "../" * depth

        # Fix: [Home](index.md "title") — with title attribute
        content = re.sub(
            r'\]\(index\.md(\s+"[^"]*")\)',
            f']({prefix}index.md\\1)',
            content
        )

        # Fix: [text](index.md "title") that references Beauchamp index
        content = re.sub(
            r'\]\(Beauchamp/index\.md\)',
            f']({prefix}index.md)',
            content
        )

        # Fix remaining bare index.md references (no title, should have been caught)
        content = re.sub(r'\]\(index\.md\)', f']({prefix}index.md)', content)

        # Fix: References like DataSharing.md, Publications.md etc at same level
        # that should now point into sibling category dirs
        # (These are few, handle them case by case)
        
        # Fix ../../attachments/ that might still be wrong  
        # (Some files might have had ../attachments or ../../../attachments already)

        if content != original:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(content)
            files_fixed += 1
            print(f"  ✓ Fixed: {rel}")

# Also fix index.md references to Beauchamp/Lab_Meetings_and_Notes etc
# that got partially resolved
index_file = BEAUCHAMP / "index.md"
with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()
original = content

# Fix references in index.md pointing to Beauchamp/ prefix (invalid from same dir)
content = content.replace("](Beauchamp/", "](")

if content != original:
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Fixed: index.md")

# Fix Obsolete files referencing sibling dirs
for md_file in sorted((BEAUCHAMP / "Obsolete").rglob("*.md")):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    
    rel = md_file.relative_to(BEAUCHAMP)
    depth = len(rel.parts) - 1
    prefix = "../" * depth
    
    content = re.sub(r'\]\(index\.md(\s+"[^"]*")?\)', f']({prefix}index.md)', content)
    
    if content != original:
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(content)
        files_fixed += 1
        print(f"  ✓ Fixed: {rel}")

print(f"\nFixed {files_fixed} files")
