#!/usr/bin/env python3
"""
Phase 2: Reorganize ~115 Beauchamp pages into 5 category subdirectories.
Creates category parent pages + subdirectories, moves files, updates frontmatter & links.
"""

import os
import re
import shutil
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PAGES_DIR = WORKSPACE / "pages"
BEAUCHAMP = PAGES_DIR / "Beauchamp"

# ─── Category definitions ──────────────────────────────────────────────
CATEGORIES = {
    "Publications_and_Talks": {
        "title": "Publications and Talks",
        "nav_order": 1,
        "pages": [
            "Publications.md",
            "talks.md",
            "Projects.md",
            "PositionsAvailable.md",
        ],
    },
    "Resources_and_Data_Sharing": {
        "title": "Resources and Data Sharing",
        "nav_order": 2,
        "pages": [
            "DataSharing.md",
            "Stimuli.md",
            "LocalizerStimuli.md",
            "PennMcGurkBattery.md",
            "VideoStimulusCreation.md",
            "RandomStimulus.md",
            "Playback_Rate.md",
            "Making_Grayscale_From_Color_Images.md",
            "word_stimuli.md",
            "McGurk_CI_Stimuli_McGurk.md",
            "Screencasts_of_Repeating_McGurk_Experiments.md",
            "CIMS.md",
            "CIMS_McGurk.md",
            "NED.md",
            "RaceModel.md",
            "100Hue.md",
        ],
    },
    "Lab_Meetings_and_Notes": {
        "title": "Lab Meetings and Notes",
        "nav_order": 3,
        "pages": [
            "Lab_Meeting.md",
            "Lab_Notebook.md",
            "Lab_Members.md",
            "Lab_Alums.md",
            "Orientation.md",
            "Ordering.md",
            "Teaching.md",
            "Subjects.md",
            "AvailableDates.md",
            "WUES.md",
            "CAMRI_PTS.md",
            "Manage_this_Wiki.md",
        ],
    },
    "Data_Processing": {
        "title": "Data Processing and Analysis",
        "nav_order": 4,
        "pages": [
            # fMRI & scanning
            "fMRIOverview.md", "HowToScan.md", "HiResfMRI.md", "Presurgical_Scanning.md",
            "CreateAFNIBRIK.md", "CreateAFNIBRIKfromMR.md", "MotionCorrection.md",
            "MRI_Data_Analysis.md", "Unwarping.md", "RealTimefMRI.md",
            "AutomatingAFNI.md", "CallingAFNISUMA.md", "GroupAna.md", "VolAverage.md",
            "Some_initial_pCASL_processing_notes_using_BASIL.md",
            # Surfaces
            "CorticalSurfaceOverview.md", "CreateCortSurfMod.md", "PrepCortSurfModels.md",
            "UseCortSurfMod.md", "FreeSurfer.md", "FreeSurferParcellation.md",
            "FSAverageReadme.md", "SUMA.md", "Caret.md", "CorticalSurfaceHCP.md",
            "SurfaceAveraging.md", "MapIco.md", "SurfDist.md", "SurfaceMetrics.md",
            "CreateStndSurfMod.md", "CreateStndSurfModNew.md",
            "Creating_Standardized_Surface_Models_New.md",
            "Creating_a_Surface_Model_and_Electrode_Localization_(by_Muge_Ozker_Sertel).md",
            "IfCortModExists.md", "EditingCortSurf.md", "FSStndSurf.md",
            "SurfaceModelsPrinting.md", "PrintingBrains.md", "InflationMovies.md",
            "BrainPix.md", "RetinotopicMapping.md", "Retinotopy.md",
            "ZillesAtlasValues.md",
            # Electrophysiology & iEEG
            "Electrophysiology.md", "iEEG_EMU_SOP.md", "iEEG_EMU_MATLAB_SOP.md",
            "iEEGWorkflow.md", "iEEGWorkflow2.md", "ClinicalWorkflow.md",
            "DownloadDataPenn.md", "ECogAnalysis.md", "ECogAnalysisV2.md", "TensorECOG.md",
            "Electrode_Localization_and_Naming.md",
            "Reconstruction_and_Electrode_Labeling_(UPenn).md",
            "iELVIS.md", "BuffyElectrodeNotes.md", "ALICE.md", "img_pipe.md",
            "RAVE.md", "RAVE:Cluster.md", "RAVE:Condition_Explorer.md", "RAVE:Module_Builder.md",
            "Brain Stimulation.md",
            "TMS.md", "TMSOverview.md", "Electrical_Stimulation.md",
            "Setup_Apparatus.md", "Shut_Down_Apparatus.md", "NIRS.md",
            # Experiments & paradigms
            "Adaptation.md", "Adaptation_and_CP.md", "Selectivity.md",
            "Perceptual_Biasing.md", "Receptive_Field_Mapping.md",
            "AuditoryTactile.md", "Tactile_Experiment_Notes.md",
            "Autism.md", "RestingState.md",
            # Statistics & analysis
            "ANOVAs_in_MATLAB.md", "anovan.md", "MVPA_Notes.md",
            "ROIanalysis.md", "DrawingROIs.md", "Choice_Probability.md",
            "dprime.md", "ActivityMaps.md", "Making_Resting_State_Correlation_Maps.md",
            # Eye tracking
            "EyeTrackSetup.md", "NewEyeTrackSetup.md", "Eye_Tracker.md", "Tobii.md",
            # Speech & transcription
            "transcription.md", "Finding_Release_Burst_Duration.md",
            # DTI
            "ProcessDiffTensImgData.md", "UsingTORTOISE.md", "DetermineTract.md",
            "VibrationArtifacts.md", "VibrationMatlabCode.md", "InitialAutoVOIforIT.md",
            # Installation & software
            "Software_Installation.md", "AFNI_Install.md", "AayushiPreprocessingNotes.md",
            # Other
            "ProjectionNotes.md",
        ],
    },
    "Internal_Notes": {
        "title": "Internal Notes",
        "nav_order": 98,
        "pages": [
            "haotian.md",
        ],
    },
}

