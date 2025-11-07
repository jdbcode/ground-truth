"""Publish rendered Quarto Markdown to Medium as a draft.

- Reads a rendered markdown file (GFM) produced by `quarto render ... --to gfm`.
- Rewrites local image refs to raw GitHub URLs so Medium can fetch them.
- Extracts title (and optional tags) from YAML front matter if present.

Environment variables:
- MEDIUM_TOKEN or MEDIUM_INTEGRATION_TOKEN: API token for Medium
- GITHUB_REPOSITORY: e.g., "owner/repo"
- GITHUB_REF_NAME: branch name (defaults to "main" if unset)

Usage:
  python scripts/publish_to_medium.py --md posts/2025-11-06-landsat-composites/index.md
"""
from __future__ import annotations

import argparse
import os
import re
import json
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

import requests


def get_medium_token() -> str:
    token = os.getenv("MEDIUM_TOKEN") or os.getenv("MEDIUM_INTEGRATION_TOKEN")
    if not token:
        raise RuntimeError("Missing MEDIUM_TOKEN (or MEDIUM_INTEGRATION_TOKEN) env var")
    return token


def get_user_id(token: str) -> str:
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8'
    }
    resp = requests.get("https://api.medium.com/v1/me", headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()['data']['id']


def parse_front_matter(md_text: str) -> Tuple[Dict[str, Any], str]:
    """Extract simple YAML front matter and return (meta, body).
    Supports lines like `title: ...`, `tags: [a, b]`.
    """
    fm_regex = r"^---\n(.*?)\n---\n(.*)$"  # non-greedy front matter
    m = re.match(fm_regex, md_text, re.DOTALL)
    if not m:
        return {}, md_text

    raw_yaml, body = m.group(1), m.group(2)
    meta: Dict[str, Any] = {}
    # naive parse to avoid adding a dependency on PyYAML
    for line in raw_yaml.splitlines():
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip().strip('"')
        if key == 'tags':
            # basic [a, b] or comma-separated support
            if val.startswith('[') and val.endswith(']'):
                inside = val[1:-1].strip()
                tags = [t.strip().strip('"\'') for t in inside.split(',') if t.strip()]
            else:
                tags = [v.strip() for v in val.split(',') if v.strip()]
            meta[key] = tags
        else:
            meta[key] = val
    return meta, body


def make_raw_url(repo: str, branch: str, repo_relative_path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{repo_relative_path}"


def replace_images_with_raw_urls(md_path: Path, md_body: str, repo: str, branch: str) -> str:
    base_dir = md_path.parent
    repo_root = Path(__file__).resolve().parents[1]

    def repl(match: re.Match) -> str:
        alt_text = match.group(1)
        local_path = match.group(2)
        # Skip if already URL
        if re.match(r"^https?://", local_path):
            return match.group(0)
        # Resolve to repo-relative path
        abs_path = (base_dir / local_path).resolve()
        try:
            rel = abs_path.relative_to(repo_root)
        except ValueError:
            # If not under repo, leave unchanged
            return match.group(0)
        raw_url = make_raw_url(repo, branch, str(rel).replace('\\', '/'))
        return f"![{alt_text}]({raw_url})"

    # Markdown image: ![alt](path)
    return re.sub(r"!\[(.*?)\]\((.*?)\)", repl, md_body)


def publish_markdown(md_path: Path) -> Dict[str, Any]:
    token = get_medium_token()
    repo = os.getenv('GITHUB_REPOSITORY', '')
    branch = os.getenv('GITHUB_REF_NAME', 'main')

    md_text = md_path.read_text(encoding='utf-8')
    meta, body = parse_front_matter(md_text)
    title = meta.get('title') or md_path.stem
    tags = meta.get('tags') or ['Earth Engine', 'Python']

    body = replace_images_with_raw_urls(md_path, body, repo=repo, branch=branch)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8'
    }

    user_id = get_user_id(token)
    url = f"https://api.medium.com/v1/users/{user_id}/posts"
    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": body,
        "tags": tags,
        "publishStatus": "draft"
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--md', required=True, help='Path to rendered markdown file (GFM)')
    args = ap.parse_args()

    md_path = Path(args.md).resolve()
    if not md_path.exists():
        raise SystemExit(f"Markdown file not found: {md_path}")

    result = publish_markdown(md_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
