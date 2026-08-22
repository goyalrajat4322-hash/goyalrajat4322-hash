#!/usr/bin/env python3
"""
Generate a Neofetch-style terminal info card as an animated SVG.
Staggered line fade-in + blinking cursor in a dark terminal window.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 504
CANVAS_H = 325
TITLEBAR_H = 28
PAD = 20

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"

CYAN = "#22d3ee"
GREEN = "#39d353"
PURPLE = "#bc8cff"
GOLD = "#f2cc60"
WHITE = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
CORAL = "#ff7b72"

ENTRIES = [
    ("OS", "Arch Linux / macOS (AI & Data Science)", CYAN),
    ("Host", "SRM Institute (B.Tech CS & AI '28)", WHITE),
    ("Role", "Data Science & AI / ML Developer", GREEN),
    ("Languages", "Python, Java, SQL, C++", GOLD),
    ("ML / AI", "TensorFlow, OpenCV, Scikit-learn, NLP, GenAI", BLUE),
    ("Backend", "Flask, MySQL, MongoDB, REST APIs", PURPLE),
    ("Projects", "AI Resume Analyzer, AI Interview Analyzer", CYAN),
    ("Status", "Building ML systems · Open to Internships", CORAL),
]

COLOR_BLOCKS = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#22d3ee", "#e6edf3"]

STATIC = bool(os.environ.get("STATIC"))

def generate():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
    )
    
    parts.append(
        '<defs>'
        f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        '</linearGradient>'
        '</defs>'
    )
    
    # Window shell
    parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#ibg)"/>')
    parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
    
    # Titlebar dots
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*15}" cy="{TITLEBAR_H/2}" r="4.5" fill="{dot}"/>')
    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="11.5" text-anchor="middle">rajat@github: ~$ neofetch</text>'
    )
    
    content_top = TITLEBAR_H + 26
    line_h = 24
    
    # Header user@host
    user_header = (
        f'<text x="{PAD}" y="{content_top}" font-size="13" font-weight="700">'
        f'<tspan fill="{CYAN}">rajat</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{BLUE}">github</tspan>'
        f'<tspan fill="{MUTED}">  --------------------------</tspan>'
        f'</text>'
    )
    
    if not STATIC:
        parts.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="0.1s" fill="freeze"/>{user_header}</g>'
        )
    else:
        parts.append(user_header)
        
    start_y = content_top + 24
    delay = 0.25
    
    for i, (k, v, val_color) in enumerate(ENTRIES):
        cur_y = start_y + i * line_h
        line_svg = (
            f'<text x="{PAD}" y="{cur_y}" font-size="12">'
            f'<tspan fill="{CYAN}" font-weight="600">{k:10s}</tspan>'
            f'<tspan fill="{MUTED}">: </tspan>'
            f'<tspan fill="{val_color}">{v}</tspan>'
            f'</text>'
        )
        if not STATIC:
            parts.append(
                f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0, -3" to="0, 0" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/>'
                f'{line_svg}</g>'
            )
        else:
            parts.append(line_svg)
        delay += 0.12
        
    # Color blocks at bottom
    blocks_y = start_y + len(ENTRIES) * line_h + 14
    block_parts = []
    block_w = 16
    block_h = 10
    for j, col in enumerate(COLOR_BLOCKS):
        bx = PAD + j * (block_w + 6)
        block_parts.append(f'<rect x="{bx}" y="{blocks_y}" width="{block_w}" height="{block_h}" rx="2" fill="{col}"/>')
    
    # Blinking cursor next to blocks
    cursor_x = PAD + len(COLOR_BLOCKS) * (block_w + 6) + 10
    block_parts.append(
        f'<rect x="{cursor_x}" y="{blocks_y - 2}" width="7" height="14" fill="{CYAN}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>'
    )
    
    if not STATIC:
        parts.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="{delay:.2f}s" fill="freeze"/>{"".join(block_parts)}</g>'
        )
    else:
        parts.append("".join(block_parts))
        
    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    svg = generate()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes) {CANVAS_W}x{CANVAS_H}")
