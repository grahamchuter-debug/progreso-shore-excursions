#!/usr/bin/env python3
"""Re-download Progreso images from documented Wikimedia Commons sources. See images/ATTRIBUTION.md."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
DOWNLOADS = [
    ("chichen-itza.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/51/Chichen_Itza_3.jpg"),
    ("uxmal.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e5/Uxmal_Pyramid_of_the_Magician.jpg"),
    ("cenote.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/54/Cenote_Ik_Kil%2C_Yucatan%2C_Dec_2011_-_05.jpg"),
    ("merida.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f2/Merida-cathedral-Yucatan-state.jpg"),
    ("pink-lagoon.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b3/Celestun_Flamingos_-_Pink_pink_pink.jpg"),
    ("progreso-port.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/de/Progreso_pier_Yucatan_2009.jpg"),
    ("progreso-beach.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c2/Progreso_Yucatan_Beach_2014_Califa_J.jpg"),
]
def main():
    print("Prefer existing PNG files already converted for the site.")
    print("Raw Commons URLs are listed in images/ATTRIBUTION.md.")
    for name, url in DOWNLOADS:
        print(f"  {name}: {url}")
if __name__ == "__main__":
    main()
