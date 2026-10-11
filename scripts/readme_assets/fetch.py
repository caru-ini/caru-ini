"""Network access: cached downloads, GitHub API, blog feed."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from . import CACHE

_UA = "caru-ini-readme"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": "application/json, */*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def cached(url: str, name: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / name
    if not path.exists():
        path.write_bytes(fetch(url))
    return path


def gh_json(url: str):
    headers = {"User-Agent": _UA, "Accept": "application/vnd.github+json"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return json.load(r)


def github_stars(user: str) -> tuple[int, int, dict[str, int]]:
    """Total stars and public repo count for `user`, plus stars per repo (forks excluded)."""
    repos: list[dict] = []
    page = 1
    while True:
        chunk = gh_json(f"https://api.github.com/users/{user}/repos?per_page=100&page={page}")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    per_repo = {r["full_name"]: r["stargazers_count"] for r in own}
    return sum(per_repo.values()), len(own), per_repo


def repo_stars(full_name: str) -> int:
    return gh_json(f"https://api.github.com/repos/{full_name}")["stargazers_count"]


def latest_post(feed_url: str) -> tuple[str, str, int]:
    """(title, date as Y.M.D, index-from-oldest) of the newest post in a JSON Feed."""
    items = json.loads(fetch(feed_url))["items"]
    item = items[0]
    date = (item.get("date_published") or item.get("date_modified") or "")[:10]
    y, m, d = (int(p) for p in date.split("-"))
    return item["title"], f"{y}.{m}.{d}", len(items) - 1
