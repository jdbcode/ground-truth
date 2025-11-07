# Ground Truth

Quarto-first blog workspace with an automated pipeline to post rendered Markdown to Medium. Each post is a self-contained directory under `posts/` with its own `index.qmd` and generated `index_files/` assets.

## Key pieces

- `.github/workflows/publish.yml` — CI that renders changed posts to GitHub Flavored Markdown (GFM) and publishes drafts to Medium.
- `scripts/publish_to_medium.py` — Converts rendered Markdown to a Medium draft, rewriting image paths to raw GitHub URLs.
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

## Medium publishing (CI)

Set repository secrets:

- `MEDIUM_TOKEN` (or `MEDIUM_INTEGRATION_TOKEN`) — Medium API token
- Optional Earth Engine service account (for non-interactive CI renders):
	- `EE_SERVICE_ACCOUNT` — service account email
	- `EE_PRIVATE_KEY_JSON` — JSON key contents (paste full JSON)

Workflow behavior on push to `posts/**/*.qmd`:

- Detect changed post(s)
- `quarto render ... --to gfm` to produce `index.md` + `index_files/`
- Commit the assets back to the branch
- Publish a draft to Medium using the rendered markdown

## Earth Engine in CI

Posts can auto-auth using a service account if the two EE secrets are provided. Locally, the code falls back to `ee.Authenticate()` on first run, then caches credentials.

## Notes

- `posts/**/index_files/` and build caches are ignored via `.gitignore`. The workflow commits rendered assets explicitly so Medium can fetch images via raw GitHub URLs.
- Keep posts self-contained. Place any small CSVs or static images alongside `index.qmd` in the same directory.

