#!/usr/bin/env python3
"""
Add YAML front matter to all wiki pages for Just-the-Docs theme.
Removes manual navigation headers.
"""

import os
import re
from pathlib import Path

# Mapping of directory names to parent titles
NAMESPACE_PARENTS = {
    'Beauchamp': 'Beauchamp',
    'BeauchampLab': 'BeauchampLab',
    'RAVE': 'RAVE',
    'CAMRI': 'CAMRI',
    'YAEL': 'YAEL',
    'Karas_Lab': 'Karas Lab',
}

def extract_title_from_content(content):
    """Extract title from the first H1 heading in markdown."""
    # Look for first H1 heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def extract_title_from_filename(filename):
    """Convert filename to readable title."""
    # Remove .md extension
    name = filename.replace('.md', '')
    # Replace underscores and hyphens with spaces
    name = name.replace('_', ' ').replace('-', ' ')
    return name

def has_front_matter(content):
    """Check if content already has YAML front matter."""
    return content.startswith('---\n') or content.startswith('---\r\n')

def remove_navigation_header(content):
    """Remove manual navigation header from content."""
    # Match lines like: > **Navigation:** [Home](index.md) • Publications • [Resources](DataSharing.md)
    # Can use • or | as separator
    pattern = r'^>\s*\*\*Navigation:\*\*.*$\n?'
    content = re.sub(pattern, '', content, flags=re.MULTILINE)
    return content

def add_front_matter(filepath, parent=None):
    """Add YAML front matter to a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has front matter
    if has_front_matter(content):
        print(f"Skipping {filepath} - already has front matter")
        return False
    
    # Remove navigation headers
    original_content = content
    content = remove_navigation_header(content)
    
    # Extract title
    title = extract_title_from_content(content)
    if not title:
        title = extract_title_from_filename(filepath.name)
    
    # Build front matter
    front_matter = ['---', 'layout: default']
    front_matter.append(f'title: "{title}"')
    
    if parent:
        front_matter.append(f'parent: {parent}')
    
    front_matter.append('---')
    front_matter.append('')  # Blank line after front matter
    
    # Combine front matter with content
    new_content = '\n'.join(front_matter) + content
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    changed = original_content != content
    return True, changed

def process_directory(base_path):
    """Process all markdown files in the pages directory."""
    base = Path(base_path)
    stats = {
        'processed': 0,
        'skipped': 0,
        'nav_removed': 0,
    }
    
    # Process namespace directories
    for namespace, parent_title in NAMESPACE_PARENTS.items():
        namespace_dir = base / namespace
        if not namespace_dir.exists():
            print(f"Warning: {namespace_dir} does not exist")
            continue
        
        print(f"\nProcessing {namespace}/ directory...")
        for md_file in sorted(namespace_dir.glob('*.md')):
            result = add_front_matter(md_file, parent=parent_title)
            if result:
                processed, nav_removed = result
                if processed:
                    stats['processed'] += 1
                    if nav_removed:
                        stats['nav_removed'] += 1
                    print(f"  ✓ {md_file.name}")
            else:
                stats['skipped'] += 1
    
    # Process root-level pages (no parent)
    print(f"\nProcessing root-level pages...")
    for md_file in sorted(base.glob('*.md')):
        if md_file.name in ['Beauchamp.md', 'BeauchampLab.md', 'RAVE.md', 
                            'CAMRI.md', 'YAEL.md', 'Karas_Lab.md', 'TODO.md', 'BROKEN_LINKS.md']:
            # Skip namespace index pages and metadata files
            print(f"  - Skipping {md_file.name} (namespace index or metadata)")
            continue
        
        result = add_front_matter(md_file, parent=None)
        if result:
            processed, nav_removed = result
            if processed:
                stats['processed'] += 1
                if nav_removed:
                    stats['nav_removed'] += 1
                print(f"  ✓ {md_file.name}")
        else:
            stats['skipped'] += 1
    
    return stats

if __name__ == '__main__':
    pages_dir = '/home/runner/work/LabWiki/LabWiki/pages'
    
    print("Adding front matter to all wiki pages...")
    print("=" * 60)
    
    stats = process_directory(pages_dir)
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  Processed: {stats['processed']} files")
    print(f"  Skipped: {stats['skipped']} files (already had front matter)")
    print(f"  Navigation headers removed: {stats['nav_removed']} files")
    print("=" * 60)
