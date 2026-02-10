#!/usr/bin/env python3
"""
OpenWetWare Wiki Migration Tool
================================
Converts an OpenWetWare wiki namespace to local Markdown files with offline media.

Usage:
    python migrate.py crawl        # Step 1: Crawl wiki, discover pages, download & convert
    python migrate.py fix          # Step 2: Fix all remaining external references
    python migrate.py audit        # Step 3: Audit for any remaining external references
    python migrate.py inventory    # Step 4: Generate TODO.md and BROKEN_LINKS.md

Configuration: Edit the CONFIG section below before running.

Dependencies:
    pip install requests beautifulsoup4 markdownify
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path
from urllib.parse import unquote, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — Edit this section for your wiki
# ═══════════════════════════════════════════════════════════════════════════════

WIKI_BASE = "https://openwetware.org"

# Primary namespace to crawl (ALL pages under this namespace are downloaded)
PRIMARY_NAMESPACE = "RAVE"

# The home page URL for the primary namespace
HOME_PAGE_URL = f"{WIKI_BASE}/wiki/{PRIMARY_NAMESPACE}"

# Seed pages: add known pages here. Format: (wiki_url,)
# The crawler will discover more pages automatically from links.
# Leave empty to start from just the home page.
SEED_PAGES = [
    f"{WIKI_BASE}/wiki/RAVE:OldHome",
    f"{WIKI_BASE}/wiki/RAVE:Install",
    f"{WIKI_BASE}/wiki/RAVE:Update",
    f"{WIKI_BASE}/wiki/RAVE:Launching",
    f"{WIKI_BASE}/wiki/RAVE:Help",
    f"{WIKI_BASE}/wiki/RAVE:Community",
    f"{WIKI_BASE}/wiki/RAVE:Tutorial_Preprocessing",
    f"{WIKI_BASE}/wiki/RAVE:Tutorial_Clusters",
]

# One-hop namespaces: pages from these wikis are downloaded ONLY if linked
# from the primary namespace. They are NOT recursively crawled.
ONE_HOP_NAMESPACES = ["YAEL", "Beauchamp", "CAMRI", "Karas_Lab", "BeauchampLab"]

# Navigation header template (relative links filled in per-page)
NAV_PAGES = [
    ("Home", "index.md"),
    ("Install", "Install.md"),
    ("Help", "Help.md"),
]

# CDN hosts used by OpenWetWare
CDN_PUBLIC = "oww-files-public.sfo3.cdn.digitaloceanspaces.com"
CDN_THUMB = "oww-files-thumb.sfo3.cdn.digitaloceanspaces.com"

# Media file extensions to download
MEDIA_EXTENSIONS = {
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".wav", ".mp3", ".mp4",
    ".zip", ".csv", ".docx", ".mat", ".ppt", ".pptx", ".doc", ".xls",
}

# Politeness delay between page fetches (seconds)
FETCH_DELAY = 0.5

# ═══════════════════════════════════════════════════════════════════════════════
# END CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent
PAGES_DIR = BASE_DIR / "pages"
ATTACH_DIR = BASE_DIR / "attachments"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh) WikiMigrator/2.0"
})


# ─── Helpers ──────────────────────────────────────────────────────────────────

def wiki_url_to_name(url):
    """Extract wiki page name from a full URL or /wiki/ path.
    E.g. 'https://openwetware.org/wiki/Beauchamp:Foo' -> 'Beauchamp:Foo'
    """
    url = url.split("#")[0].split("?")[0]  # strip fragment and query
    m = re.search(r"/wiki/(.+)$", url)
    return unquote(m.group(1)) if m else None


def wiki_name_to_local_path(wiki_name):
    """Convert a wiki page name to a local .md file path.
    'Beauchamp:Publications' -> 'pages/Beauchamp/Publications.md'
    'RAVE:Install'           -> 'pages/RAVE/Install.md'
    'Beauchamp'              -> 'pages/Beauchamp/index.md'
    'Some_Page'              -> 'pages/Some_Page.md'
    """
    if ":" in wiki_name:
        ns, page = wiki_name.split(":", 1)
        page = page.replace(" ", "_").replace(":", "_")
        return f"pages/{ns}/{page}.md"
    # Bare name — check if it's a known namespace (would be their index page)
    all_ns = [PRIMARY_NAMESPACE] + ONE_HOP_NAMESPACES
    if wiki_name in all_ns:
        return f"pages/{wiki_name}/index.md"
    return f"pages/{wiki_name.replace(' ', '_')}.md"


def get_attachment_section(wiki_name):
    """Determine attachment subfolder name from wiki page name."""
    if ":" in wiki_name:
        ns, page = wiki_name.split(":", 1)
        page = page.replace(" ", "_")
        if ns == PRIMARY_NAMESPACE:
            return page
        return f"{ns}_{page}"
    return wiki_name.replace(" ", "_")


def make_relative(from_md, to_md):
    """Compute relative path between two paths (both relative to BASE_DIR)."""
    from_dir = os.path.dirname(from_md)
    return os.path.relpath(to_md, from_dir)


def download_file(url, dest_path):
    """Download a file. Returns True on success. Skips if already exists."""
    dest = Path(dest_path)
    if dest.exists() and dest.stat().st_size > 0:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = SESSION.get(url, timeout=60, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        if dest.stat().st_size == 0:
            dest.unlink()
            return False
        return True
    except Exception as e:
        print(f"    [WARN] Download failed: {url} — {e}")
        if dest.exists():
            dest.unlink()
        return False


def thumb_to_full(url):
    """Convert a CDN thumbnail URL to the full-size image URL.
    Replace 'oww-files-thumb' with 'oww-files-public' and drop the last
    path segment (the thumbnail-sized filename like /250px-image.jpg).
    """
    url = url.replace(CDN_THUMB, CDN_PUBLIC)
    parts = url.split("/")
    return "/".join(parts[:-1])  # drop last segment


def resolve_file_via_api(filename):
    """Resolve a File:name via MediaWiki API to get the actual download URL."""
    api_url = f"{WIKI_BASE}/mediawiki/api.php"
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    }
    try:
        r = SESSION.get(api_url, params=params, timeout=10)
        data = r.json()
        for pid, pdata in data.get("query", {}).get("pages", {}).items():
            if pid == "-1":
                continue
            ii = pdata.get("imageinfo", [])
            if ii:
                return ii[0].get("url", "")
    except Exception:
        pass
    return None


def build_local_pages_map():
    """Walk pages/ directory and build wiki_name -> relative_path map."""
    pages = {}
    for root, dirs, files in os.walk(PAGES_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, PAGES_DIR)
            parts = rel.replace(".md", "").split(os.sep)
            if len(parts) == 2:
                wiki_name = f"{parts[0]}:{parts[1]}"
            elif len(parts) == 1:
                wiki_name = parts[0]
            else:
                continue
            pages[wiki_name] = os.path.relpath(full, BASE_DIR)
    return pages


def build_attachments_map():
    """Walk attachments/ and build filename.lower() -> full_path map."""
    atts = {}
    for root, dirs, files in os.walk(ATTACH_DIR):
        for f in files:
            atts[f.lower()] = os.path.join(root, f)
    return atts


def resolve_wiki_name(wiki_name, local_pages):
    """Multi-strategy resolution of a wiki name to a local page path."""
    if wiki_name in local_pages:
        return local_pages[wiki_name]
    us = wiki_name.replace(" ", "_")
    if us in local_pages:
        return local_pages[us]
    if f"{wiki_name}:index" in local_pages:
        return local_pages[f"{wiki_name}:index"]
    lower = wiki_name.lower()
    for k, v in local_pages.items():
        if k.lower() == lower:
            return v
    return None


# ─── Step 1: Crawl & Convert ─────────────────────────────────────────────────

def fetch_and_convert(wiki_name, wiki_url):
    """Fetch a wiki page, convert to Markdown, download media.
    Returns (markdown_content, [(media_url, local_dest), ...], [discovered_wiki_names])
    """
    local_path = wiki_name_to_local_path(wiki_name)
    att_section = get_attachment_section(wiki_name)
    file_dir = os.path.dirname(local_path)

    # Fetch
    resp = SESSION.get(wiki_url, timeout=30)
    if resp.status_code != 200:
        return None, [], [], f"HTTP {resp.status_code}"
    if "noarticletext" in resp.text or "There is currently no text" in resp.text:
        return None, [], [], "Page does not exist (404)"

    soup = BeautifulSoup(resp.text, "html.parser")
    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div:
        return None, [], [], "No #mw-content-text div"

    # Clean HTML
    for tag in content_div.find_all("span", class_="mw-editsection"):
        tag.decompose()
    for tag in content_div.find_all("div", class_="catlinks"):
        tag.decompose()
    for tag in content_div.find_all("div", id="toc"):
        tag.decompose()

    # Discover linked pages and rewrite links
    discovered = []
    media_downloads = []

    for a_tag in content_div.find_all("a", href=True):
        href = a_tag["href"]

        # Red links (non-existent pages)
        if "redlink=1" in href or a_tag.get("class") == ["new"]:
            a_tag["href"] = "#"
            a_tag["title"] = f"{a_tag.get_text()} - red link"
            continue

        # Internal wiki links
        if href.startswith("/wiki/"):
            target_name = unquote(href.split("/wiki/")[1].split("#")[0])
            fragment = ""
            if "#" in href:
                fragment = "#" + href.split("#")[1]

            # File: links
            if target_name.startswith("File:"):
                filename = target_name[5:]
                media_url = resolve_file_via_api(filename)
                if media_url:
                    fn_clean = unquote(filename).replace(" ", "_")
                    dest = str(ATTACH_DIR / att_section / fn_clean)
                    media_downloads.append((media_url, dest))
                    a_tag["href"] = make_relative(local_path, dest)
                else:
                    a_tag["href"] = "#"
                    a_tag["title"] = f"File:{filename} - not available"
                continue

            # Wiki page links
            if ":" in target_name:
                ns = target_name.split(":")[0]
                all_ns = [PRIMARY_NAMESPACE] + ONE_HOP_NAMESPACES
                if ns in all_ns:
                    target_local = wiki_name_to_local_path(target_name)
                    a_tag["href"] = make_relative(local_path, target_local) + fragment
                    discovered.append(target_name)
                    continue
            elif target_name == PRIMARY_NAMESPACE:
                a_tag["href"] = make_relative(local_path, wiki_name_to_local_path(target_name)) + fragment
                continue

            # Other /wiki/ links — leave as full URL
            a_tag["href"] = WIKI_BASE + href

    # Rewrite CDN image srcs
    for img in content_div.find_all("img", src=True):
        src = img["src"]
        if CDN_THUMB in src or CDN_PUBLIC in src:
            if CDN_THUMB in src:
                full_url = thumb_to_full(src)
            else:
                full_url = src
            filename = unquote(full_url.split("/")[-1]).replace(" ", "_")
            dest = str(ATTACH_DIR / att_section / filename)
            media_downloads.append((full_url, dest))
            img["src"] = make_relative(local_path, dest)

    # Convert to Markdown
    markdown = md(str(content_div), heading_style="ATX", strip=["div", "span"])

    # Clean up
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)  # collapse blank lines
    markdown = re.sub(r'Retrieved from "[^"]*"', "", markdown)  # strip footers
    markdown = re.sub(r"\[edit\]", "", markdown)  # strip edit links

    # Build navigation header
    if ":" in wiki_name:
        ns = wiki_name.split(":")[0]
        if ns == PRIMARY_NAMESPACE:
            nav_parts = []
            for label, target in NAV_PAGES:
                target_full = f"pages/{PRIMARY_NAMESPACE}/{target}"
                nav_parts.append(f"[{label}]({make_relative(local_path, target_full)})")
            nav = "> **Navigation:** " + " | ".join(nav_parts) + "\n\n"
        else:
            nav = f"> **Navigation:** [{ns} Home]({make_relative(local_path, f'pages/{ns}/index.md')})\n\n"
    else:
        nav = ""

    title = wiki_name.split(":")[-1].replace("_", " ")
    full_content = f"{nav}# {title}\n\n{markdown}".rstrip() + "\n"

    return full_content, media_downloads, discovered, None


def cmd_crawl(args):
    """Step 1: Crawl the wiki, discover pages, convert to Markdown."""
    print("=" * 70)
    print(f"CRAWLING: {WIKI_BASE}/wiki/{PRIMARY_NAMESPACE}")
    print("=" * 70)

    # Seed the queue
    queue = set()
    visited = set()
    queue.add(PRIMARY_NAMESPACE)

    # Add seed pages
    for url in SEED_PAGES:
        name = wiki_url_to_name(url)
        if name:
            queue.add(name)

    # Load already-converted pages
    local_pages = build_local_pages_map()
    if args.force:
        # With --force, only mark non-primary pages as visited
        # so primary namespace pages are re-crawled and their links discovered
        for name in local_pages:
            if ":" in name:
                ns = name.split(":")[0]
                if ns != PRIMARY_NAMESPACE:
                    visited.add(name)
            elif name != PRIMARY_NAMESPACE:
                visited.add(name)
        print(f"  Force mode: will re-convert {PRIMARY_NAMESPACE} pages")
    else:
        for name in local_pages:
            visited.add(name)
        print(f"  Skipping {len(visited)} already-converted pages (use --force to re-convert)")

    total_downloaded = 0
    total_converted = 0
    total_failed = 0
    round_num = 0

    while queue - visited:
        round_num += 1
        batch = list(queue - visited)
        print(f"\n--- Round {round_num}: {len(batch)} pages to process ---")

        new_discovered = set()

        for wiki_name in sorted(batch):
            # Scope check
            if ":" in wiki_name:
                ns = wiki_name.split(":")[0]
                all_ns = [PRIMARY_NAMESPACE] + ONE_HOP_NAMESPACES
                if ns not in all_ns:
                    visited.add(wiki_name)
                    continue
                # Don't crawl one-hop pages recursively
                if ns != PRIMARY_NAMESPACE and ns in ONE_HOP_NAMESPACES:
                    # Only download, don't add their links to queue
                    pass
            elif wiki_name not in [PRIMARY_NAMESPACE]:
                # Unknown bare page — skip unless it's the home
                visited.add(wiki_name)
                continue

            local_path = wiki_name_to_local_path(wiki_name)
            full_local = BASE_DIR / local_path

            if full_local.exists() and not args.force:
                visited.add(wiki_name)
                continue

            wiki_url = f"{WIKI_BASE}/wiki/{wiki_name}"
            print(f"  Converting: {wiki_name}")

            content, media, discovered, error = fetch_and_convert(wiki_name, wiki_url)
            visited.add(wiki_name)

            if error:
                print(f"    ERROR: {error}")
                total_failed += 1
                continue

            # Write page
            full_local.parent.mkdir(parents=True, exist_ok=True)
            full_local.write_text(content)
            total_converted += 1

            # Download media
            for url, dest in media:
                if download_file(url, dest):
                    total_downloaded += 1

            # Queue discovered pages (only from primary namespace pages)
            if ":" in wiki_name and wiki_name.split(":")[0] == PRIMARY_NAMESPACE:
                for d in discovered:
                    new_discovered.add(d)
            elif wiki_name == PRIMARY_NAMESPACE:
                for d in discovered:
                    new_discovered.add(d)

            time.sleep(FETCH_DELAY)

        queue.update(new_discovered)

    print(f"\n{'=' * 70}")
    print(f"CRAWL COMPLETE")
    print(f"  Pages converted: {total_converted}")
    print(f"  Media downloaded: {total_downloaded}")
    print(f"  Failures: {total_failed}")
    print(f"  Total pages in workspace: {len(build_local_pages_map())}")
    print(f"{'=' * 70}")


# ─── Step 2: Fix References ──────────────────────────────────────────────────

def cmd_fix(args):
    """Step 2: Fix all remaining external references in converted pages."""
    print("=" * 70)
    print("FIXING EXTERNAL REFERENCES")
    print("=" * 70)

    local_pages = build_local_pages_map()
    attachments_map = build_attachments_map()
    print(f"  Local pages: {len(local_pages)}")
    print(f"  Attachments: {len(attachments_map)}")

    broken_links = set()
    fixed_files = 0

    for root, dirs, files in os.walk(PAGES_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)

            with open(filepath, "r") as f:
                content = f.read()

            # Quick check — skip files with no external references
            needs_fix = (
                "/wiki/" in content
                or CDN_PUBLIC in content
                or CDN_THUMB in content
                or "openwetware.org" in content
            )
            if not needs_fix:
                continue

            original = content
            rel_path = os.path.relpath(filepath, PAGES_DIR)
            file_dir = os.path.dirname(os.path.relpath(filepath, BASE_DIR))

            # Determine attachment section
            parts = rel_path.replace(".md", "").split(os.sep)
            if len(parts) == 2:
                att_section = f"{parts[0]}_{parts[1]}" if parts[0] != PRIMARY_NAMESPACE else parts[1]
            else:
                att_section = parts[0]

            def _make_rel_from_file(target_path):
                return os.path.relpath(target_path, os.path.join(BASE_DIR, file_dir))

            # --- Fix markdown links [text](url "title") ---
            def fix_md_link(match):
                prefix = match.group(1)
                text = match.group(2)
                url_and_title = match.group(3)

                url_m = re.match(r"(\S+?)(\s+\"[^\"]*\")?$", url_and_title)
                if not url_m:
                    return match.group(0)
                url = url_m.group(1)
                title = url_m.group(2) or ""

                # CDN thumbnails
                if CDN_THUMB in url:
                    full_url = thumb_to_full(url)
                    filename = unquote(full_url.split("/")[-1]).replace(" ", "_")
                    dest = str(ATTACH_DIR / att_section / filename)
                    if download_file(full_url, dest):
                        return f"{prefix}{text}]({_make_rel_from_file(dest)}{title})"
                    broken_links.add(url)
                    return match.group(0)

                # CDN public
                if CDN_PUBLIC in url:
                    filename = unquote(url.split("/")[-1]).replace(" ", "_")
                    dest = str(ATTACH_DIR / att_section / filename)
                    if download_file(url, dest):
                        return f"{prefix}{text}]({_make_rel_from_file(dest)}{title})"
                    broken_links.add(url)
                    return match.group(0)

                # /wiki/File: links
                fm = re.match(r"/wiki/File:(.+)", url)
                if fm:
                    filename = unquote(fm.group(1)).replace(" ", "_")
                    if filename.lower() in attachments_map:
                        return f"{prefix}{text}]({_make_rel_from_file(attachments_map[filename.lower()])}{title})"
                    media_url = resolve_file_via_api(fm.group(1))
                    if media_url:
                        dest = str(ATTACH_DIR / att_section / filename)
                        if download_file(media_url, dest):
                            return f"{prefix}{text}]({_make_rel_from_file(dest)}{title})"
                    broken_links.add(f"/wiki/File:{fm.group(1)}")
                    return f'{prefix}{text}](# "File:{fm.group(1)} - not available"{title})'

                # /wiki/Namespace:Page links
                wm = re.match(r"/wiki/(.+?)(?:#(.+))?$", url)
                if wm:
                    wiki_name = unquote(wm.group(1))
                    fragment = f"#{wm.group(2)}" if wm.group(2) else ""
                    local = resolve_wiki_name(wiki_name, local_pages)
                    if local:
                        return f"{prefix}{text}]({_make_rel_from_file(local)}{fragment}{title})"
                    broken_links.add(f"/wiki/{wiki_name}")
                    return f'{prefix}{text}](# "{wiki_name} - not archived"{title})'

                # Full openwetware URLs
                if "openwetware.org" in url:
                    wm2 = re.search(r"/wiki/(.+?)(?:#(.+))?$", url)
                    if wm2:
                        wiki_name = unquote(wm2.group(1))
                        fragment = f"#{wm2.group(2)}" if wm2.group(2) else ""
                        if wiki_name.startswith("File:"):
                            fn = wiki_name[5:].replace(" ", "_")
                            if fn.lower() in attachments_map:
                                return f"{prefix}{text}]({_make_rel_from_file(attachments_map[fn.lower()])}{title})"
                            broken_links.add(url)
                            return f'{prefix}{text}](# "{wiki_name} - not available"{title})'
                        local = resolve_wiki_name(wiki_name, local_pages)
                        if local:
                            return f"{prefix}{text}]({_make_rel_from_file(local)}{fragment}{title})"
                        broken_links.add(url)
                        return f'{prefix}{text}](# "{wiki_name} - not archived"{title})'

                return match.group(0)

            content = re.sub(r"(!?\[)([^\]]*)\]\(([^)]+)\)", fix_md_link, content)

            # --- Fix bare CDN URLs ---
            def fix_bare_cdn(match):
                url = match.group(0)
                if CDN_THUMB in url:
                    full_url = thumb_to_full(url)
                else:
                    full_url = url
                filename = unquote(full_url.split("/")[-1]).replace(" ", "_")
                dest = str(ATTACH_DIR / att_section / filename)
                if download_file(full_url, dest):
                    return _make_rel_from_file(dest)
                return url

            content = re.sub(
                rf"https?://(?:{re.escape(CDN_PUBLIC)}|{re.escape(CDN_THUMB)})/[^\s)<\]\"]+",
                fix_bare_cdn, content,
            )

            # --- Fix angle-bracket URLs <https://openwetware.org/wiki/...> ---
            def fix_angle_bracket_url(match):
                url = match.group(1)
                wm = re.search(r"/wiki/(.+?)(?:#(.+))?$", url)
                if not wm:
                    return match.group(0)
                wiki_name = unquote(wm.group(1))
                fragment = f"#{wm.group(2)}" if wm.group(2) else ""
                local = resolve_wiki_name(wiki_name, local_pages)
                if local:
                    display = wiki_name.split(":")[-1].replace("_", " ")
                    return f"[{display}]({_make_rel_from_file(local)}{fragment})"
                broken_links.add(url)
                display = wiki_name.split(":")[-1].replace("_", " ")
                return f"~~{display}~~ *(page not archived)*"

            content = re.sub(
                r"<(https?://(?:www\.)?openwetware\.org/wiki/[^>]+)>",
                fix_angle_bracket_url, content,
            )

            # --- Fix bare openwetware URLs not in markdown links ---
            def fix_bare_oww_url(match):
                url = match.group(0)
                wm = re.search(r"/wiki/(.+?)(?:#(.+))?$", url)
                if not wm:
                    return url
                wiki_name = unquote(wm.group(1))
                fragment = f"#{wm.group(2)}" if wm.group(2) else ""
                local = resolve_wiki_name(wiki_name, local_pages)
                if local:
                    display = wiki_name.split(":")[-1].replace("_", " ")
                    return f"[{display}]({_make_rel_from_file(local)}{fragment})"
                return url

            content = re.sub(
                r"(?<![(<\[])https?://(?:www\.)?openwetware\.org/wiki/[^\s)>\]\"]+",
                fix_bare_oww_url, content,
            )

            # --- Fix ``url`` (archived) (archived) patterns ---
            def fix_backtick_archived(match):
                url = match.group(1)
                wm = re.search(r"/wiki/(.+?)(?:#.*)?$", url)
                if not wm:
                    return match.group(0)
                wiki_name = unquote(wm.group(1))
                local = resolve_wiki_name(wiki_name, local_pages)
                if local:
                    display = wiki_name.split(":")[-1].replace("_", " ")
                    return f"[{display}]({_make_rel_from_file(local)})"
                display = wiki_name.split(":")[-1].replace("_", " ")
                broken_links.add(url)
                return f"~~{display}~~ *(page not archived)*"

            content = re.sub(
                r"``(https?://(?:www\.)?openwetware\.org/wiki/[^`]+)``\s*(?:\(archived\)\s*)*",
                fix_backtick_archived, content,
            )

            # --- Remove "Retrieved from" footers ---
            content = re.sub(
                r'\n*Retrieved from "[<]*https?://[^"]*openwetware[^"]*[>]*"\s*\n*',
                "\n", content,
            )

            # --- Fix text mentions ---
            content = content.replace("site:openwetware.org", "in the local wiki pages")
            content = re.sub(
                r"Google\s+\*\*([^*]+)\s+in\s+openwetware\.org/wiki/\w+\*\*",
                r"search **\1 in the local wiki pages**",
                content,
            )

            # --- Re-resolve broken markers ---
            def fix_anchor_link(match):
                text = match.group(1)
                wiki_name = match.group(2)
                local = resolve_wiki_name(wiki_name, local_pages)
                if not local:
                    local = resolve_wiki_name(wiki_name.replace(" ", "_"), local_pages)
                if local:
                    return f"[{text}]({_make_rel_from_file(local)})"
                broken_links.add(wiki_name)
                return match.group(0)

            content = re.sub(
                r'\[([^\]]+)\]\(#\s+"([^"]+)\s+-\s+not archived"(?:\s+"[^"]*")?\)',
                fix_anchor_link, content,
            )

            def fix_strikethrough(match):
                name = match.group(1)
                ns = parts[0] if len(parts) == 2 else ""
                for c in [f"{ns}:{name}", f"{ns}:{name.replace(' ', '_')}", name, name.replace(" ", "_")]:
                    if c and c in local_pages:
                        return f"[{name}]({_make_rel_from_file(local_pages[c])})"
                return match.group(0)

            content = re.sub(
                r"~~([^~]+)~~\s*\*\(page not archived\)\*",
                fix_strikethrough, content,
            )

            content = content.rstrip() + "\n"

            if content != original:
                with open(filepath, "w") as f:
                    f.write(content)
                rel = os.path.relpath(filepath, BASE_DIR)
                print(f"  Fixed: {rel}")
                fixed_files += 1

    print(f"\nFixed {fixed_files} files")
    if broken_links:
        print(f"{len(broken_links)} broken links (see BROKEN_LINKS.md after running 'inventory')")

    # Write broken links for inventory step
    bl_file = BASE_DIR / ".broken_links_cache.json"
    existing = set()
    if bl_file.exists():
        existing = set(json.loads(bl_file.read_text()))
    existing.update(broken_links)
    bl_file.write_text(json.dumps(sorted(existing)))


# ─── Step 3: Audit ───────────────────────────────────────────────────────────

def cmd_audit(args):
    """Step 3: Audit all pages for remaining external references."""
    print("=" * 70)
    print("AUDITING FOR EXTERNAL REFERENCES")
    print("=" * 70)

    patterns = {
        "openwetware.org": "OWW URL",
        CDN_PUBLIC: "CDN public",
        CDN_THUMB: "CDN thumb",
    }

    remaining = []
    for root, dirs, files in os.walk(PAGES_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            with open(filepath) as f:
                for i, line in enumerate(f, 1):
                    for pattern, label in patterns.items():
                        if pattern in line:
                            rel = os.path.relpath(filepath, BASE_DIR)
                            remaining.append((label, rel, i, line.strip()[:140]))

    # Also check for unconverted /wiki/ links
    for root, dirs, files in os.walk(PAGES_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            with open(filepath) as f:
                for i, line in enumerate(f, 1):
                    if re.search(r"\(/wiki/", line):
                        rel = os.path.relpath(filepath, BASE_DIR)
                        remaining.append(("/wiki/ link", rel, i, line.strip()[:140]))

    if remaining:
        print(f"\n{len(remaining)} remaining references:\n")
        for label, path, line, text in remaining:
            print(f"  [{label}] {path}:{line}: {text}")
        print(f"\nRun 'python migrate.py fix' to attempt to resolve these.")
    else:
        print("\n  ✓ ZERO external references remain. Full offline capability achieved.")

    return len(remaining)


# ─── Step 4: Inventory ───────────────────────────────────────────────────────

def cmd_inventory(args):
    """Step 4: Generate TODO.md and BROKEN_LINKS.md."""
    print("=" * 70)
    print("GENERATING INVENTORY")
    print("=" * 70)

    # --- TODO.md ---
    namespaces = {}
    root_pages = []
    for root, dirs, files in os.walk(PAGES_DIR):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), PAGES_DIR)
            parts = rel.split(os.sep)
            if len(parts) == 2:
                ns = parts[0]
                name = parts[1].replace(".md", "")
                namespaces.setdefault(ns, []).append(name)
            elif len(parts) == 1:
                root_pages.append(parts[0].replace(".md", ""))

    att_count = sum(1 for _, _, fs in os.walk(ATTACH_DIR) for _ in fs)

    with open(BASE_DIR / "TODO.md", "w") as f:
        f.write("# Wiki Migration — Complete\n\n")
        total = sum(len(v) for v in namespaces.values()) + len(root_pages)
        f.write(f"**{total} pages** converted, **{att_count} attachments** downloaded.\n\n---\n\n")

        for ns in sorted(namespaces.keys()):
            pages = namespaces[ns]
            marker = "Primary" if ns == PRIMARY_NAMESPACE else "One-hop"
            f.write(f"## {ns} ({len(pages)} pages, {marker})\n\n")
            for p in sorted(pages):
                f.write(f"- [x] **{p.replace('_', ' ')}** — `pages/{ns}/{p}.md`\n")
            f.write("\n")

        if root_pages:
            f.write(f"## Root-Level Pages ({len(root_pages)})\n\n")
            for p in sorted(root_pages):
                f.write(f"- [x] **{p.replace('_', ' ')}** — `pages/{p}.md`\n")
            f.write("\n")

        f.write("---\n\n")
        f.write(f"| Category | Count |\n|----------|-------|\n")
        for ns in sorted(namespaces.keys()):
            f.write(f"| {ns} | {len(namespaces[ns])} |\n")
        if root_pages:
            f.write(f"| Root-level | {len(root_pages)} |\n")
        f.write(f"| **Total pages** | **{total}** |\n")
        f.write(f"| Attachments | {att_count} |\n")

    print(f"  Wrote TODO.md ({total} pages, {att_count} attachments)")

    # --- BROKEN_LINKS.md ---
    all_broken = {}
    for root, dirs, files in os.walk(PAGES_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath) as fh:
                content = fh.read()
            entries = []
            for m in re.finditer(r'\[([^\]]+)\]\(#\s+"([^"]+)\s+-\s+not archived"', content):
                entries.append(("Page not available", m.group(2)))
            for m in re.finditer(r'\[([^\]]+)\]\(#\s+"([^"]+)\s+-\s+not available"', content):
                entries.append(("File not available", m.group(2)))
            for m in re.finditer(r"~~([^~]+)~~\s*\*\(page not archived\)\*", content):
                entries.append(("Page not archived (404)", m.group(1)))
            if entries:
                all_broken[rel] = entries

    bl_count = sum(len(v) for v in all_broken.values())
    with open(BASE_DIR / "BROKEN_LINKS.md", "w") as f:
        f.write("# Broken Links Report\n\n")
        f.write("Links that could not be resolved during migration.\n\n")
        for filepath, entries in sorted(all_broken.items()):
            f.write(f"## [{filepath}]({filepath})\n\n")
            for btype, bname in entries:
                f.write(f"- {btype}: `{bname}`\n")
            f.write("\n")
        f.write(f"---\n*Total: {bl_count} broken links*\n")

    print(f"  Wrote BROKEN_LINKS.md ({bl_count} broken links)")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OpenWetWare Wiki Migration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Steps:
  1. python migrate.py crawl       Crawl wiki, convert pages, download media
  2. python migrate.py fix         Fix remaining external references (run multiple times)
  3. python migrate.py audit       Verify zero external references remain
  4. python migrate.py inventory   Generate TODO.md and BROKEN_LINKS.md
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_crawl = sub.add_parser("crawl", help="Crawl wiki and convert pages")
    p_crawl.add_argument("--force", action="store_true", help="Re-convert already-existing pages")

    p_fix = sub.add_parser("fix", help="Fix remaining external references")
    p_fix.add_argument("--force", action="store_true")

    p_audit = sub.add_parser("audit", help="Audit for remaining external references")
    p_audit.add_argument("--force", action="store_true")

    p_inv = sub.add_parser("inventory", help="Generate TODO.md and BROKEN_LINKS.md")
    p_inv.add_argument("--force", action="store_true")

    args = parser.parse_args()

    if args.command == "crawl":
        cmd_crawl(args)
    elif args.command == "fix":
        cmd_fix(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "inventory":
        cmd_inventory(args)


if __name__ == "__main__":
    main()
