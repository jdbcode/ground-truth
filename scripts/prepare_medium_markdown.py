"""Prepare Markdown for Medium by rewriting local image paths to raw GitHub URLs.

Usage:
  python scripts/prepare_medium_markdown.py --md posts/<slug>/index.md --repo <owner/repo> [--branch main] [--out posts/<slug>/medium.md]

Notes:
- Ensure you've committed and pushed the images (index_files/) to the repo so the raw URLs resolve on Medium.
- This script does not publish to Medium; copy/paste the resulting Markdown into Medium's editor.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional


def make_raw_url(repo: str, branch: str, repo_relative_path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{repo_relative_path}"


def replace_images_with_raw_urls(md_path: Path, md_text: str, repo: str, branch: str) -> str:
    base_dir = md_path.parent
    # Assume repo root is repo top-level containing this scripts/ directory
    # scripts/ lives under <repo_root>/scripts/
    # Resolve repo_root relative to script file location for robustness
    scripts_dir = Path(__file__).resolve().parent
    repo_root = scripts_dir.parent

    def repl(match: re.Match) -> str:
        alt_text = match.group(1)
        local_path = match.group(2)
        # Leave http(s) URLs untouched
        if re.match(r"^https?://", local_path):
            return match.group(0)
        # Resolve local path relative to the Markdown file
        abs_path = (base_dir / local_path).resolve()
        try:
            rel = abs_path.relative_to(repo_root)
        except ValueError:
            # If outside repo, leave unchanged
            return match.group(0)
        raw_url = make_raw_url(repo, branch, str(rel).replace("\\", "/"))
        return f"![{alt_text}]({raw_url})"

    # Markdown image pattern: ![alt](path)
    return re.sub(r"!\[(.*?)\]\((.*?)\)", repl, md_text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True, help="Path to the rendered Markdown (GFM) file")
    ap.add_argument("--repo", required=True, help="GitHub <owner>/<repo> (e.g., jdbcode/ground-truth)")
    ap.add_argument("--branch", default="main", help="Branch name (default: main)")
    ap.add_argument("--out", default=None, help="Output path for modified Markdown (default: <md_dir>/medium.md)")
    args = ap.parse_args()

    md_path = Path(args.md).resolve()
    if not md_path.exists():
        raise SystemExit(f"Markdown file not found: {md_path}")

    md_text = md_path.read_text(encoding="utf-8")
    updated = replace_images_with_raw_urls(md_path, md_text, repo=args.repo, branch=args.branch)

    out_path: Path
    if args.out:
        out_path = Path(args.out).resolve()
    else:
        out_path = md_path.with_name("medium.md")

    out_path.write_text(updated, encoding="utf-8")
    print(f"Wrote Medium-ready Markdown to: {out_path}")


if __name__ == "__main__":
    main()
