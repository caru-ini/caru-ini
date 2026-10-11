"""SVG primitives: boxes, pills, clipping, section marks, and inlined logos."""

from __future__ import annotations

import math
import re

from . import LOGOS
from .tokens import INK, SHAPES

_uid = 0


def uid(prefix: str) -> str:
    global _uid
    _uid += 1
    return f"{prefix}{_uid}"


def svg(width: float, height: float, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width:g}" height="{height:g}" viewBox="0 0 {width:g} {height:g}">{body}</svg>\n'
    )


def rrect(x: float, y: float, w: float, h: float, r: float, fill: str, stroke: str | None = None) -> str:
    s = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{s}/>'


def pill(x: float, y: float, w: float, h: float, fill: str, stroke: str | None = None) -> str:
    # Stroked pills are inset by half a pixel so the 1px rule stays crisp.
    if stroke:
        return rrect(x + 0.5, y + 0.5, w - 1, h - 1, (h - 1) / 2, fill, stroke)
    return rrect(x, y, w, h, h / 2, fill)


def clipped(w: float, h: float, r: float, body: str) -> str:
    cid = uid("clip")
    return f'<clipPath id="{cid}">{rrect(0, 0, w, h, r, "#000")}</clipPath><g clip-path="url(#{cid})">{body}</g>'


def mark(kind: str, cx: float, cy: float, size: float, rotate: float = 0) -> str:
    """A section shape centred at (cx, cy)."""
    return (
        f'<g transform="translate({cx:g} {cy:g}) rotate({rotate:g}) scale({size / 100:g}) translate(-50 -50)">'
        f"{SHAPES[kind][0]}</g>"
    )


def star(cx: float, cy: float, r: float, fill: str = INK) -> str:
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def _is_dark(hex_: str) -> bool:
    h = hex_.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b < 100


def _on_ink(inner: str, fg: str) -> str:
    """Swap dark fills for the on-ink foreground; brand colours stay as they are."""
    return re.sub(
        r'(fill|stroke)(="|:)(#[0-9a-fA-F]{3,6})',
        lambda m: f"{m.group(1)}{m.group(2)}{fg if _is_dark(m.group(3)) else m.group(3)}",
        inner,
    )


_ROOT_ATTR_DROP = {"width", "height", "xmlns", "version", "id", "style", "class", "preserveAspectRatio", "overflow"}


def logo(
    name: str, x: float, y: float, w: float, h: float,
    recolor: dict[str, str] | None = None, fg: str | None = None, viewbox: str | None = None,
) -> str:
    """Inline scripts/logos/<name>.svg scaled into a box. Ids get a unique prefix so logos
    don't collide; `fg` recolours dark fills for use on ink; `viewbox` crops."""
    raw = (LOGOS / f"{name}.svg").read_text()
    raw = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->|<!DOCTYPE[^>]*>", "", raw, flags=re.S)
    m = re.search(r"<svg\b([^>]*)>(.*)</svg>", raw, flags=re.S)
    if not m:
        raise ValueError(f"{name}: not an svg")
    attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(1)))
    inner = m.group(2)
    if "viewBox" not in attrs:
        attrs["viewBox"] = f"0 0 {attrs['width']} {attrs['height']}"
    if viewbox:
        attrs["viewBox"] = viewbox
    keep = " ".join(f'{k}="{v}"' for k, v in attrs.items() if k not in _ROOT_ATTR_DROP and not k.startswith("xmlns"))
    prefix = uid("l") + "-"
    for i in set(re.findall(r'\bid="([^"]+)"', inner)):
        inner = re.sub(rf'\bid="{re.escape(i)}"', f'id="{prefix}{i}"', inner)
        inner = inner.replace(f"url(#{i})", f"url(#{prefix}{i})")
        inner = re.sub(rf'href="#{re.escape(i)}"', f'href="#{prefix}{i}"', inner)
    for old, new in (recolor or {}).items():
        inner = inner.replace(old, new)
    if fg:
        inner = _on_ink(inner, fg)
    return f'<svg x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" {keep}>{inner}</svg>'
