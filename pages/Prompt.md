---
layout: default
title: "Prompt: Migrate an OpenWetWare Wiki to Offline Markdown"
---
# Prompt: Migrate an OpenWetWare Wiki to Offline Markdown

Use this prompt to instruct an AI coding assistant (e.g. GitHub Copilot, Claude) to migrate an OpenWetWare lab wiki to local Markdown files with full offline capability.

---

## The Prompt

> Migrate the lab wiki at `https://openwetware.org/wiki/NAMESPACE` to local Markdown files. The end result must be fully offline-readable — if openwetware.org and its CDN shut down, all content including images must still work.
>
> Use the migration tool `migrate.py` in this repo. Edit the CONFIG section at the top to set the primary namespace and one-hop namespaces, then run the pipeline:
>
> ```
> python migrate.py crawl       # Discover & convert all pages
> python migrate.py fix         # Fix remaining external references
> python migrate.py fix         # Run again — each pass catches new edge cases
> python migrate.py audit       # Verify zero references remain
> python migrate.py inventory   # Generate TODO.md and BROKEN_LINKS.md
> ```
>
> Repeat `fix` → `audit` until audit returns zero. See the DOs and DON'Ts below.

---

## Step-by-Step Guide

### 1. Setup

```bash
mkdir labwiki && cd labwiki
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 markdownify
```

Copy `migrate.py` into the project root.

### 2. Configure

Edit the CONFIG section in `migrate.py`:

```python
WIKI_BASE = "https://openwetware.org"
PRIMARY_NAMESPACE = "YourLab"          # e.g. "Beauchamp"
HOME_PAGE_URL = f"{WIKI_BASE}/wiki/{PRIMARY_NAMESPACE}"
ONE_HOP_NAMESPACES = ["RAVE", "CAMRI"] # linked wikis to include (not crawled recursively)
```

### 3. Crawl

```bash
python migrate.py crawl
```

This will:
- Start from the home page and follow all internal links
- Download ALL pages under the primary namespace
- Download one-hop pages (pages from other namespaces linked from primary pages)
- Convert HTML → Markdown using `markdownify`
- Download all CDN-hosted media (images, PDFs) to `attachments/`
- Rewrite links to relative local paths

### 4. Fix (run multiple times)

```bash
python migrate.py fix
python migrate.py fix   # yes, run it again
```

Each pass catches edge cases the previous pass missed. Keep running until audit is clean.

### 5. Audit

```bash
python migrate.py audit
```

Must return **ZERO** remaining references. If not, run `fix` again.

### 6. Inventory

```bash
python migrate.py inventory
```

Generates `TODO.md` (all pages with checkboxes) and `BROKEN_LINKS.md` (unresolvable links).

---

## Architecture (What Gets Created)

```
labwiki/
├── migrate.py                    # Migration tool
├── TODO.md                       # Generated inventory
├── BROKEN_LINKS.md               # Unresolvable links
├── pages/
│   ├── YourLab/                  # Primary namespace
│   │   ├── index.md              # Home page
│   │   ├── Publications.md
│   │   └── ...
│   ├── RAVE/                     # One-hop namespaces
│   │   ├── index.md
│   │   └── ...
│   ├── CAMRI/
│   └── SomePage.md               # Root-level pages (no namespace)
└── attachments/
    ├── Publications/             # Media organized by page
    │   ├── paper.pdf
    │   └── figure1.jpg
    ├── RAVE_Install/
    └── ...
```

---

## DOs and DON'Ts

### DOs

1. **DO use Python script files** for all batch operations. Never inline Python in zsh/bash — quoting issues with URLs, special characters, and nested quotes will silently corrupt commands.

2. **DO run `fix` multiple times.** A single regex pass will NOT catch everything. Each pass reveals new edge cases (title attributes, nested links, angle-bracket URLs). Run `fix` → `audit` in a loop until audit returns zero.

3. **DO audit after every fix pass** with `grep -rn 'openwetware.org' pages/` and also `grep -rn 'oww-files' pages/`. The audit command does this automatically.

4. **DO handle title attributes in markdown links.** Links like `[text](url "Beauchamp:PageName")` are common. A naive regex `[^)]+` greedily captures the title as part of the URL. Split URL from title with: `r'(\S+?)(\s+"[^"]*")?$'`

5. **DO handle the CDN thumbnail trick.** Thumbnails are on `oww-files-thumb.sfo3.cdn.digitaloceanspaces.com`. To get the full-size image: replace `oww-files-thumb` with `oww-files-public` in the URL AND drop the last path segment (the `/250px-filename.jpg` part).

6. **DO use the MediaWiki API** to resolve `File:` page links. URL: `{WIKI_BASE}/mediawiki/api.php?action=query&titles=File:{name}&prop=imageinfo&iiprop=url&format=json`. The response contains the actual CDN download URL.

7. **DO strip "Retrieved from" footers.** These are MediaWiki boilerplate at the bottom of every page: `Retrieved from "https://openwetware.org/mediawiki/..."`. Strip them during conversion.

8. **DO strip `[edit]` section links.** These are MediaWiki editing chrome that appears next to every heading.

9. **DO URL-decode filenames** when saving locally (`%2C` → `,`, `%28` → `(`, etc.) and replace spaces with underscores.

10. **DO define scope clearly.** Primary namespace = crawl everything. Other namespaces = one-hop only (download if linked, but do NOT follow their links recursively). This prevents scope creep.

11. **DO use markers for broken links** that can be re-resolved later. Pattern: `](# "WikiName - not archived")` for missing pages, `~~Page Name~~ *(page not archived)*` for 404s.

