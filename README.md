# Ground Truth

Quarto-first blog workspace optimized for local development and Medium publishing. Each post is a self-contained directory under `posts/` with its own `index.qmd`.

## Key pieces

- `posts/` — Self-contained post bundles (e.g., `2025-11-06-landsat-composites/`), each with:
  - `index.qmd` — Source post
  - `index.md` — Rendered GitHub Flavored Markdown
  - `medium-import.html` — Self-contained HTML for Medium import
  - `index_files/` — Generated assets (images, plots)
- `_quarto.yml` — Quarto website config, ready for future self-hosted site
- `requirements.txt` — Python deps including Earth Engine, geemap, Altair
- `scripts/publish_to_medium.py` — Legacy script for Medium's deprecated API (kept for reference)

## Local development

### Setup

1. Install Quarto (CLI) from https://quarto.org

2. Create a Python env and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Authenticate with Earth Engine (first time only):

```bash
python -c "import ee; ee.Authenticate()"
```

### Working on a post

1. Create or edit a post in `posts/<slug>/index.qmd`

2. Render the post to Markdown:

```bash
quarto render posts/<slug>/index.qmd --to gfm
```

3. Render a self-contained HTML for Medium import:

```bash
cd posts/<slug>
quarto render index.qmd --to html -M self-contained:true --output medium-import.html
```

4. Preview the rendered Markdown locally:

```bash
quarto preview posts/<slug>/index.qmd
```

Or preview the entire site:

```bash
quarto preview
```

### Publishing to Medium

After rendering locally:

1. Navigate to https://medium.com/p/import
2. Upload `posts/<slug>/medium-import.html`
3. Review and publish

### Committing changes

Commit both source and rendered outputs:

```bash
git add posts/<slug>/
git commit -m "Add/update post: <title>"
git push
```

Rendered outputs (`*.md`, `medium-import.html`, `index_files/`) are tracked so they're always available from GitHub.

## Future: Self-hosted site

To publish the full Quarto site to GitHub Pages:

```bash
quarto render
# Then commit _site/ or deploy via GitHub Pages workflow
```

## Notes

- Keep posts self-contained: place CSVs, static images, etc. alongside `index.qmd`
- `_site/` and `_freeze/` are ignored (build caches)
- All rendered post assets are versioned in Git for easy access and Medium import


