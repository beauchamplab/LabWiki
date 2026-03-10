
#!/bin/bash
set -e

## Prepare
cd "$(dirname "$0")"

## Bootstrap: ensure Homebrew, Ruby, Bundler, and gems are installed

# Ensure Homebrew is in PATH (common install locations)
if ! command -v brew &>/dev/null; then
  for brewdir in /opt/homebrew/bin /usr/local/bin; do
    if [[ -x "$brewdir/brew" ]]; then
      eval "$("$brewdir/brew" shellenv)"
      break
    fi
  done
fi

if ! command -v brew &>/dev/null; then
  echo "Error: Homebrew not found. Install it from https://brew.sh" >&2
  exit 1
fi

# Detect missing components and show one-time setup notice
MISSING=()
if [[ ! -d "$(brew --prefix)/opt/ruby/bin" ]] && ! command -v ruby &>/dev/null; then
  MISSING+=("Ruby")
fi
if ! command -v bundle &>/dev/null; then
  MISSING+=("Bundler")
fi
if [[ ! -f Gemfile.lock ]] || [[ Gemfile -nt Gemfile.lock ]]; then
  MISSING+=("gems")
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo ""
  echo "=============================================="
  echo "  First-time setup detected — don't panic!"
  echo "  Missing: ${MISSING[*]}"
  echo "  This is a one-time install and may take"
  echo "  a minute or two. Subsequent runs will be fast."
  echo "=============================================="
  echo ""
fi

# Use Homebrew Ruby if available
if [[ -d "$(brew --prefix)/opt/ruby/bin" ]]; then
  export PATH="$(brew --prefix)/opt/ruby/bin:$PATH"
  export PATH="$(gem environment gemdir)/bin:$PATH"
fi

# Install Ruby via Homebrew if missing
if ! command -v ruby &>/dev/null; then
  echo "Ruby not found. Installing via Homebrew..."
  brew install ruby
  export PATH="$(brew --prefix)/opt/ruby/bin:$PATH"
  export PATH="$(gem environment gemdir)/bin:$PATH"
fi

# Install Bundler if missing
if ! command -v bundle &>/dev/null; then
  echo "Bundler not found. Installing..."
  gem install bundler
fi

# Install gems if Gemfile.lock is missing or Gemfile is newer
if [[ ! -f Gemfile.lock ]] || [[ Gemfile -nt Gemfile.lock ]]; then
  echo "Running bundle install..."
  bundle install
fi

## Compile and serve
PORT=4000
echo "Serving at http://127.0.0.1:$PORT/LabWiki/ ..."
(sleep 8 && open "http://127.0.0.1:$PORT/LabWiki/") &
bundle exec jekyll serve --port "$PORT" --incremental