12. **DO check for nested image-link patterns.** MediaWiki often generates `[![img](thumbnail.jpg)](/wiki/File:FullSize.jpg)` — an image wrapped in a clickable link. Both the `src` and the `href` need to be resolved.

13. **DO extract content from `#mw-content-text` only.** The rest of the page (sidebar, navigation, footer) is wiki chrome, not content.

14. **DO handle multiple URL variations.** The same wiki link can appear as:
    - `/wiki/Beauchamp:Foo` (relative)
    - `https://openwetware.org/wiki/Beauchamp:Foo` (absolute)
    - `http://www.openwetware.org/wiki/Beauchamp:Foo` (http, www)

### DON'Ts

1. **DON'T use inline Python in shell commands.** Zsh and bash have different quoting rules. URLs with special characters (`%`, `(`, `)`, `&`) will break. Always write a `.py` file and run it.

2. **DON'T assume one fix pass is enough.** We needed 5+ rounds of fixing for the Beauchamp wiki (291 initial references → 0). Each pass catches ~60-80% of remaining issues.

3. **DON'T use a simple `[^)]+` regex for markdown link URLs.** It fails on title attributes: `[text](url "title")` — the `)` in `"title")` isn't the closing paren of the link. Also fails on nested image-links `[![](src)](href)`.

4. **DON'T recursively crawl non-primary namespaces.** Other wikis (RAVE, CAMRI, YAEL) have their own structure. Only download pages that are directly linked from primary namespace pages.

5. **DON'T forget about `File:` wrapper links.** Pattern `[img](https://openwetware.org/wiki/File:Name.jpg)` is NOT a direct image URL — it's a wiki page that wraps the full-size image. Must resolve via API.

6. **DON'T leave CDN thumbnail URLs.** `oww-files-thumb.sfo3.cdn.digitaloceanspaces.com` serves low-res thumbnails. Always convert to full-size from `oww-files-public`.

7. **DON'T skip the "Retrieved from" footer check.** New pages downloaded in later rounds will have these footers. They reference `openwetware.org` and will fail the audit.

8. **DON'T batch-process quoting-sensitive strings through the shell.** Even `echo` or `sed` can corrupt URLs with `&`, `=`, `(`, `)`. Python's string handling is safer.

9. **DON'T forget angle-bracket URLs.** Some wiki pages contain `<http://openwetware.org/wiki/CAMRI:Flywheel>` — bare URLs in angle brackets. These need a separate regex pass, not just the `[text](url)` pattern.

10. **DON'T assume wiki page names are case-sensitive if resolution fails.** Try exact match, then underscored, then case-insensitive, then index page fallback.

---

## OpenWetWare-Specific Reference

### URL Patterns

| Pattern | Example | Meaning |
|---------|---------|---------|
| `/wiki/Namespace:Page` | `/wiki/Beauchamp:Publications` | Wiki page |
| `/wiki/File:Name.ext` | `/wiki/File:RAVE_Logo.jpg` | File description page (NOT the file itself) |
| `/wiki/User:Name` | `/wiki/User:John_Doe` | User profile (skip) |
| `?action=edit&redlink=1` | `?title=Beauchamp:Foo&action=edit&redlink=1` | Non-existent page |

### CDN URL Patterns

| Host | Purpose | Example |
|------|---------|---------|
| `oww-files-public.sfo3.cdn.digitaloceanspaces.com` | Full-size files | `https://oww-files-public.sfo3.cdn.../a/ab/Paper.pdf` |
| `oww-files-thumb.sfo3.cdn.digitaloceanspaces.com` | Thumbnails | `https://oww-files-thumb.sfo3.cdn.../a/ab/Image.jpg/250px-Image.jpg` |

### Thumbnail → Full-Size Conversion

```
Thumbnail: https://oww-files-thumb.sfo3.cdn.../a/ab/Image.jpg/250px-Image.jpg
                   ^^^^^^^^^^^^^^                              ^^^^^^^^^^^^^^^^
                   replace with                                drop this segment
                   oww-files-public

Full-size: https://oww-files-public.sfo3.cdn.../a/ab/Image.jpg
```

### MediaWiki API for File Resolution

```
GET {WIKI_BASE}/mediawiki/api.php?action=query&titles=File:{name}&prop=imageinfo&iiprop=url&format=json
```

Response:
```json
{
  "query": {
    "pages": {
      "12345": {
        "imageinfo": [{
          "url": "https://oww-files-public.sfo3.cdn.../a/ab/Image.jpg"
        }]
      }
    }
  }
}
```

### Content Extraction

Target: `<div id="mw-content-text">...</div>`

Remove before conversion:
- `<span class="mw-editsection">` — "[edit]" links
- `<div class="catlinks">` — category links
- `<div id="toc">` — table of contents
- `Retrieved from "..."` — page footer

### Broken Link Markers

In converted Markdown, broken links use these conventions:

```markdown
[Link text](# "WikiName - not archived")           <!-- Page doesn't exist locally -->
[Link text](# "File:name.jpg - not available")     <!-- File couldn't be downloaded -->
~~Page Name~~ *(page not archived)*                 <!-- Page returned 404 -->
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `audit` keeps finding references | Run `fix` again — each pass catches ~60-80% |
| Title attributes break regex | Use `r'(\S+?)(\s+"[^"]*")?$'` to split URL from title |
| Inline Python in shell fails | Write a `.py` file instead — never use `python -c "..."` with URLs |
| Images missing after migration | Check for `oww-files-thumb` URLs — convert to `oww-files-public` |
| `/wiki/File:` links still external | Use MediaWiki API to resolve, not direct URL construction |
| `(archived) (archived)` duplication | Fix script ran twice — the `fix` command handles this pattern |
| Nested `[![img](src)](href)` broken | Both inner `src` and outer `href` need separate resolution |
