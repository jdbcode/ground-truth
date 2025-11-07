# Ground Truth

Quarto-first blog workspace optimized for local development, GitHub Pages hosting (`docs/`), and Medium publishing (Markdown-only flow). Each post is a self-contained directory under `posts/` with its own `index.qmd`.

## Key pieces

- `posts/` — Self-contained post bundles (e.g., `2025-11-06-landsat-composites/`), each with:
  - `index.qmd` — Source post
  - `index.md` — Rendered GitHub Flavored Markdown
  - `index_files/` — Generated assets (images, plots)
- `_quarto.yml` — Quarto website config (output to `docs/` for GitHub Pages)
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

2. From the post folder, render Markdown next to the source (avoids writing to `_site/`):

```bash
cd posts/<slug>

# Render Markdown next to index.qmd
quarto render index.qmd --to gfm --output index.md --output-dir .
```

3. Preview locally (served preview lives under a temp server, final site build goes to `docs/`):

```bash
quarto preview index.qmd
```

Or preview the entire site:

```bash
quarto preview
```

### Publishing to Medium (Markdown flow)

After rendering locally, convert image paths to absolute raw GitHub URLs and copy/paste to Medium:

```bash
# Make sure images are committed and pushed so raw URLs resolve on Medium
git add posts/<slug>/index_files/
git commit -m "Post assets"
git push

# Generate Medium-ready Markdown with absolute image URLs
python scripts/prepare_medium_markdown.py \
  --md posts/<slug>/index.md \
  --repo jdbcode/ground-truth \
  --branch main \
  --out posts/<slug>/medium.md

# Open posts/<slug>/medium.md and copy/paste into Medium's editor
```

### Committing changes

Commit both source and rendered outputs:

```bash
git add posts/<slug>/
git commit -m "Add/update post: <title>"
git push
```

Rendered outputs (`*.md`, `index_files/`) are tracked so they're always available from GitHub.

## GitHub Pages deployment (docs/)

The site output directory is `docs/`. To (re)build and publish:

```bash
quarto render
git add docs/
git commit -m "Site build"
git push
```

Then enable GitHub Pages: Repository Settings → Pages → Build and deployment → Deploy from branch → Branch: `main`, Folder: `/docs`.

After activation, each post will have a URL like:

```
https://<username>.github.io/ground-truth/posts/<slug>/index.html
```

You can use that URL with Medium’s Import tool (https://medium.com/p/import) instead of generating separate HTML.

## Notes

- Keep posts self-contained: place CSVs, static images, etc. alongside `index.qmd`
- `_freeze/` is ignored (execution cache); `docs/` is committed for Pages
- All rendered post assets (Markdown + index_files) are versioned in Git for easy access and Medium publishing