# ─── Helpers ────────────────────────────────────────────────────────────

def update_frontmatter(filepath, new_parent, new_grand_parent="Beauchamp"):
    """Update parent/grand_parent in existing YAML frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        print(f"  WARNING: No frontmatter in {filepath}")
        return

    end = content.index("---", 3)
    fm = content[3:end]
    body = content[end:]

    # Remove old parent / grand_parent lines
    fm = re.sub(r'^parent:.*\n', '', fm, flags=re.MULTILINE)
    fm = re.sub(r'^grand_parent:.*\n', '', fm, flags=re.MULTILINE)

    # Append new ones (before trailing newline)
    fm = fm.rstrip('\n') + '\n'
    fm += f'parent: {new_parent}\n'
    fm += f'grand_parent: {new_grand_parent}\n'

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---" + fm + body)


def fix_links_in_file(filepath, moved_files_map):
    """
    In filepath, rewrite relative markdown links to files that have moved.
    moved_files_map: { old_basename: new_relative_from_beauchamp }
    e.g. { "Publications.md": "Publications_and_Talks/Publications.md" }
    filepath is assumed inside pages/Beauchamp/ or a subdir of it.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Determine how deep this file is relative to pages/Beauchamp/
    rel = filepath.relative_to(BEAUCHAMP)
    depth = len(rel.parts) - 1  # 0 for files directly in Beauchamp/

    for old_name, new_rel in moved_files_map.items():
        # Build old reference patterns (could be just the filename when in same dir)
        # and new relative path from this file's location
        prefix_up = "../" * depth
        new_path = prefix_up + new_rel

        # Replace plain filename references: [text](OldName.md)
        # Also handle [text](OldName.md#anchor) and [text](OldName.md "title")
        old_escaped = re.escape(old_name)
        pattern = r'(\[[^\]]*\]\()' + old_escaped + r'([#"\s\)])'
        replacement = r'\1' + new_path + r'\2'
        content = re.sub(pattern, replacement, content)

        # Also fix references that already use a wrong subdir prefix
        # e.g. if a file references "Obsolete/foo.md" but foo moved elsewhere
        # (unlikely here but safe)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def fix_links_outside_beauchamp(moved_files_map):
    """Fix links in files outside pages/Beauchamp/ that reference moved files."""
    count = 0
    # Check RAVE, CAMRI, YAEL, Karas_Lab, root pages
    for search_dir in [PAGES_DIR / "RAVE", PAGES_DIR / "CAMRI", PAGES_DIR / "YAEL",
                       PAGES_DIR / "Karas_Lab", PAGES_DIR]:
        if not search_dir.exists():
            continue
        pattern = "*.md" if search_dir == PAGES_DIR else "**/*.md"
        for md_file in search_dir.glob(pattern):
            if md_file.is_dir():
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            original = content
            for old_name, new_rel in moved_files_map.items():
                # These files reference Beauchamp pages with path like ../Beauchamp/OldName.md
                old_ref = f"Beauchamp/{old_name}"
                new_ref = f"Beauchamp/{new_rel}"
                content = content.replace(old_ref, new_ref)
            if content != original:
                with open(md_file, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
                print(f"  Fixed external links in {md_file.relative_to(PAGES_DIR)}")
    return count


# ─── Main ───────────────────────────────────────────────────────────────

def main():
    moved_files_map = {}  # old_basename -> new_relative_path (from Beauchamp/)
    total_moved = 0
    skipped = []

    # 1. Create category parent pages and subdirectories
    print("=" * 60)
    print("Phase 2: Reorganize Beauchamp pages into categories")
    print("=" * 60)

    for cat_dir_name, cat_info in CATEGORIES.items():
        cat_dir = BEAUCHAMP / cat_dir_name
        cat_dir.mkdir(exist_ok=True)
        print(f"\n📁 Created directory: {cat_dir_name}/")

        # Create category parent page
        parent_page = BEAUCHAMP / f"{cat_dir_name}.md"
        if not parent_page.exists():
            with open(parent_page, "w", encoding="utf-8") as f:
                f.write(f"""---
layout: default
title: "{cat_info['title']}"
parent: Beauchamp
has_children: true
nav_order: {cat_info['nav_order']}
---
# {cat_info['title']}
""")
            print(f"  ✓ Created parent page: {cat_dir_name}.md")
        else:
            print(f"  - Parent page exists: {cat_dir_name}.md")

        # 2. Move pages into subdirectory
        for page_name in cat_info["pages"]:
            src = BEAUCHAMP / page_name
            dst = cat_dir / page_name

            if not src.exists():
                skipped.append(page_name)
                print(f"  ⚠ Not found: {page_name}")
                continue

            if dst.exists():
                print(f"  - Already moved: {page_name}")
                moved_files_map[page_name] = f"{cat_dir_name}/{page_name}"
                continue

            shutil.move(str(src), str(dst))
            moved_files_map[page_name] = f"{cat_dir_name}/{page_name}"
            total_moved += 1
            print(f"  ✓ Moved: {page_name}")

            # Update frontmatter
            update_frontmatter(dst, new_parent=cat_info["title"], new_grand_parent="Beauchamp")

        # Special: Brain Stimulation subfolder → Data_Processing/
        if cat_dir_name == "Data_Processing":
            bs_subdir = BEAUCHAMP / "Brain Stimulation"
            if bs_subdir.exists() and bs_subdir.is_dir():
                dst_subdir = cat_dir / "Brain Stimulation"
                if not dst_subdir.exists():
                    shutil.move(str(bs_subdir), str(dst_subdir))
                    print(f"  ✓ Moved subfolder: Brain Stimulation/")
                    # Update Artifact Rejection frontmatter
                    ar_file = dst_subdir / "Artifact Rejection.md"
                    if ar_file.exists():
                        update_frontmatter(ar_file,
                                           new_parent="Brain Stimulation",
                                           new_grand_parent="Data Processing and Analysis")
                else:
                    print(f"  - Subfolder already moved: Brain Stimulation/")

    # 3. Fix links in index.md
    print("\n" + "-" * 60)
    print("Fixing links in index.md...")
    index_file = BEAUCHAMP / "index.md"
    if fix_links_in_file(index_file, moved_files_map):
        print("  ✓ index.md links updated")
    else:
        print("  - No link changes needed in index.md")

    # 4. Fix links in Obsolete/ pages that may reference moved pages
    print("\nFixing links in Obsolete/ pages...")
    obs_count = 0
    for md_file in (BEAUCHAMP / "Obsolete").rglob("*.md"):
        if fix_links_in_file(md_file, moved_files_map):
            obs_count += 1
            print(f"  ✓ Fixed links in Obsolete/{md_file.relative_to(BEAUCHAMP / 'Obsolete')}")
    if obs_count == 0:
        print("  - No link changes needed")

    # 5. Fix links within moved files (cross-references between categories)
    print("\nFixing cross-references in moved files...")
    xref_count = 0
    for cat_dir_name in CATEGORIES:
        cat_dir = BEAUCHAMP / cat_dir_name
        for md_file in cat_dir.rglob("*.md"):
            if fix_links_in_file(md_file, moved_files_map):
                xref_count += 1
    print(f"  ✓ Fixed cross-references in {xref_count} files")

    # 6. Fix links in files outside Beauchamp/
    print("\nFixing links in external wiki pages...")
    ext_count = fix_links_outside_beauchamp(moved_files_map)
    print(f"  ✓ Fixed {ext_count} external files")

    # 7. Update .gitignore for Internal_Notes
    print("\nUpdating .gitignore...")
    gitignore = WORKSPACE / ".gitignore"
    with open(gitignore, "r", encoding="utf-8") as f:
        gi_content = f.read()

    additions = []
    if "pages/Beauchamp/Internal_Notes.md" not in gi_content:
        additions.append("pages/Beauchamp/Internal_Notes.md")
    if "pages/Beauchamp/Internal_Notes/" not in gi_content:
        additions.append("pages/Beauchamp/Internal_Notes/")

    if additions:
        with open(gitignore, "a", encoding="utf-8") as f:
            f.write("\n# Internal notes (not published)\n")
            for entry in additions:
                f.write(entry + "\n")
        print(f"  ✓ Added {len(additions)} entries to .gitignore")
    else:
        print("  - .gitignore already up to date")

    # 8. Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Pages moved:        {total_moved}")
    print(f"  Cross-refs fixed:   {xref_count}")
    print(f"  External fixes:     {ext_count}")
    if skipped:
        print(f"  Skipped (not found): {len(skipped)}")
        for s in skipped:
            print(f"    - {s}")
    print("=" * 60)


if __name__ == "__main__":
    main()
