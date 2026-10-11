"""Drawing library for the README assets. Content lives in scripts/content.py."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGOS = ROOT / "scripts" / "logos"
CACHE = ROOT / "scripts" / ".cache"
OUT = ROOT / "assets"
