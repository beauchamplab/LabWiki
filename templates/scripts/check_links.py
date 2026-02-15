#!/usr/bin/env python3
"""
Link Checker for Beauchamp Lab Wiki

This script checks for broken internal links in the wiki, including:
- Markdown links to other pages
- Links to attachment files (images, PDFs, etc.)
- Cross-namespace references

Usage:
    python3 scripts/check_links.py [--fix] [--verbose]

Options:
    --fix       Attempt to automatically fix broken links where possible
    --verbose   Show detailed output for each file processed
    --report    Generate a detailed report file

Output:
    - Lists all broken links found
    - Compares with pages/BROKEN_LINKS.md to find new issues
    - Optionally attempts to fix common issues

Common issues detected:
    1. Links to moved/renamed files
    2. Broken attachment references
    3. Invalid relative paths
    4. Links with incorrect file extensions (.html vs .md)
    5. Case sensitivity issues
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple
import argparse


class LinkChecker:
    def __init__(self, base_dir: Path, verbose: bool = False):
        self.base_dir = base_dir
        self.pages_dir = base_dir / "pages"
        self.attachments_dir = base_dir / "attachments"
        self.verbose = verbose
        
        # Track all available files
        self.available_pages: Set[Path] = set()
        self.available_attachments: Set[Path] = set()
        
        # Track issues
        self.broken_links: Dict[str, List[Tuple[int, str, str]]] = defaultdict(list)
        self.fixed_links: Dict[str, List[str]] = defaultdict(list)
        
    def scan_available_files(self):
        """Build index of all available pages and attachments"""
        if self.verbose:
            print("Scanning available files...")
        
        # Find all markdown pages
        for md_file in self.pages_dir.rglob("*.md"):
            self.available_pages.add(md_file.relative_to(self.pages_dir))
        
        # Find all attachments
        if self.attachments_dir.exists():
            for att_file in self.attachments_dir.rglob("*"):
                if att_file.is_file():
                    self.available_attachments.add(att_file.relative_to(self.attachments_dir))
        
        if self.verbose:
            print(f"  Found {len(self.available_pages)} pages")
            print(f"  Found {len(self.available_attachments)} attachments")
    
    def extract_links(self, content: str, file_path: Path) -> List[Tuple[int, str, str]]:
        """
        Extract all markdown links from content.
        Returns: [(line_number, link_text, link_url), ...]
        """
        links = []
        
        # Pattern for markdown links: [text](url) or [text](url "title")
        # Also handle image links: ![alt](url)
        pattern = r'!?\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)'
        
        for line_num, line in enumerate(content.split('\n'), 1):
            for match in re.finditer(pattern, line):
                link_text = match.group(1)
                link_url = match.group(2)
                
                # Skip external links (http, https, mailto, etc.)
                if re.match(r'^[a-zA-Z]+://', link_url):
                    continue
                
                # Skip anchors only
                if link_url.startswith('#'):
                    continue
                
                links.append((line_num, link_text, link_url))
        
        return links
    
    def resolve_link(self, source_file: Path, link_url: str) -> Tuple[bool, str]:
        """
        Check if a link can be resolved.
        Returns: (is_valid, suggested_fix_or_error_message)
        """
        # Remove anchor if present
        clean_url = link_url.split('#')[0]
        
        if not clean_url:
            return True, ""  # Just an anchor
        
        # Resolve relative to source file's directory
        source_dir = source_file.parent
        
        # Try to resolve as markdown file
        if clean_url.endswith('.md') or clean_url.endswith('.html'):
            # Convert .html to .md for checking
            check_url = clean_url.replace('.html', '.md')
            
            # Build absolute path
            if check_url.startswith('../'):
                # Link goes up from current position
                target = (self.pages_dir / source_dir / check_url).resolve()
            elif check_url.startswith('./'):
                # Explicit same directory
                target = (self.pages_dir / source_dir / check_url[2:]).resolve()
            elif '/' in check_url:
                # Path includes directory (e.g., "Beauchamp/Page.md")
                target = (self.pages_dir / check_url).resolve()
            else:
                # No path separator - same directory as source
                target = (self.pages_dir / source_dir / check_url).resolve()
            
            try:
                rel_target = target.relative_to(self.pages_dir)
                if rel_target in self.available_pages:
                    return True, ""
                
                # Try to find a similar file (case-insensitive or similar name)
                suggestion = self.find_similar_file(rel_target, self.available_pages)
                if suggestion:
                    return False, f"File not found. Did you mean: {suggestion}?"
                return False, f"File not found: {rel_target}"
            except ValueError:
                return False, f"Link points outside pages directory: {clean_url}"
        
        # Try to resolve as attachment
        if clean_url.startswith('../../attachments/') or clean_url.startswith('../attachments/'):
            # Extract attachment path
            att_path = re.sub(r'^(\.\./)+attachments/', '', clean_url)
            att_path = Path(att_path)
            
            if att_path in self.available_attachments:
                return True, ""
            
            # Try to find similar attachment
            suggestion = self.find_similar_file(att_path, self.available_attachments)
            if suggestion:
                return False, f"Attachment not found. Did you mean: {suggestion}?"
            return False, f"Attachment not found: {att_path}"
        
        # Unknown link type
        return False, f"Cannot resolve link type: {clean_url}"
    
    def find_similar_file(self, target: Path, available: Set[Path]) -> str:
        """Find similar filenames (case-insensitive or close match)"""
        target_lower = str(target).lower()
        target_name = target.name.lower()
        
        # Check for case-insensitive match
        for available_file in available:
            if str(available_file).lower() == target_lower:
                return str(available_file)
        
        # Check for filename match in different directory
        for available_file in available:
            if available_file.name.lower() == target_name:
                return str(available_file)
        
        return ""
    
    def check_file(self, md_file: Path) -> int:
        """Check all links in a markdown file. Returns count of broken links."""
        rel_path = md_file.relative_to(self.pages_dir)
        
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ⚠ Cannot read {rel_path}: {e}")
            return 0
        
        links = self.extract_links(content, rel_path)
        
        if not links and self.verbose:
            print(f"  ✓ {rel_path} (no links)")
            return 0
        
        broken_count = 0
        for line_num, link_text, link_url in links:
            is_valid, message = self.resolve_link(rel_path, link_url)
            
            if not is_valid:
                self.broken_links[str(rel_path)].append((line_num, link_url, message))
                broken_count += 1
        
        if self.verbose:
            if broken_count > 0:
                print(f"  ✗ {rel_path} ({broken_count} broken links)")
            else:
                print(f"  ✓ {rel_path} ({len(links)} links OK)")
        
        return broken_count
    
    def check_all(self):
        """Check all markdown files in the wiki"""
        self.scan_available_files()
        
        print(f"\nChecking links in {len(self.available_pages)} pages...")
        
        total_broken = 0
        for md_file in sorted(self.pages_dir.rglob("*.md")):
            # Skip excluded files
            if md_file.name in ['TODO.md', 'BROKEN_LINKS.md', 'Prompt.md']:
                continue
            
            broken_count = self.check_file(md_file)
            total_broken += broken_count
        
        return total_broken
    
    def print_report(self):
        """Print summary report of broken links"""
        if not self.broken_links:
            print("\n✓ No broken links found!")
            return
        
        print(f"\n{'='*70}")
        print(f"BROKEN LINKS REPORT")
        print(f"{'='*70}\n")
        
        total_broken = sum(len(links) for links in self.broken_links.values())
        print(f"Found {total_broken} broken links in {len(self.broken_links)} files:\n")
        
        for file_path in sorted(self.broken_links.keys()):
            print(f"\n📄 {file_path}")
            print(f"   {'─'*66}")
            
            for line_num, link_url, message in self.broken_links[file_path]:
                print(f"   Line {line_num:4d}: {link_url}")
                print(f"              → {message}")
    
    def compare_with_known_broken(self):
        """Compare found broken links with pages/BROKEN_LINKS.md"""
        broken_links_file = self.pages_dir / "BROKEN_LINKS.md"
        
        if not broken_links_file.exists():
            print("\n⚠ pages/BROKEN_LINKS.md not found, skipping comparison")
            return
        
        content = broken_links_file.read_text()
        
        # Extract known broken links (simplified parsing)
        known_broken = set()
        for line in content.split('\n'):
            if line.startswith('- Page not archived'):
                match = re.search(r'`([^`]+)`', line)
                if match:
                    known_broken.add(match.group(1))
        
        # Find new broken links
        new_broken = set()
        for file_path, links in self.broken_links.items():
            for _, link_url, _ in links:
                # Extract page name from link
                page_name = Path(link_url).stem
                if page_name not in known_broken:
                    new_broken.add(link_url)
        
        if new_broken:
            print(f"\n{'='*70}")
            print("NEW BROKEN LINKS (not in BROKEN_LINKS.md):")
            print(f"{'='*70}\n")
            for link in sorted(new_broken):
                print(f"  - {link}")
        else:
            print("\n✓ No new broken links beyond those in BROKEN_LINKS.md")
    
    def save_report(self, output_file: Path):
        """Save detailed report to file"""
        from datetime import datetime
        
        with open(output_file, 'w') as f:
            f.write("# Broken Links Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not self.broken_links:
                f.write("✓ No broken links found!\n")
                return
            
            total_broken = sum(len(links) for links in self.broken_links.values())
            f.write(f"Found **{total_broken}** broken links in **{len(self.broken_links)}** files:\n\n")
            
            for file_path in sorted(self.broken_links.keys()):
                f.write(f"\n## [{file_path}](../{file_path})\n\n")
                
                for line_num, link_url, message in self.broken_links[file_path]:
                    f.write(f"- **Line {line_num}**: `{link_url}`\n")
                    f.write(f"  - {message}\n")
        
        print(f"\n✓ Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Check for broken links in Beauchamp Lab Wiki",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output for each file')
    parser.add_argument('--report', '-r', type=str,
                        help='Save detailed report to specified file')
    parser.add_argument('--fix', action='store_true',
                        help='Attempt to automatically fix broken links (not implemented yet)')
    
    args = parser.parse_args()
    
    # Get base directory
    base_dir = Path(__file__).parent.parent
    
    # Create checker
    checker = LinkChecker(base_dir, verbose=args.verbose)
    
    # Run checks
    total_broken = checker.check_all()
    
    # Print report
    checker.print_report()
    
    # Compare with known broken links
    checker.compare_with_known_broken()
    
    # Save report if requested
    if args.report:
        checker.save_report(Path(args.report))
    
    # Exit with error code if broken links found
    sys.exit(1 if total_broken > 0 else 0)


if __name__ == "__main__":
    main()
