# frozen_string_literal: true

# _plugins/resolve_obsidian_links.rb
#
# Rewrites Obsidian vault-root-relative markdown links at Jekyll build time.
#
# When Obsidian moves a file it rewrites internal links relative to the vault
# root, e.g. [text](pages/Beauchamp/Lab_Info/Lab_Members.md).  Jekyll normally
# treats such a path as relative to the containing page's directory, which causes
# broken links on nested pages located more than one level deep.
#
# Resolution rule applied to every internal markdown link before rendering:
#   1. If the link already resolves from the current page's directory → keep it.
#   2. Else if the link resolves from the Jekyll source root → rewrite it to the
#      correct relative path from the current page's directory.
#   3. Otherwise keep unchanged and emit a WARNING so broken links are surfaced.
#
# Skips: external links (http://, https://, mailto:, etc.), absolute paths (/…),
#        anchor-only links (#…), angle-bracket < > URLs.
#
# Works together with jekyll-relative-links: this plugin corrects the paths in
# the markdown source first; jekyll-relative-links then converts .md extensions
# to final HTML URLs.

require 'pathname'

module ObsidianLinkResolver
  # Matches markdown links: [text](url) or [text](url "title") or ![alt](url).
  #
  # The URL group allows one level of balanced parentheses so that filenames like
  # Reconstruction_and_Electrode_Labeling_(UPenn).md are captured whole.
  #
  # Group 1: prefix  — everything up to and including the opening paren "[text]("
  # Group 2: url     — the URL, possibly with a #fragment, no surrounding spaces
  # Group 3: title   — optional title attribute including leading whitespace
  # Group 4: suffix  — the closing paren ")"
  LINK_PATTERN = /
    (!?\[[^\]]*\]\()              # [$1] "[text](" or "![alt]("
    ((?:[^()\s]|\([^()]*\))+)    # [$2] URL: no spaces, one level of (balanced)
    ((?:\s+"[^"]*"|\s+'[^']*')?) # [$3] optional title attribute with leading space
    (\))                          # [$4] closing paren
  /x

  # Returns true for URLs that should be left completely untouched.
  def self.skip_url?(url)
    return true if url.nil? || url.empty?
    return true if url.start_with?('#')   # anchor-only
    return true if url.start_with?('/')   # absolute path
    return true if url.start_with?('<')   # angle-bracket URL
    return true if url =~ /\A[a-zA-Z][a-zA-Z0-9+\-.]*:/  # scheme (http, mailto…)
    false
  end

  # Rewrites all markdown links in +content+ that are root-relative (Obsidian
  # style) so they become correct relative paths from +doc_abs_dir+.
  #
  # @param content      [String]  raw markdown content of the document
  # @param doc_abs_dir  [String]  absolute path to the directory containing the doc
  # @param site_source  [String]  absolute path to the Jekyll site source root
  # @return [String] content with links rewritten where necessary
  def self.rewrite_content(content, doc_abs_dir, site_source)
    content.gsub(LINK_PATTERN) do
      prefix   = $1  # "[text](" or "![alt]("
      url_full = $2  # raw URL token (may include #fragment)
      title    = $3  # optional: ' "Title text"' (with leading whitespace)
      suffix   = $4  # ")"

      # Separate #fragment from the file path
      url, fragment = url_full.split('#', 2)
      fragment_str  = fragment ? "##{fragment}" : ''

      if skip_url?(url)
        next "#{prefix}#{url_full}#{title}#{suffix}"
      end

      # ------------------------------------------------------------------
      # Step 1: already a valid relative path from this page's directory?
      # ------------------------------------------------------------------
      candidate_in_dir = File.expand_path(url, doc_abs_dir)
      if File.exist?(candidate_in_dir)
        # Also convert .md → .html so links with title attributes resolve
        # correctly (jekyll-relative-links skips links that have title attrs).
        final_url = url.sub(/\.md$/, '.html') + fragment_str
        next "#{prefix}#{final_url}#{title}#{suffix}"
      end

      # ------------------------------------------------------------------
      # Step 2: resolves from the repo root (Obsidian vault-root style)?
      # ------------------------------------------------------------------
      candidate_from_root = File.join(site_source, url)
      if File.exist?(candidate_from_root)
        rel = Pathname.new(candidate_from_root)
                      .relative_path_from(Pathname.new(doc_abs_dir))
                      .to_s
        rewritten_url = "#{rel.sub(/\.md$/, '.html')}#{fragment_str}"
        rel_doc = doc_abs_dir.sub("#{site_source}/", '')
        Jekyll.logger.debug('ObsidianLinks:', "#{rel_doc}: '#{url}' → '#{rel}'")
        next "#{prefix}#{rewritten_url}#{title}#{suffix}"
      end

      # ------------------------------------------------------------------
      # Step 3: unresolved — keep unchanged, emit warning for visibility
      # ------------------------------------------------------------------
      rel_doc = doc_abs_dir.sub("#{site_source}/", '')
      Jekyll.logger.warn('ObsidianLinks:', "Unresolved link '#{url}' in: #{rel_doc}/")
      "#{prefix}#{url_full}#{title}#{suffix}"
    end
  end
end

# Register on both :pages (regular .md files) and :documents (collection items).
# The check for .md extension prevents processing of static files like CSS/JS.
[:pages, :documents].each do |hook_type|
  Jekyll::Hooks.register hook_type, :pre_render do |doc|
    next unless doc.relative_path.end_with?('.md')

    site_source = doc.site.source
    doc_abs_dir = File.dirname(File.join(site_source, doc.relative_path))

    doc.content = ObsidianLinkResolver.rewrite_content(
      doc.content, doc_abs_dir, site_source
    )
  end
end
