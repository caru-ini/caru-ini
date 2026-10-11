"""README building blocks, each mirroring a component in the Figma file."""

from __future__ import annotations

import base64
from pathlib import Path

from .draw import clipped, logo, mark, pill, rrect, star, svg, uid
from .text import baseline, measure, paragraph, text, wrap
from .tokens import CYAN_INK, CYAN_TINT, INK, INK2, IRIS_TINT, MINT, MINT_TINT, R_HERO, R_INSET, R_PANEL, RULE, SHAPES, SURFACE, W

_SIGNATURE = ("circle", "triangle", "pentagon", "square")


def logo_mark(on_ink: bool = False) -> str:
    """●▲⬟■.moe wordmark (Figma "Logo"). Shapes 17.6px, gap 3, ".moe" Figtree ExtraBold 22."""
    s, gap = 17.6, 3
    x, body = 0.0, ""
    for kind in _SIGNATURE:
        body += mark(kind, x + s / 2, 11, s)
        x += s + gap
    x += gap
    tw = measure(".moe", 22, 800)
    body += text(".moe", 22, 800, x, baseline(0, 22, 22, 800), SURFACE if on_ink else INK)
    return svg(round(x + tw + 1), 22, body)


def signature() -> str:
    body = "".join(mark(k, 6 + i * 16, 6, 12) for i, k in enumerate(_SIGNATURE))
    return svg(60, 12, body)


def link_button(label: str, icon: str, primary: bool, on_ink: bool = False) -> str:
    """Figma "LinkButton": Primary is ink, Tonal is surface. Tonal gets a rule border and
    Primary a faint one so the pills still read on the README background."""
    h, size = 32, 14 if primary else 12
    tw = measure(label, size, 700)
    w = 16 + 14 + 7 + tw + 16
    if primary:
        body = pill(0, 0, w, h, INK, INK2 if on_ink else None)
        fg = SURFACE
    else:
        body = pill(0, 0, w, h, SURFACE, RULE)
        fg = INK
    body += logo(icon, 16, 9, 14, 14, fg=fg if primary else None)
    body += text(label, size, 700, 37, baseline(0, h, size, 700), fg)
    return svg(w, h, body)


def footer_link(label: str, icon: str, on_ink: bool = False) -> str:
    """Figma "FooterLink": icon 13 + Figtree Bold 13, padding 10/6, no fill."""
    h = 33
    tw = measure(label, 13, 700)
    w = 10 + 13 + 6 + tw + 10
    fg = SURFACE if on_ink else INK
    body = logo(icon, 10, 10, 13, 13, fg=fg if on_ink else None)
    body += text(label, 13, 700, 29, baseline(0, h, 13, 700), fg)
    return svg(w, h, body)


def award_chip(label: str) -> str:
    """Figma "AwardChip": cyan tint pill, trophy 13, Bold 13 with 1.6 leading."""
    h = 25
    tw = measure(label, 13, 700)
    w = 8 + 13 + 6 + tw + 10
    body = pill(0, 0, w, h, CYAN_TINT)
    body += logo("icon-trophy", 8, 6, 13, 13)
    body += text(label, 13, 700, 27, baseline(0, h, 13, 700))
    return svg(w, h, body)


def star_chip(count: int) -> str:
    """Figma "StarChip": iris tint pill with the star count (built from the API, never by hand)."""
    h = 25
    s = f"{count:,} Stars"
    tw = measure(s, 13, 700)
    w = 8 + 13 + 5 + tw + 10
    body = pill(0, 0, w, h, IRIS_TINT)
    body += star(14.5, 12.5, 6.2)
    body += text(s, 13, 700, 26, baseline(0, h, 13, 700))
    return svg(w, h, body)


