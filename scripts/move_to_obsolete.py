#!/usr/bin/env python3
"""
Move pages into Obsolete/ and Obsolete/Lectures/ subdirectories,
update their frontmatter, and fix all internal links across the wiki.
"""

import os
import re
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PAGES = BASE / "pages"
BEAUCHAMP = PAGES / "Beauchamp"

# Pages moving to Obsolete/ with new parent "Obsolete"
OBSOLETE_PAGES = [
    "Software_Installation_OLD.md",
    "CreateCortSurfModOLD.md",
    "UseCortSurfModOLD.md",
    "PrepCortSurfModelsOLD.md",
    "TeachingOld.md",
    "Old_Protocols.md",
    "_iEEG_EMU_SOP.md",
    "_Creating_a_Surface_Model_and_Electrode_Localization_(by_Muge_Ozker_Sertel).md",
    "RAVE:AWS.md",
]

# Pages moving to Obsolete/Lectures/ with new parent "Lectures"
LECTURE_PAGES = [
    "ShortCourse2010.md",
    "ShortCourse2010Participants.md",
    "NeuroimagingElective.md",
    "GraduateNeuroanatomy.md",
    "TCH.md",
    "MedNSLab.md",
    "MedNSLabNotes.md",
    "ElectiveNotes.md",
]


def update_frontmatter_parent(content, new_parent, grand_parent=None):
    """Replace parent: Beauchamp with new_parent in YAML frontmatter."""
    # Match the frontmatter block
    fm_match = re.match(r'^(---\n)(.*?)(---\n)', content, re.DOTALL)
    if not fm_match:
        return content

    fm_body = fm_match.group(2)
    rest = content[fm_match.end():]

    # Replace parent line
    fm_body = re.sub(r'^parent:\s+.*$', f'parent: {new_parent}', fm_body, flags=re.MULTILINE)

    # Add grand_parent if specified and not already present
    if grand_parent and 'grand_parent:' not in fm_body:
        fm_body = re.sub(
            r'^(parent:\s+.*)$',
            rf'\1\ngrand_parent: {grand_parent}',
            fm_body,
            flags=re.MULTILINE
        )

    return fm_match.group(1) + fm_body + fm_match.group(3) + rest


def move_and_update(filename, dest_dir, new_parent, grand_parent=None):
    """Move a file and update its frontmatter."""
    src = BEAUCHAMP / filename
    if not src.exists():
        print(f"  WARNING: {src} does not exist, skipping")
        return False

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename

    content = src.read_text(encoding='utf-8')
    content = update_frontmatter_parent(content, new_parent, grand_parent)
    dest.write_text(content, encoding='utf-8')
    src.unlink()
    print(f"  Moved {filename} -> {dest.relative_to(BASE)}")
    return True


