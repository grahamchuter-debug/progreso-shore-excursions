#!/usr/bin/env python3
"""Download hero and content images from Unsplash (Unsplash License)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"

# Direct images.unsplash.com URLs (stable photo IDs)
DOWNLOADS: list[tuple[str, str]] = [
    ("hero-progreso.png", "https://images.unsplash.com/photo-1750942725387-3485cf0c9d7b?w=1920&q=80&fm=jpg"),
    ("chichen-itza.png", "https://images.unsplash.com/photo-1750942725387-3485cf0c9d7b?w=1920&q=80&fm=jpg"),
    ("uxmal.png", "https://images.unsplash.com/photo-1777000969224-0b3f09971246?w=1920&q=80&fm=jpg"),
    ("cenote.png", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1920&q=80&fm=jpg"),
    ("merida.png", "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1920&q=80&fm=jpg"),
    ("pink-lagoon.png", "https://images.unsplash.com/photo-1551884831-bbf3cdc6469e?w=1920&q=80&fm=jpg"),
    ("progreso-port.png", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80&fm=jpg"),
    ("progreso-beach.png", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80&fm=jpg"),
    ("progreso-intro.png", "https://images.unsplash.com/photo-1777000969224-0b3f09971246?w=1920&q=80&fm=jpg"),
    ("best-progreso-excursions.png", "https://images.unsplash.com/photo-1750942725387-3485cf0c9d7b?w=1920&q=80&fm=jpg"),
    ("one-day-progreso.png", "https://images.unsplash.com/photo-1777000969224-0b3f09971246?w=1920&q=80&fm=jpg"),
]


def download(filename: str, url: str) -> bool:
    dest = IMAGES / filename
    print(f"  {filename}")
    result = subprocess.run(
        ["curl", "-fsSL", "-o", str(dest), url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"    FAILED: {result.stderr.strip()}", file=sys.stderr)
        return False
    size = dest.stat().st_size
    if size < 10_000:
        print(f"    WARNING: small file ({size} bytes)", file=sys.stderr)
    print(f"    OK ({size // 1024} KB)")
    return True


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    print("Downloading Progreso images from Unsplash…")
    failed = 0
    for filename, url in DOWNLOADS:
        if not download(filename, url):
            failed += 1
    if failed:
        raise SystemExit(f"{failed} download(s) failed.")
    print("Done.")


if __name__ == "__main__":
    main()
