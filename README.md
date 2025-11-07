# Ground Truth

Quarto-first blog workspace with an automated pipeline to produce import-ready HTML for Medium. Each post is a self-contained directory under `posts/` with its own `index.qmd`.

## Key pieces

- `.github/workflows/publish.yml` — CI that renders changed posts and uploads a self-contained HTML artifact for easy import into Medium (no API token required).
- `scripts/publish_to_medium.py` — Legacy script for Medium’s deprecated API (kept for historical reference; not used by CI).
- `posts/` — Self-contained post bundles (e.g., `2025-11-06-landsat-composites/`).
- `_quarto.yml` — Quarto website config, ready for future self-hosted site.
- `requirements.txt` — Python deps for local dev and CI, including Earth Engine, geemap, Altair.

## Local development

1) Install Quarto (CLI) from https://quarto.org.

2) Create a Python env and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Render site locally:

```bash
quarto render
```

## Medium publishing (Import flow)

No tokens required. On push to `posts/**/*.qmd` or via the manual “Run workflow” button:

- CI detects changed post(s)
- Renders a self-contained HTML file for each post: `posts/<slug>/medium-import.html`
- Renders GitHub Flavored Markdown alongside it: `posts/<slug>/index.md`
- Uploads two artifacts:
  - `medium-import-html-<sha>` with the HTML files
  - `medium-markdown-<sha>` with the Markdown files

To publish on Medium:

1. Open the Actions run for your commit.
2. Download the `medium-import-html-<sha>` artifact (recommended) or `medium-markdown-<sha>` for editing.
3. Go to https://medium.com/p/import and upload `medium-import.html`, or paste the Markdown into Medium’s editor.

Optional: If you later obtain a legacy Medium token, you can re-enable API-based publishing by adding the relevant steps back to the workflow.

## Earth Engine in CI

Posts can auto-auth using a service account if the two EE secrets are provided. Locally, the code falls back to `ee.Authenticate()` on first run, then caches credentials.

## Notes

- `posts/**/index_files/` and build caches are ignored via `.gitignore`. For Medium import, CI produces a self-contained HTML file that embeds assets.
- Keep posts self-contained. Place any small CSVs or static images alongside `index.qmd` in the same directory.

