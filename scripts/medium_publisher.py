"""Simple Medium publisher skeleton.

This script is a starter: it looks for MEDIUM_INTEGRATION_TOKEN in the env and will
print what it would publish. Extend with the official Medium API or a library.
"""
import os
import json
from pathlib import Path

MEDIUM_TOKEN = os.getenv("MEDIUM_INTEGRATION_TOKEN")

def find_posts(posts_dir: Path):
    for child in posts_dir.iterdir():
        if child.is_dir():
            idx = child / "index.qmd"
            if idx.exists():
                yield child, idx


def publish_post_to_medium(post_path: Path, token: str):
    # Placeholder: read the post and print summary
    text = post_path.read_text(encoding='utf8')
    print(f"Would publish {post_path} (len={len(text)} chars) to Medium using token prefix {token[:4]}...")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    posts_dir = repo_root / "posts"

    if not MEDIUM_TOKEN:
        print("MEDIUM_INTEGRATION_TOKEN not set — skipping actual publish. Dry-run only.")

    for post_dir, idx in find_posts(posts_dir):
        print("Found post:", post_dir.name)
        publish_post_to_medium(idx, MEDIUM_TOKEN or "(no-token)")


if __name__ == '__main__':
    main()
