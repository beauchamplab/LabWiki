#!/usr/bin/env python3
"""
Fix remaining broken links after Phase 2 reorganization.
Handles:
1. Obsolete/ files with wrong attachment path depth
2. Screencasts page wrong attachment depth
3. Files with parentheses in names (regex issue in link fixer)
4. External wiki refs needing ../ prefix
5. Misc one-off fixes
"""
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PAGES = WORKSPACE / "pages"
BEAUCHAMP = PAGES / "Beauchamp"
fixed = 0


def fix_file(filepath, replacements):
    """Apply a list of (old, new) string replacements to a file."""
    global fixed
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        rel = filepath.relative_to(PAGES)
        print(f"  ✓ {rel}")
        fixed += 1


# 1. Fix ../../attachments/ -> ../../../attachments/ in Obsolete/ files (depth 2)
print("Fixing attachment paths in Obsolete/ files...")
for md_file in sorted((BEAUCHAMP / "Obsolete").glob("*.md")):
    fix_file(md_file, [
        ("](../../attachments/", "](../../../attachments/"),
    ])

# 2. Fix ../../attachments/ -> ../../../../attachments/ in Obsolete/Lectures/ files (depth 3)
print("Fixing attachment paths in Obsolete/Lectures/ files...")
for md_file in sorted((BEAUCHAMP / "Obsolete" / "Lectures").glob("*.md")):
    fix_file(md_file, [
        ("](../../attachments/", "](../../../../attachments/"),
        # Also fix if already partially done (../../../ -> ../../../../)
        ("](../../../attachments/", "](../../../../attachments/"),
    ])

# 3. Fix Screencasts page: ../attachments/ -> ../../../attachments/
print("Fixing Screencasts attachment paths...")
sc = BEAUCHAMP / "Resources_and_Data_Sharing" / "Screencasts_of_Repeating_McGurk_Experiments.md"
if sc.exists():
    fix_file(sc, [
        ("](../attachments/", "](../../../attachments/"),
    ])

# 4. Fix external wiki refs (CAMRI, Karas_Lab) pointing to Beauchamp/ pages
print("Fixing external wiki references...")
for filepath, replacements in [
    (PAGES / "CAMRI" / "HowToScan.md", [
        ("](Beauchamp/Lab_Meetings_and_Notes/Lab_Notebook.md)", "](../Beauchamp/Lab_Meetings_and_Notes/Lab_Notebook.md)"),
    ]),
    (PAGES / "CAMRI" / "Resources.md", [
        ("](Beauchamp/Lab_Meetings_and_Notes/Lab_Notebook.md)", "](../Beauchamp/Lab_Meetings_and_Notes/Lab_Notebook.md)"),
    ]),
    (PAGES / "Karas_Lab" / "RAVE_Electrode_Localization.md", [
        ("](Beauchamp/Data_Processing/BuffyElectrodeNotes.md)", "](../Beauchamp/Data_Processing/BuffyElectrodeNotes.md)"),
    ]),
]:
    if filepath.exists():
        fix_file(filepath, replacements)

# 5. Fix parentheses in filenames (links get truncated by markdown parser)
# These files have names with () that break simple [text](path) matching
print("Fixing links with parentheses in filenames...")

# index.md links to files with parentheses
index = BEAUCHAMP / "index.md"
if index.exists():
    fix_file(index, [
        ("](Data_Processing/Reconstruction_and_Electrode_Labeling_(UPenn).md)",
         "](Data_Processing/Reconstruction_and_Electrode_Labeling_%28UPenn%29.md)"),
        ("](Data_Processing/Creating_a_Surface_Model_and_Electrode_Localization_(by_Muge_Ozker_Sertel).md)",
         "](Data_Processing/Creating_a_Surface_Model_and_Electrode_Localization_%28by_Muge_Ozker_Sertel%29.md)"),
    ])

# Wait - actually the files DO have parens in their names. The issue is the regex
# in check_broken_links.py truncates at ( in the target. Let me check if the link
# actually resolves correctly:
# The target in index.md: Data_Processing/Reconstruction_and_Electrode_Labeling_(UPenn).md
# The actual file: Data_Processing/Reconstruction_and_Electrode_Labeling_(UPenn).md
# These should work! The broken link checker has a bug with parens.
# Let me NOT percent-encode these and instead revert the index.md changes.

# Actually, let me re-check. The checker uses re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', ...)
# The regex [^)]+ stops at the first ), so (UPenn) breaks it.
# But the actual file DOES exist. So these are FALSE POSITIVES from the checker.
# Revert the % encoding:

if index.exists():
    fix_file(index, [
        ("](Data_Processing/Reconstruction_and_Electrode_Labeling_%28UPenn%29.md)",
         "](Data_Processing/Reconstruction_and_Electrode_Labeling_(UPenn).md)"),
        ("](Data_Processing/Creating_a_Surface_Model_and_Electrode_Localization_%28by_Muge_Ozker_Sertel%29.md)",
         "](Data_Processing/Creating_a_Surface_Model_and_Electrode_Localization_(by_Muge_Ozker_Sertel).md)"),
    ])

# 6. Fix one-off issues
print("Fixing one-off issues...")

# Artifact Rejection: pages/Beauchamp/Publications.md -> ../../Publications_and_Talks/Publications.md
ar = BEAUCHAMP / "Data_Processing" / "Brain Stimulation" / "Artifact Rejection.md"
if ar.exists():
    fix_file(ar, [
        ("](pages/Beauchamp/Publications.md)", "](../../Publications_and_Talks/Publications.md)"),
    ])

# Some_initial_pCASL: Beauchamp/index.md -> ../index.md, etc.
pcasl = BEAUCHAMP / "Data_Processing" / "Some_initial_pCASL_processing_notes_using_BASIL.md"
if pcasl.exists():
    fix_file(pcasl, [
        ("](Beauchamp/index.md)", "](../index.md)"),
        ("](Beauchamp/Publications.md)", "](../Publications_and_Talks/Publications.md)"),
        ("](Beauchamp/DataSharing.md)", "](../Resources_and_Data_Sharing/DataSharing.md)"),
    ])

# Lab_Notebook.md: Fix links with parens in filenames
lab_nb = BEAUCHAMP / "Lab_Meetings_and_Notes" / "Lab_Notebook.md"
if lab_nb.exists():
    with open(lab_nb, "r", encoding="utf-8") as f:
        content = f.read()
    # These links work but the checker flagged them as false positives due to parens
    # No actual fix needed if the files exist at the target paths

# RAVE/LocalizeElectrodes.md: Same parens issue (false positive)

# Obsolete/TeachingOld.md: AvailableDates20142015.md - page never existed (pre-existing)

# RetinotopicMapping.md: attachment with parens - false positive from checker

print(f"\nTotal files fixed: {fixed}")
