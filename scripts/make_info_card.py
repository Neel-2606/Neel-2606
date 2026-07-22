#!/usr/bin/env python3
"""Neofetch-style info card SVG for Neel Prajapati.
STATIC=1 emits a frozen frame for local preview."""
import os

STATIC = os.environ.get("STATIC") == "1"

W, H = 680, 360
BG = "#0d1117"
BORDER = "#1E90FF"
TITLE = "#1E90FF"
KEY = "#39d353"
VAL = "#c9d1d9"
DIM = "#8b949e"

ROWS = [
    ("Role", "AI Engineer • Full-Stack Developer"),
    ("Education", "B.E. Computer Science • MSU Baroda"),
    ("CGPA", "8.31"),
    ("Current Focus", "Generative AI • Computer Vision • Full Stack Development • NASA Data"),
    ("Tech Stack", "Python • Java • React • Next.js • PostgreSQL"),
    ("Achievements", "🏆 NASA Space Apps Winner / 🥈 IBM AI Innovation Challenge / 🥈 Ingenius Runner-Up / 🚀 Open Source Contributor"),
    ("Location", "Vadodara, India"),
    ("Motto", "Don't just build models— Build things that ship.")
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

parts = []
# Added a title and alt text placeholder within svg standard if possible, but standard is just <title> and <desc>
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Fira Code, Consolas, monospace" role="img" aria-label="Neel Prajapati Info Card">')
parts.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>')

# title bar dots
parts.append('<circle cx="22" cy="24" r="5" fill="#ff5f56"/>')
parts.append('<circle cx="40" cy="24" r="5" fill="#ffbd2e"/>')
parts.append('<circle cx="58" cy="24" r="5" fill="#27c93f"/>')
parts.append(f'<text x="{W-18}" y="28" text-anchor="end" font-size="12" fill="{DIM}">neofetch</text>')

# header line: neel@github
def animrow(y, inner, delay):
    if STATIC:
        return f'<g transform="translate(0,{y})" opacity="1">{inner}</g>'
    # Animation duration 1s as requested, plays once (fill="freeze")
    return (f'<g transform="translate(0,{y})" opacity="0">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="1s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="14 {y}" to="0 {y}" begin="{delay}s" dur="1s" fill="freeze"/></g>')

y = 60
delay = 0.2
header = (f'<text x="24" y="0" font-size="15"><tspan fill="{TITLE}" font-weight="700">neel</tspan>'
          f'<tspan fill="{VAL}">@</tspan><tspan fill="{TITLE}" font-weight="700">github</tspan></text>')
parts.append(animrow(y, header, round(delay, 2)))
y += 8
rule = f'<rect x="24" y="0" width="{W-48}" height="1.5" fill="{BORDER}" opacity="0.5"/>'
delay += 0.15
parts.append(animrow(y, rule, round(delay, 2)))

y += 24
for k, v in ROWS:
    delay += 0.15
    inner = (f'<text x="24" y="0" font-size="13.5">'
             f'<tspan fill="{KEY}" font-weight="700">{esc(k)}</tspan>'
             f'<tspan fill="{DIM}" dx="6">&#8250;</tspan>'
             f'<tspan fill="{VAL}" dx="6">{esc(v)}</tspan></text>')
    parts.append(animrow(y, inner, round(delay, 2)))
    y += 26

# color swatches footer
delay += 0.2
swatch = ['#ff5f56', '#ffbd2e', '#39d353', '#1E90FF', '#8A2BE2', '#3ECF8E', '#c9d1d9']
sw = ''.join(f'<rect x="{24 + i*18}" y="-11" width="14" height="14" rx="2" fill="{c}"/>' for i, c in enumerate(swatch))
parts.append(animrow(y + 6, sw, round(delay, 2)))

parts.append('</svg>')
open("info-card.svg", "w", encoding="utf-8").write("\n".join(parts))
print("wrote info-card.svg")
