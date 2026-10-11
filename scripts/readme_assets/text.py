"""Text as outlines: GitHub strips web fonts from README images, so every string is
shaped with HarfBuzz (kerning included) and emitted as SVG path data."""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from functools import lru_cache

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from .fetch import cached
from .tokens import FONT_URLS, INK


@dataclass
class Face:
    font: hb.Font
    glyphs: object
    order: list[str]
    upem: int
    ascent: int
    descent: int


@lru_cache(maxsize=None)
def face(family: str, weight: int) -> Face:
    """A static instance of the variable font at `weight`, ready for shaping and drawing."""
    vf = TTFont(cached(FONT_URLS[family], f"{family}.ttf"))
    inst = instancer.instantiateVariableFont(vf, {"wght": weight}, inplace=False)
    buf = io.BytesIO()
    inst.save(buf)
    hb_face = hb.Face(buf.getvalue())
    hhea = inst["hhea"]
    return Face(hb.Font(hb_face), inst.getGlyphSet(), inst.getGlyphOrder(), hb_face.upem, hhea.ascent, -hhea.descent)


_JP_CHAR = re.compile(r"[　-ヿ㐀-䶿一-鿿＀-￯]")


def _num(v: float) -> str:
    # Two decimals is sub-pixel at these sizes and keeps the outlines small.
    return f"{v:.2f}".rstrip("0").rstrip(".") or "0"


def runs(text_: str) -> list[tuple[str, str]]:
    """Split text into (family, chunk) runs: Japanese goes to M PLUS 2, the rest to Figtree."""
    out: list[list[str]] = []
    for ch in text_:
        fam = "mplus2" if _JP_CHAR.match(ch) else "figtree"
        if out and out[-1][0] == fam:
            out[-1][1] += ch
        else:
            out.append([fam, ch])
    return [(f, t) for f, t in out]


def shape_run(text_: str, family: str, weight: int, size: float, x: float, y: float) -> tuple[str, float]:
    """Path data for one single-family run at baseline (x, y), plus its advance width."""
    f = face(family, weight)
    buf = hb.Buffer()
    buf.add_str(text_)
    buf.guess_segment_properties()
    hb.shape(f.font, buf, {"kern": True, "liga": True, "calt": True})
    s = size / f.upem
    cmds: list[str] = []
    pen_x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(f.glyphs, ntos=_num)
        tp = TransformPen(pen, (s, 0, 0, -s, x + (pen_x + pos.x_offset) * s, y - pos.y_offset * s))
        f.glyphs[f.order[info.codepoint]].draw(tp)
        if d := pen.getCommands():
            cmds.append(d)
        pen_x += pos.x_advance
    return " ".join(cmds), pen_x * s


def measure(text_: str, size: float, weight: int) -> float:
    return sum(shape_run(t, fam, weight, size, 0, 0)[1] for fam, t in runs(text_))


def text(text_: str, size: float, weight: int, x: float, baseline_y: float, fill: str = INK) -> str:
    """One line of text as a single outlined path, anchored at the baseline."""
    parts: list[str] = []
    for fam, chunk in runs(text_):
        d, adv = shape_run(chunk, fam, weight, size, x, baseline_y)
        parts.append(d)
        x += adv
    return f'<path fill="{fill}" d="{" ".join(parts)}"/>'


def baseline(top: float, line_height: float, size: float, weight: int, family: str = "figtree") -> float:
    """Baseline of a line box, with half-leading like a browser."""
    f = face(family, weight)
    content = (f.ascent + f.descent) * size / f.upem
    return top + (line_height - content) / 2 + f.ascent * size / f.upem


def wrap(text_: str, size: float, weight: int, max_width: float) -> list[str]:
    """Greedy wrap on spaces; Japanese text (no spaces) wraps per character."""
    units = text_.split(" ") if " " in text_ else list(text_)
    joiner = " " if " " in text_ else ""
    lines: list[str] = []
    line = ""
    for unit in units:
        trial = f"{line}{joiner}{unit}" if line else unit
        if line and measure(trial, size, weight) > max_width:
            lines.append(line)
            line = unit
        else:
            line = trial
    return lines + [line]


def paragraph(
    text_: str, size: float, weight: int, x: float, top: float, max_width: float, leading: float, fill: str = INK
) -> tuple[str, float]:
    """Wrapped paragraph; returns (svg, height)."""
    lh = size * leading
    out = []
    for i, line in enumerate(wrap(text_, size, weight, max_width)):
        out.append(text(line, size, weight, x, baseline(top + i * lh, lh, size, weight), fill))
    return "".join(out), lh * len(out)