def hero(name: str, role: str, intro: str, stars: int, repos: int, avatar: Path) -> str:
    """Figma "Hero", scaled to the README column: iris tint, name in Figtree Black, avatar at right."""
    H, pad, av = 272, 40, 200
    body = rrect(0, 0, W, H, R_HERO, IRIS_TINT)

    col_w = W - pad - av - 48 - pad
    name_lh, role_lh = 100 * 0.85, 20 * 1.3
    intro_h = 14 * 1.75 * len(wrap(intro, 14, 400, col_w))
    chip_h = 30
    content_h = name_lh + 10 + role_lh + 12 + intro_h + 18 + chip_h
    top = (H - content_h) / 2

    body += text(name, 100, 900, pad - 4, baseline(top, name_lh, 100, 900))
    y = top + name_lh + 10
    body += text(role, 20, 500, pad, baseline(y, role_lh, 20, 500))
    y += role_lh + 12
    para, _ = paragraph(intro, 14, 400, pad, y, col_w, 1.75)
    body += para
    y += intro_h + 18

    # Stats row: surface pills so they read on the tinted hero.
    x = pad
    for label, icon in ((f"{stars:,} stars", "star"), (f"{repos} public repos", "icon-globe")):
        tw = measure(label, 13, 700)
        w = 12 + 14 + 6 + tw + 14
        body += pill(x, y, w, chip_h, SURFACE)
        if icon == "star":
            body += star(x + 12 + 7, y + chip_h / 2, 6.5)
        else:
            body += logo(icon, x + 12, y + (chip_h - 14) / 2, 14, 14)
        body += text(label, 13, 700, x + 12 + 14 + 6, baseline(y, chip_h, 13, 700))
        x += w + 8

    avatar_b64 = base64.b64encode(avatar.read_bytes()).decode()
    cid = uid("clip")
    ax, ay = W - pad - av, (H - av) / 2
    body += f'<clipPath id="{cid}"><circle cx="{ax + av / 2:g}" cy="{ay + av / 2:g}" r="{av / 2:g}"/></clipPath>'
    body += (
        f'<image x="{ax:g}" y="{ay:g}" width="{av}" height="{av}" clip-path="url(#{cid})" '
        f'href="data:image/png;base64,{avatar_b64}"/>'
    )
    return svg(W, H, body)


def band(title: str, desc: str, kind: str) -> str:
    """Figma "SectionBand": section tint, big tilted mark at the top right, title + one line."""
    H, pad = 126, 28
    body = clipped(W, H, R_PANEL, rrect(0, 0, W, H, R_PANEL, SHAPES[kind][1]) + mark(kind, W - 103, 90, 200, 16))
    title_lh = 40 * 1.05
    body += text(title, 40, 700, pad - 2, baseline(pad, title_lh, 40, 700))
    body += text(desc, 14, 400, pad, baseline(pad + title_lh + 6, 14 * 1.6, 14, 400))
    return svg(W, H, body)


_PANEL_PAD, _PANEL_GAP, _PANEL_TITLE_LH = 20, 12, 32 * 1.25


def panel_height(desc: str, preview_h: float, width: float) -> float:
    desc_h = 14 * 1.75 * len(wrap(desc, 14, 400, width - 2 * _PANEL_PAD - 48))
    return _PANEL_PAD + _PANEL_TITLE_LH + _PANEL_GAP + desc_h + _PANEL_GAP + preview_h + 22


def panel(title: str, desc: str, kind: str, preview: tuple[str, float], width: float, H: float) -> str:
    """Figma "Panel" (Mobile layout): a tinted entrance card with a preview and a small mark
    tucked into the bottom-right corner. Panels in a row share a height and the previews
    sit on the bottom edge. `preview` is (svg at origin, height)."""
    pad, gap, title_lh = _PANEL_PAD, _PANEL_GAP, _PANEL_TITLE_LH
    preview_svg, preview_h = preview

    body = rrect(0, 0, width, H, R_PANEL, SHAPES[kind][1])
    body += mark(kind, width + 30.8 - 55, H + 41.8 - 55, 110)
    body = clipped(width, H, R_PANEL, body)
    body += text(title, 32, 700, pad - 1, baseline(pad, title_lh, 32, 700))
    para, _ = paragraph(desc, 14, 400, pad, pad + title_lh + gap, width - 2 * pad - 48, 1.75)
    body += para
    body += f'<g transform="translate({pad} {H - 22 - preview_h:g})">{preview_svg}</g>'
    # "Go" affordance: the whole image is the link in the README.
    body += f'<circle cx="{width - pad - 20:g}" cy="{pad + 20}" r="20" fill="{SURFACE}"/>'
    body += logo("icon-arrow-right", width - pad - 29, pad + 11, 18, 18)
    return svg(width, H, body)


