# Copilot Instructions — Beauchamp Lab Wiki Migration

## Project Status
**MIGRATION COMPLETE.** 199 pages converted, 549 attachments downloaded, zero openwetware references remaining.

## Project Goal
Migrate the Beauchamp Lab wiki from <https://openwetware.org/wiki/Beauchamp> to local Markdown files. The primary scope is all pages under the `:Beauchamp` namespace. Other wikis (RAVE, YAEL, CAMRI, Karas_Lab) are included **only if directly linked from Beauchamp pages** (one hop, not recursive).

**Core requirement:** If openwetware.org and its Amazon S3 CDN shut down (including images), all wiki content must be readable offline without any issues.

## Wiki Naming & Scope

### Namespace Convention
OpenWetWare uses `Namespace:PageName` URL patterns:
- `openwetware.org/wiki/Beauchamp:Publications` → Beauchamp namespace
- `openwetware.org/wiki/RAVE:Install` → RAVE namespace (separate wiki)
- `openwetware.org/wiki/CAMRI:HowToScan` → CAMRI namespace
- `openwetware.org/wiki/YAEL:Install` → YAEL namespace
- `openwetware.org/wiki/Karas_Lab:Lab_Notebook` → Karas_Lab namespace

### Download Scope Rules
1. **Primary:** ALL `Beauchamp:*` pages → `pages/Beauchamp/*.md`
2. **One-hop:** Non-Beauchamp pages linked FROM Beauchamp → `pages/RAVE/*.md`, `pages/CAMRI/*.md`, etc.
3. **Do NOT** recursively crawl non-Beauchamp wikis (they have their own independent structure)
4. Pages without a namespace prefix go to `pages/*.md`

## File Structure
- `pages/Beauchamp/*.md` — 141 core Beauchamp wiki pages
- `pages/RAVE/*.md` — 25 RAVE pages (linked from Beauchamp)
- `pages/CAMRI/*.md` — 12 CAMRI pages (linked from Beauchamp)
- `pages/YAEL/*.md` — 7 YAEL pages (linked from Beauchamp)
- `pages/Karas_Lab/*.md` — 7 Karas_Lab pages (linked from Beauchamp)
- `pages/*.md` — 6 root-level pages (no namespace)
- `attachments/<Section>/` — 549 media files organized by section

## Key Rules

### Page Conversion
1. Fetch each wiki page, extract `#mw-content-text` div (ignore navigation chrome, sidebar, "Additional Links", footer, "Retrieved from" lines).
2. Convert to clean Markdown with `markdownify` (ATX headings, strip divs).
3. Add a navigation header: `> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)`
4. Rewrite internal wiki links to relative `.md` paths using namespace-aware resolution.
5. Keep external links (journals, DOIs, GitHub, Dropbox, etc.) as-is.
6. Mark red links (non-existent pages) with strikethrough: `~~Page Name~~ *(page not archived)*`
7. Remove `[edit]` section links and MediaWiki editing chrome.

### Link Resolution (critical lessons)
1. **Wiki links appear in multiple formats:**
   - `/wiki/Beauchamp:Foo` — relative wiki path
   - `https://openwetware.org/wiki/Beauchamp:Foo` — full URL (with http/https/www variants)
   - `[text](url "title")` — markdown links may include title attributes
   - `[![img](src)](href)` — nested image-link patterns (image inside clickable link)
   - `<url>` — angle-bracket URLs in text
   - Bare URLs in text without any markdown formatting

2. **File: wrapper links:** Pattern `[img](https://openwetware.org/wiki/File:Name.jpg)` wraps images that are already downloaded. Resolve via MediaWiki API: `{WIKI_BASE}/mediawiki/api.php?action=query&titles=File:{name}&prop=imageinfo&iiprop=url&format=json`

3. **CDN hosts:**
   - Full images: `oww-files-public.sfo3.cdn.digitaloceanspaces.com`
   - Thumbnails: `oww-files-thumb.sfo3.cdn.digitaloceanspaces.com`
   - Thumbnail → full-size: replace `oww-files-thumb` with `oww-files-public`, drop last path segment

4. **Title attributes in links** like `[text](url "Beauchamp:PageName")` must be handled — naïve regex `[^)]+` greedily captures the title as part of the URL.

5. **Multi-pass fixing is necessary.** A single regex pass misses edge cases. Run audit after each fix pass and iterate until zero references remain.

### Media / Attachments
1. **Download** any file hosted on CDN (`oww-files-public` or `oww-files-thumb`).
2. Target media types: `.pdf`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.wav`, `.mp3`, `.mp4`, `.zip`, `.csv`, `.docx`, `.mat`, `.ppt`.
3. Save to `attachments/<Section>/` where Section = page name (e.g., `attachments/Publications/`, `attachments/RAVE_OldHome/`).
4. **Rewrite** CDN URLs to relative local paths (`../../attachments/Section/filename.ext`).
5. URL-decode filenames (`%2C` → `,`, `%28` → `(`, etc.) when saving locally.
6. Replace spaces with underscores in filenames.

### Batch Processing
- **Always use Python script files** for batch operations — never inline Python in zsh (quoting issues with URLs, special chars, nested quotes).
- Use `concurrent.futures.ThreadPoolExecutor` with 8 workers for parallel downloads.
- Verify downloads: check for empty files and report counts/sizes.
- Track progress with print statements showing file counts and outcomes.

### Link Maintenance
- **Use `scripts/check_links.py`** to detect broken links across all pages.
- **Fix links manually with AI assistance** rather than automated scripts — links require namespace-aware context that regex cannot handle.
- **Common link issues:**
  - Cross-namespace references: `../RAVE/Page.md` vs `Page.md` (same folder)
  - Files with parentheses in names: `File_(Note).md` confuses simple regex
  - RAVE namespace uses colon in filenames: `RAVE:Module_Builder.md`
  - Template files need different relative paths depending on location
- **Verification workflow:** Run `check_links.py` → ask AI to fix → run checker again to verify

### TODO.md Maintenance
- Track all pages with `- [x]` checkboxes.
- Maintain summary table at the bottom.
- Keep `BROKEN_LINKS.md` for pages/files that couldn't be resolved.

## Lessons Learned

1. **Scope creep prevention:** Define scope clearly — Beauchamp is the primary wiki; other namespaces are secondary (one-hop only). Don't recursively crawl non-Beauchamp wikis.

2. **Regex for markdown links is hard:** Simple `\[text\]\(url\)` regex fails for:
   - Title attributes: `[text](url "title")`
   - Escaped quotes in titles: `"\"quoted\""`
   - Nested links: `[![img](src)](href)` — the inner match consumes characters
   - Angle-bracket URLs: `<url>`

3. **MediaWiki "Retrieved from" footers** are boilerplate that should be stripped during conversion.

4. **CDN thumbnail trick:** Replace `oww-files-thumb` with `oww-files-public` and drop the last path segment (e.g., `/250px-image.jpg`) to get the full-size image URL.

5. **Multiple fix passes required:** Each pass reveals new edge cases. Always audit after fixing with `grep -rn 'openwetware.org' pages/` and iterate.

6. **Anchor markers for broken links:** Use `](# "WikiName - not archived")` as a placeholder that can be re-resolved later when pages become available.

7. **`/wiki/File:` links** are click-to-view-full-size wrappers around thumbnails. They should point to the same local file as the embedded image.

8. **Python virtual environment:** `.venv/` with `requests`, `beautifulsoup4`, `markdownify` installed.
