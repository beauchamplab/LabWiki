#!/usr/bin/env python3
"""
Reorganize wiki pages:
1. Move BeauchampLab/* to Beauchamp/
2. Move orphaned pages/* to pages/Beauchamp/
3. Update all internal links
4. Update frontmatter parent references
"""

import os
import re
import shutil
from pathlib import Path

# Files to move from pages/ to pages/Beauchamp/
# Excluding: TODO.md, Prompt.md, BROKEN_LINKS.md (these stay in pages/)
ORPHANED_FILES = [
    "Creating_Standardized_Surface_Models_New.md",
    "Finding_Release_Burst_Duration.md",
    "FreeSurferParcellation.md",
    "Making_Resting_State_Correlation_Maps.md",
    "Screencasts_of_Repeating_McGurk_Experiments.md",
    "Some_initial_pCASL_processing_notes_using_BASIL.md",
]

# Files to move from pages/BeauchampLab/ to pages/Beauchamp/
BEAUCHAMPLAB_FILES = [
    "VibrationMatlabCode.md",
]

def update_frontmatter(content, new_parent="Beauchamp"):
    """Update parent in frontmatter"""
    # Match frontmatter parent line
    pattern = r'(---\n(?:.*\n)*?)parent:\s*BeauchampLab(\n(?:.*\n)*?---)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1parent: ' + new_parent + r'\2', content)
    # Add parent if no frontmatter exists
    elif content.startswith('---\n'):
        pattern = r'(---\n(?:.*\n)*?)(---)'
        if 'parent:' not in content.split('---')[1]:
            content = re.sub(pattern, r'\1parent: ' + new_parent + r'\n\2', content)
    else:
        # Add frontmatter if completely missing
        title = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title_text = title.group(1) if title else "Untitled"
        content = f'---\nlayout: default\ntitle: "{title_text}"\nparent: {new_parent}\n---\n' + content
    return content

def update_links_in_content(content, file_mappings):
    """Update markdown links based on file mappings"""
    for old_path, new_path in file_mappings.items():
        # Handle various link formats
        patterns = [
            (rf'\[([^\]]+)\]\({re.escape(old_path)}\)', rf'[\1]({new_path})'),
            (rf'\[([^\]]+)\]\(\.\./\.\./pages/{re.escape(old_path)}\)', rf'[\1]({new_path})'),
            (rf'\[([^\]]+)\]\(\.\./pages/{re.escape(old_path)}\)', rf'[\1](../{new_path})'),
            (rf'\[([^\]]+)\]\(pages/{re.escape(old_path)}\)', rf'[\1](pages/{new_path})'),
        ]
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
    return content

def main():
    base_dir = Path("/Users/dipterix/PennNeurosurgery Dropbox/Dipterix W/BeauchampLabAtPenn/LabWiki")
    pages_dir = base_dir / "pages"
    beauchamp_dir = pages_dir / "Beauchamp"
    beauchamplab_dir = pages_dir / "BeauchampLab"
    
    # Create mapping of old → new paths for link updates
    file_mappings = {}
    
    # Build mappings for orphaned files
    for filename in ORPHANED_FILES:
        file_mappings[filename] = f"Beauchamp/{filename}"
        file_mappings[f"pages/{filename}"] = f"pages/Beauchamp/{filename}"
    
    # Build mappings for BeauchampLab files
    for filename in BEAUCHAMPLAB_FILES:
        file_mappings[f"BeauchampLab/{filename}"] = f"Beauchamp/{filename}"
        file_mappings[f"pages/BeauchampLab/{filename}"] = f"pages/Beauchamp/{filename}"
    
    print("=== Moving orphaned files to pages/Beauchamp/ ===")
    for filename in ORPHANED_FILES:
        src = pages_dir / filename
        dst = beauchamp_dir / filename
        if src.exists():
            print(f"Moving {src.name} → Beauchamp/")
            # Read content
            content = src.read_text()
            # Update frontmatter
            content = update_frontmatter(content)
            # Write to new location
            dst.write_text(content)
            # Remove old file
            src.unlink()
        else:
            print(f"  ⚠ Not found: {src}")
    
    print("\n=== Moving BeauchampLab files to pages/Beauchamp/ ===")
    for filename in BEAUCHAMPLAB_FILES:
        src = beauchamplab_dir / filename
        dst = beauchamp_dir / filename
        if src.exists():
            print(f"Moving {src.name} → Beauchamp/")
            # Read content
            content = src.read_text()
            # Update frontmatter (change parent from BeauchampLab to Beauchamp)
            content = update_frontmatter(content)
            # Write to new location
            dst.write_text(content)
            # Remove old file
            src.unlink()
        else:
            print(f"  ⚠ Not found: {src}")
    
    print("\n=== Removing BeauchampLab namespace ===")
    beauchamplab_index = pages_dir / "BeauchampLab.md"
    if beauchamplab_index.exists():
        print(f"Removing {beauchamplab_index}")
        beauchamplab_index.unlink()
    
    if beauchamplab_dir.exists() and not list(beauchamplab_dir.iterdir()):
        print(f"Removing empty directory {beauchamplab_dir}")
        beauchamplab_dir.rmdir()
    
    print("\n=== Updating links in all markdown files ===")
    all_md_files = list(pages_dir.rglob("*.md"))
    updated_count = 0
    
    for md_file in all_md_files:
        content = md_file.read_text()
        new_content = update_links_in_content(content, file_mappings)
        if new_content != content:
            md_file.write_text(new_content)
            updated_count += 1
            print(f"  Updated links in {md_file.relative_to(pages_dir)}")
    
    print(f"\n✓ Complete! Updated {updated_count} files with new links.")
    print(f"✓ Moved {len(ORPHANED_FILES) + len(BEAUCHAMPLAB_FILES)} files to pages/Beauchamp/")

if __name__ == "__main__":
    main()
