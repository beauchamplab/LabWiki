# Wiki Maintenance Scripts

This directory contains helper scripts for maintaining the Beauchamp Lab Wiki. These scripts are excluded from the Jekyll build.

## Available Scripts

### `check_links.py` - Link Checker

Scans all markdown files in the wiki to detect broken internal links and attachment references.

**Features:**
- Detects broken links to other wiki pages
- Validates attachment references (images, PDFs, etc.)
- Compares findings with `pages/BROKEN_LINKS.md` to find new issues
- Suggests similar filenames for common typos
- Generates detailed reports

**Usage:**

```bash
# Basic check
python3 scripts/check_links.py

# Verbose output (show every file checked)
python3 scripts/check_links.py --verbose

# Generate a detailed report file
python3 scripts/check_links.py --report scripts/link_report.md

# Combined
python3 scripts/check_links.py -v -r scripts/link_report.md
```

**Exit Codes:**
- `0` - No broken links found
- `1` - Broken links detected

**Workflow:**

1. **Run the link checker** to identify broken links:
   ```bash
   python3 scripts/check_links.py
   ```

2. **Review the output** to understand the broken link patterns.

3. **Use AI (GitHub Copilot) to fix links manually:**
   - Links require namespace-aware context (same folder vs. cross-namespace references)
   - AI understands file organization and wiki structure better than regex patterns
   - Prevents false fixes that break valid links
   - Ask Copilot: "Fix the broken links found by check_links.py"

4. **Verify fixes** by running the checker again:
   ```bash
   python3 scripts/check_links.py
   ```

**Why not use automated fixing?**

Links in the wiki are delicate and require context:
- Namespace-relative paths: `../RAVE/Install.md` vs `Install.md`
- Special characters in filenames (parentheses, underscores)
- Template files that need different paths per namespace
- Title attributes that look like broken URLs to simple regex

AI can understand these nuances; regex scripts cannot.

---

## Adding New Scripts

When adding new maintenance scripts:

1. Place them in this `scripts/` directory
2. Add documentation to this README
3. Make scripts executable: `chmod +x scripts/your_script.py`
4. Add a shebang line: `#!/usr/bin/env python3`
5. Include usage documentation in the script's docstring

## Python Dependencies

Most scripts use only Python standard library. If additional dependencies are needed, document them here.

Current requirements:
- Python 3.7+
- No external packages required for `check_links.py`

---

## Related Files

- `pages/BROKEN_LINKS.md` - Known broken links from migration
- `pages/TODO.md` - Migration tracking and TODO items
- `_config.yml` - Excludes this `scripts/` directory from Jekyll build
