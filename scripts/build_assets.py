# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools>=4.53", "uharfbuzz>=0.45"]
# ///
"""Builds the SVG assets in assets/ for README.md.

    uv run scripts/build_assets.py

Content comes from scripts/content.py, drawing from scripts/readme_assets/.
Star counts come from the GitHub API (set GITHUB_TOKEN to raise the rate limit)
and the latest post from the blog feed, so the workflow can rebuild on a schedule.
Fonts and the avatar are cached in scripts/.cache.
"""

import content
from readme_assets import OUT
from readme_assets import components as c
from readme_assets.fetch import cached, github_stars, latest_post, repo_stars
from readme_assets.tokens import JACKET_COLOURS, W


def write(name: str, svg: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg)
    print(f"  {name}")


def main() -> None:
    total, repo_count, per_repo = github_stars(content.USER)
    for full in content.STAR_REPOS:
        if full not in per_repo:
            per_repo[full] = repo_stars(full)
    post_title, post_date, post_index = latest_post(content.FEED_URL)
    print(f"stars: {total} across {repo_count} repos / latest post: {post_title} ({post_date})")

    avatar = cached(f"https://github.com/{content.USER}.png?size=400", "avatar.png")
    write("hero.svg", c.hero(**content.HERO, stars=total, repos=repo_count, avatar=avatar))
    write("signature.svg", c.signature())

    for name, label, icon, primary in content.BUTTONS:
        write(f"{name}.svg", c.link_button(label, icon, primary))
        write(f"{name}-dark.svg", c.link_button(label, icon, primary, on_ink=True))
    for name, label, icon in content.FOOTER_LINKS:
        write(f"{name}.svg", c.footer_link(label, icon))
        write(f"{name}-dark.svg", c.footer_link(label, icon, on_ink=True))

    for name, label in content.AWARDS.items():
        write(f"{name}.svg", c.award_chip(label))
    for full in content.STAR_REPOS:
        write(f"stars-{full.split('/')[1]}.svg", c.star_chip(per_repo[full]))

    for name, title, desc, kind in content.BANDS:
        write(f"{name}.svg", c.band(title, desc, kind))
    for level, title, desc, chips in content.LEVELS:
        write(f"skills-{level}.svg", c.skills_row(level, title, desc, chips))

    # Two panels side by side; they share a height like the site's home page.
    pw = (W - 8) / 2
    inset_w = pw - 40
    history_pv = c.history_preview(content.HISTORY[:3], inset_w)
    blog_pv = c.blog_preview(post_title, post_date, JACKET_COLOURS[post_index % 4], inset_w)
    ph = max(c.panel_height(content.HISTORY_DESC, history_pv[1], pw), c.panel_height(content.BLOG_DESC, blog_pv[1], pw))
    write("panel-history.svg", c.panel("History", content.HISTORY_DESC, "circle", history_pv, pw, ph))
    write("panel-blog.svg", c.panel("Blog", content.BLOG_DESC, "triangle", blog_pv, pw, ph))


if __name__ == "__main__":
    main()