def history_preview(entries: list[tuple[str, str]], width: float) -> tuple[str, float]:
    """Surface inset listing the latest entries: date in cyan ink, title in bold."""
    px, py, row_gap = 14, 12, 6
    row_h = 13 * 1.6
    H = py + len(entries) * row_h + (len(entries) - 1) * row_gap + py
    body = rrect(0, 0, width, H, R_INSET, SURFACE)
    for i, (date, title) in enumerate(entries):
        y = py + i * (row_h + row_gap)
        body += text(date, 13, 700, px, baseline(y, row_h, 13, 700), CYAN_INK)
        body += text(title, 13, 700, px + 46 + 12, baseline(y, row_h, 13, 700))
    return body, H


def blog_preview(title: str, date: str, colour: str, width: float) -> tuple[str, float]:
    """Surface inset with the post's jacket (cropped like the site) and its caption."""
    jw, jh = 112, 76
    cap_x = 8 + jw + 12
    cap_w = width - cap_x - 12
    lines = wrap(title, 14, 700, cap_w)[:3]
    cap_h = 13 * 1.4 + 2 + 14 * 1.25 * len(lines)
    H = max(jh + 16, cap_h + 16)
    body = rrect(0, 0, width, H, R_INSET, SURFACE)
    jy = (H - jh) / 2
    cid = uid("clip")
    body += f'<clipPath id="{cid}">{rrect(8, jy, jw, jh, 10, "#000")}</clipPath>'
    # The site shows the left-middle part of the 300x100 jacket at 0.912 scale.
    body += f'<g clip-path="url(#{cid})">{logo(f"jacket-{colour}", 8, jy, jw, jh, viewbox="19.7 8.8 122.8 83.3")}</g>'
    y = (H - cap_h) / 2
    body += text(date, 13, 700, cap_x, baseline(y, 13 * 1.4, 13, 700), INK2)
    y += 13 * 1.4 + 2
    for i, line in enumerate(lines):
        body += text(line, 14, 700, cap_x, baseline(y + i * 14 * 1.25, 14 * 1.25, 14, 700))
    return body, H


def _level_dots(level: int, x: float, y: float) -> str:
    return "".join(rrect(x + i * 16, y, 12, 12, 3, MINT if i < level else RULE) for i in range(3))


def skills_row(level: int, title: str, desc: str, chips: list[tuple[str, str]]) -> str:
    """One proficiency row of the Skills page: mint side panel + wrapped SkillChips."""
    side, pad, gap = 226, 20, 8
    chip_h = 36
    chips_x = side + pad
    max_x = W - pad - 1

    placed: list[tuple[float, float, str, str, float]] = []
    x, row = chips_x, 0
    for name, icon in chips:
        tw = measure(name, 14, 700)
        w = 10 + 18 + 8 + tw + 14
        if x + w > max_x and x > chips_x:
            x, row = chips_x, row + 1
        placed.append((x, row, name, icon, w))
        x += w + gap
    rows = row + 1
    chips_h = pad + rows * chip_h + (rows - 1) * gap + pad

    side_w = side - 2 * pad
    desc_lines = wrap(desc, 13, 400, side_w)
    side_h = pad + 12 + 10 + 18 * 1.25 + 8 + 13 * 1.6 * len(desc_lines) + pad
    H = max(chips_h, side_h)

    body = rrect(0, 0, W, H, R_PANEL, SURFACE)
    body += clipped(W, H, R_PANEL, rrect(0, 0, side, H, 0, MINT_TINT))
    body += rrect(0.5, 0.5, W - 1, H - 1, R_PANEL - 0.5, "none", RULE)

    y = pad
    body += _level_dots(level, pad, y)
    y += 12 + 10
    body += text(title, 18, 700, pad, baseline(y, 18 * 1.25, 18, 700))
    y += 18 * 1.25 + 8
    para, _ = paragraph(desc, 13, 400, pad, y, side_w, 1.6, INK2)
    body += para

    for x, row, name, icon, w in placed:
        y = pad + row * (chip_h + gap)
        body += pill(x, y, w, chip_h, SURFACE, RULE)
        # The Orca logo is drawn white for dark backgrounds.
        body += logo(icon, x + 10, y + 9, 18, 18, {"#ffffff": INK} if icon == "orca" else None)
        body += text(name, 14, 700, x + 36, baseline(y, chip_h, 14, 700))
    return svg(W, H, body)
