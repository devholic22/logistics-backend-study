# -*- coding: utf-8 -*-
"""손으로 레이아웃한 도식용 SVG 프리미티브."""
import html

FONT = "-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo',Pretendard,'Malgun Gothic',system-ui,sans-serif"

PAPER = "#fbfbf9"
RULE  = "#e4e7e0"
INK   = "#1f2937"
INK2  = "#4b5563"
INK3  = "#6b7280"

GREEN  = ("#2f6b46", "#eef6f1")
BLUE   = ("#2b4fa8", "#e9eef9")
AMBER  = ("#8a6a1c", "#fbf4e3")
SLATE  = ("#475569", "#eef1f5")
PURPLE = ("#6b3fa0", "#f1ebf9")
OLIVE  = ("#6b7f3a", "#f1f4e7")

SOLID = "#334155"   # 재고(물리) 이동
DASH  = "#6b7280"   # 정보 흐름

def esc(s):
    return html.escape(str(s), quote=True)

def tw(s, size):
    """텍스트 폭 추정 — 한글 1em, 라틴/숫자 0.56em."""
    w = 0.0
    for c in s:
        if ord(c) > 0x1100:
            w += size * 1.0
        elif c == " ":
            w += size * 0.30
        else:
            w += size * 0.56
    return w

class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.parts = []
        self.markers = {}

    def marker(self, color):
        key = color.lstrip("#")
        if key not in self.markers:
            self.markers[key] = (
                f'<marker id="a{key}" markerWidth="8" markerHeight="8" refX="7.2" refY="4" '
                f'orient="auto" markerUnits="strokeWidth">'
                f'<path d="M0,0.6 L7.6,4 L0,7.4 z" fill="{color}"/></marker>'
            )
        return f"url(#a{key})"

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=14, fill=INK2, weight=400, anchor="middle", ls=0):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"'
                 + (f' letter-spacing="{ls}"' if ls else "")
                 + f'>{esc(s)}</text>')

    def rrect(self, x, y, w, h, r, fill, stroke=None, sw=2, dash=None, op=None):
        a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if op:
            a += f' opacity="{op}"'
        self.add(a + "/>")

    def card(self, x, y, w, title, lines=(), color=SLATE, min_h=None, title_size=17, body_size=13.5):
        """컬러 헤더칩이 달린 흰 카드. 높이를 반환."""
        c, bg = color
        chip_h = 32
        body_h = (10 + 19 * len(lines)) if lines else 0
        h = 10 + chip_h + body_h + 12
        pad_top = 0
        if min_h and min_h > h:
            pad_top = (min_h - h) / 2
            h = min_h
        self.rrect(x, y, w, h, 12, "#ffffff", c, 2)
        cy = y + pad_top
        self.rrect(x + 10, cy + 10, w - 20, chip_h, 8, c)
        self.text(x + w / 2, cy + 10 + 22, title, title_size, "#ffffff", 700)
        for i, ln in enumerate(lines):
            bold = ln.startswith("*")
            value = ln[1:] if bold else ln
            self.text(x + w / 2, cy + 10 + chip_h + 10 + 14 + i * 19, value, body_size,
                      c if bold else INK2, 700 if bold else 400)
        return h

    def panel(self, x, y, w, h, label, color=None, dashed=True, label_at="left"):
        """그룹 경계 + 라벨칩."""
        if color:
            c, bg = color
            self.rrect(x, y, w, h, 16, bg, c, 1.6, "7 6" if dashed else None)
            tc = c
        else:
            self.rrect(x, y, w, h, 16, "none", "#a9b0a4", 1.6, "7 6")
            tc = INK3
        lw = tw(label, 12.5) + 22
        lx = x + 18 if label_at == "left" else x + (w - lw) / 2
        self.rrect(lx, y - 13, lw, 26, 13, PAPER, tc, 1.4)
        self.text(lx + lw / 2, y + 4.5, label, 12.5, tc, 700)

    def pill(self, cx, cy, lines, color=INK2, size=12.5):
        if isinstance(lines, str):
            lines = [lines]
        w = max(tw(line, size) for line in lines) + 22
        h = 24 + (len(lines) - 1) * 17
        self.rrect(cx - w / 2, cy - h / 2, w, h, h / 2 if len(lines) == 1 else 10,
                   "#ffffff", color, 1.4)
        y0 = cy - h / 2 + 16.5
        for i, line in enumerate(lines):
            self.text(cx, y0 + i * 17, line, size, color, 700)
        return w, h

    def edge(self, pts, color=SOLID, dashed=False, sw=2.2):
        d = " ".join(("M" if i == 0 else "L") + f"{p[0]:.1f},{p[1]:.1f}" for i, p in enumerate(pts))
        a = (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
             f'stroke-linejoin="round" stroke-linecap="round" marker-end="{self.marker(color)}"')
        if dashed:
            a += ' stroke-dasharray="7 5"'
        self.add(a + "/>")

    def legend(self, x, y, items):
        """items: [(kind, text)] kind in {'solid','dash'}"""
        cx = x
        for kind, label in items:
            col = SOLID if kind == "solid" else DASH
            self.add(f'<path d="M{cx},{y} L{cx+30},{y}" stroke="{col}" stroke-width="2.2" '
                     f'stroke-linecap="round"'
                     + (' stroke-dasharray="7 5"' if kind == "dash" else "") + "/>")
            self.text(cx + 38, y + 4.5, label, 12.5, INK3, 600, "start")
            cx += 38 + tw(label, 12.5) + 26

    def render(self):
        defs = "".join(self.markers.values())
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" font-family="{FONT}">'
            f"<title>{esc(self.title)}</title>"
            f"<defs>{defs}</defs>"
            f'<rect x="0.5" y="0.5" width="{self.w-1}" height="{self.h-1}" rx="10" ry="10" '
            f'fill="{PAPER}" stroke="{RULE}"/>'
            + "".join(self.parts) + "</svg>"
        )