def fix_links_in_file(filepath, moved_files_map):
    """
    Fix markdown links in a file that reference moved pages.
    moved_files_map: dict of old_filename -> new_relative_path_from_Beauchamp
    """
    content = filepath.read_text(encoding='utf-8')
    original = content

    # Determine the directory of the current file relative to pages/Beauchamp
    try:
        rel = filepath.relative_to(BEAUCHAMP)
        depth_from_beauchamp = len(rel.parts) - 1  # subtract the filename itself
    except ValueError:
        # File is not under Beauchamp/ — check if it's under pages/
        try:
            rel = filepath.relative_to(PAGES)
            # For files in other namespace dirs (RAVE/, CAMRI/, etc.)
            # they might link to Beauchamp pages like ../Beauchamp/OldPage.md
            depth_from_beauchamp = None
        except ValueError:
            depth_from_beauchamp = None

    for old_name, new_rel_from_beauchamp in moved_files_map.items():
        # Pattern 1: Direct link to the file (same directory) e.g., [text](OldPage.md)
        # Pattern 2: Link with path e.g., [text](../Beauchamp/OldPage.md)
        # Pattern 3: Link with Beauchamp/ prefix e.g., [text](Beauchamp/OldPage.md)
        # We need to handle all these variants

        old_escaped = re.escape(old_name)

        if depth_from_beauchamp is not None:
            # File is under Beauchamp/ — look for direct references
            # Replace: (OldPage.md) or (OldPage.md "title") or (OldPage.md#anchor)
            def make_replacement(match):
                prefix = match.group(1)  # opening paren or space before
                suffix = match.group(2)  # anchor, title, or closing paren
                # Calculate relative path from current file's directory to new location
                if depth_from_beauchamp == 0:
                    new_path = new_rel_from_beauchamp
                else:
                    new_path = "../" * depth_from_beauchamp + new_rel_from_beauchamp
                return f"{prefix}{new_path}{suffix}"

            # Match link targets: ](OldFile.md), ](OldFile.md#anchor), ](OldFile.md "title")
            pattern = rf'(\]\()({old_escaped})((?:#[^\s)]*)?(?:\s+"[^"]*")?\))'
            content = re.sub(pattern, lambda m: m.group(1) + _calc_path(new_rel_from_beauchamp, depth_from_beauchamp) + m.group(3), content)

        # For files outside Beauchamp/, fix paths like ../Beauchamp/OldFile.md
        if depth_from_beauchamp is None or depth_from_beauchamp > 0:
            # Match ../Beauchamp/OldFile.md or Beauchamp/OldFile.md patterns
            old_with_prefix = rf'(\]\([^\)]*?)(?:\.\./)*(Beauchamp/{old_escaped})((?:#[^\s)]*)?(?:\s+"[^"]*")?\))'
            def fix_external_ref(m):
                before = m.group(1)
                suffix = m.group(3)
                return f'{before}Beauchamp/{new_rel_from_beauchamp}{suffix}'
            content = re.sub(old_with_prefix, fix_external_ref, content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def _calc_path(new_rel_from_beauchamp, depth_from_beauchamp):
    """Calculate relative path from current depth to new location."""
    if depth_from_beauchamp == 0:
        return new_rel_from_beauchamp
    return "../" * depth_from_beauchamp + new_rel_from_beauchamp


def fix_all_links(moved_files_map):
    """Scan all markdown files and fix links to moved pages."""
    fixed_count = 0
    # Scan all .md files under pages/
    for md_file in sorted(PAGES.rglob("*.md")):
        if fix_links_in_file(md_file, moved_files_map):
            print(f"  Fixed links in {md_file.relative_to(BASE)}")
            fixed_count += 1

    # Also check index.md at root
    root_index = BASE / "index.md"
    if root_index.exists():
        if fix_links_in_file(root_index, moved_files_map):
            print(f"  Fixed links in index.md")
            fixed_count += 1

    return fixed_count


def main():
    moved_files_map = {}

    print("Phase 1: Moving deprecated pages to Obsolete/")
    print("-" * 50)
    obsolete_dir = BEAUCHAMP / "Obsolete"
    for filename in OBSOLETE_PAGES:
        if move_and_update(filename, obsolete_dir, "Obsolete", grand_parent="Beauchamp"):
            moved_files_map[filename] = f"Obsolete/{filename}"

    print()
    print("Phase 2: Moving lecture pages to Obsolete/Lectures/")
    print("-" * 50)
    lectures_dir = BEAUCHAMP / "Obsolete" / "Lectures"
    for filename in LECTURE_PAGES:
        if move_and_update(filename, lectures_dir, "Lectures", grand_parent="Obsolete"):
            moved_files_map[filename] = f"Obsolete/Lectures/{filename}"

    print()
    print("Phase 3: Fixing internal links across all pages")
    print("-" * 50)
    fixed = fix_all_links(moved_files_map)
    print(f"  Fixed links in {fixed} files")

    print()
    print("Summary:")
    print(f"  Moved {len([f for f in OBSOLETE_PAGES if f in [k for k in moved_files_map if 'Lectures' not in moved_files_map[k]]])} pages to Obsolete/")
    print(f"  Moved {len([f for f in LECTURE_PAGES if f in moved_files_map])} pages to Obsolete/Lectures/")
    print(f"  Fixed links in {fixed} files")


if __name__ == "__main__":
    main()
