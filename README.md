# Beauchamp Lab Wiki

This repository contains the Beauchamp Lab wiki, migrated from OpenWetWare.

## Viewing the Wiki as a Website

This wiki is published via GitHub Pages at:
**https://beauchamplab.github.io/LabWiki/**

### How to Enable GitHub Pages (for repository admins)

1. Go to repository **Settings** → **Pages**
2. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
3. Click **Save**
4. Wait 1-2 minutes for GitHub to build the site
5. Visit `https://beauchamplab.github.io/LabWiki/`

The site will automatically rebuild whenever you push changes to the main branch.

## Repository Structure

```
├── pages/                    # Markdown wiki pages
│   ├── Beauchamp/           # Main Beauchamp Lab wiki (141 pages)
│   ├── RAVE/                # RAVE documentation (25 pages)
│   ├── CAMRI/               # CAMRI resources (12 pages)
│   ├── YAEL/                # YAEL documentation (7 pages)
│   └── Karas_Lab/           # Karas Lab wiki (7 pages)
├── attachments/             # Media files, PDFs, data
│   ├── Publications/        # Lab publications (PDFs)
│   └── [section]/           # Files organized by section
├── _config.yml              # Jekyll configuration
└── index.md                 # Home page
```

## Files and Git LFS

This repository uses Git LFS (Large File Storage) for non-image files:
- **LFS tracked**: PDFs, audio, video, zip, docx, etc. (~1.0GB)
- **Regular Git**: Images (png, jpg, jpeg, webp), Publications folder, markdown (~282MB)

## Migration Details

- **Source**: OpenWetWare (openwetware.org/wiki/Beauchamp)
- **Pages migrated**: 199
- **Attachments**: 549 files
- **Status**: Complete - zero OpenWetWare references remaining

## Local Development

To preview the site locally:

```bash
# Install Jekyll
gem install bundler jekyll

# Create Gemfile (if needed)
bundle init
bundle add jekyll

# Serve locally
bundle exec jekyll serve

# View at http://localhost:4000/LabWiki/
```

## Contributing

This wiki is primarily for Beauchamp Lab members. For the official lab website, visit:
[beauchamplab.med.upenn.edu](https://beauchamplab.med.upenn.edu/)
