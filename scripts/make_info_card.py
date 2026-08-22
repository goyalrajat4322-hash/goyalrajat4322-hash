#!/usr/bin/env python3
"""
Generate a Neofetch-style terminal info card as an SVG.
Designed to be 100% compatible with GitHub's image proxy and sanitizer.
Uses CSS keyframe animations that gracefully default to fully visible text.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 860
CANVAS_H = 290
TITLEBAR_H = 30
PAD = 22

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
TITLE_TEXT = "#7d8590"

CYAN = "#22d3ee"
GREEN = "#39d353"
PURPLE = "#bc8cff"
GOLD = "#f2cc60"
WHITE = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
CORAL = "#ff7b72"

COLOR_BLOCKS = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#22d3ee", "#e6edf3"]

def generate():
    css = """
    @keyframes lineFade {
      0%   { opacity: 0; transform: translateY(-4px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    .ln {
      animation: lineFade 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) both;
    }
    @media (prefers-reduced-motion: reduce) {
      .ln { animation: none !important; opacity: 1 !important; }
    }
    """.strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#ibg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    # Titlebar dots
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">rajat@github: ~$ neofetch --system</text>'
    )

    left_col_x = PAD + 8
    right_col_x = 440
    start_y = TITLEBAR_H + 30
    line_h = 25

    # Header in left col
    parts.append(
        f'<g class="ln" style="animation-delay: 0.05s;">'
        f'<text x="{left_col_x}" y="{start_y}" font-size="14" font-weight="700">'
        f'<tspan fill="{CYAN}">rajat</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{BLUE}">github</tspan>'
        f'<tspan fill="{MUTED}">  ───────────────</tspan>'
        f'</text></g>'
    )

    left_entries = [
        ("OS", "Arch Linux / macOS (AI & Data Science)", CYAN),
        ("Host", "SRM Institute (B.Tech CS & AI '28)", WHITE),
        ("Role", "Data Science & AI / ML Developer", GREEN),
        ("Languages", "Python, Java, SQL, C++", GOLD),
        ("ML / DL", "TensorFlow, OpenCV, Scikit-learn, NLP", BLUE),
        ("Backend", "Flask, FastAPI, MySQL, MongoDB", PURPLE),
    ]

    delay = 0.12
    for i, (k, v, val_color) in enumerate(left_entries):
        cur_y = start_y + (i + 1) * line_h + 4
        parts.append(
            f'<g class="ln" style="animation-delay: {delay:.2f}s;">'
            f'<text x="{left_col_x}" y="{cur_y}" font-size="12.5">'
            f'<tspan fill="{CYAN}" font-weight="600">{k:10s}</tspan>'
            f'<tspan fill="{MUTED}">: </tspan>'
            f'<tspan fill="{val_color}">{v}</tspan>'
            f'</text></g>'
        )
        delay += 0.06

    # Right column header
    parts.append(
        f'<g class="ln" style="animation-delay: 0.15s;">'
        f'<text x="{right_col_x}" y="{start_y}" font-size="14" font-weight="700">'
        f'<tspan fill="{PURPLE}">system.profile</tspan>'
        f'<tspan fill="{MUTED}">  ───────────────</tspan>'
        f'</text></g>'
    )

    right_entries = [
        ("Focus", "Computer Vision & Generative AI", CYAN),
        ("Resume AI", "82% skill-match feature extraction", GREEN),
        ("Vision AI", "89% interview anomaly detection", GOLD),
        ("Projects", "Peblo TV, Interview Analyzer, Resume AI", BLUE),
        ("Open To", "Data Science Internships & AI Research", CORAL),
        ("Status", "Active · Solving DSA & Building Systems", WHITE),
    ]

    for i, (k, v, val_color) in enumerate(right_entries):
        cur_y = start_y + (i + 1) * line_h + 4
        parts.append(
            f'<g class="ln" style="animation-delay: {delay:.2f}s;">'
            f'<text x="{right_col_x}" y="{cur_y}" font-size="12.5">'
            f'<tspan fill="{PURPLE}" font-weight="600">{k:10s}</tspan>'
            f'<tspan fill="{MUTED}">: </tspan>'
            f'<tspan fill="{val_color}">{v}</tspan>'
            f'</text></g>'
        )
        delay += 0.06

    # Bottom ANSI Color Palette + Blinking Prompt Cursor
    palette_y = CANVAS_H - 24
    parts.append(f'<g class="ln" style="animation-delay: {delay:.2f}s;">')
    parts.append(f'<text x="{left_col_x}" y="{palette_y + 9}" fill="{MUTED}" font-size="11">ANSI:</text>')
    bx = left_col_x + 45
    block_w = 20
    block_h = 11
    for col in COLOR_BLOCKS:
        parts.append(f'<rect x="{bx}" y="{palette_y}" width="{block_w}" height="{block_h}" rx="2.5" fill="{col}"/>')
        bx += block_w + 6
    
    # Blinking prompt cursor
    parts.append(
        f'<rect x="{bx + 6}" y="{palette_y - 1}" width="8" height="13" fill="{CYAN}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    parts.append('</g>')

    parts.append('</svg>')
    return "".join(parts)


if __name__ == "__main__":
    svg = generate()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes) {CANVAS_W}x{CANVAS_H}")
