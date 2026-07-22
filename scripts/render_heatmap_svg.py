#!/usr/bin/env python3
"""Render data/contributions.json as an animated 53x7 heatmap SVG.
Boxes reveal in a diagonal slide-down, play once on load, then freeze."""
import json, os
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG = "#0d1117"
ACCENT = "#1E90FF"
DIM = "#8b949e"
TEXT = "#c9d1d9"

CELL = 13
GAP = 3
PAD_L = 20
PAD_T = 46

def load():
    with open("data/contributions.json") as f:
        return json.load(f)

def weeks_from_days(days):
    """Group into columns of 7 aligned to weekday (0=Sun)."""
    cols = []
    cur = [None] * 7
    for d in days:
        wd = datetime.strptime(d["date"], "%Y-%m-%d").weekday()  # Mon=0
        wd = (wd + 1) % 7  # convert to Sun=0
        if wd == 0 and any(c is not None for c in cur):
            cols.append(cur)
            cur = [None] * 7
        cur[wd] = d
    if any(c is not None for c in cur):
        cols.append(cur)
    return cols[-53:]

def main():
    data = load()
    days = data["days"]
    cols = weeks_from_days(days)
    ncols = len(cols)

    W = PAD_L + ncols * (CELL + GAP) + 20
    H = PAD_T + 7 * (CELL + GAP) + 60

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="Fira Code, Consolas, monospace">']
    out.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{ACCENT}" stroke-width="1.5" opacity="1"/>')

    # keyframe css: cells start hidden/shifted, animate in
    out.append('<style>')
    out.append('.cell{opacity:0;transform:translateY(-6px);animation:pop .35s ease-out forwards;}')
    out.append('@keyframes pop{to{opacity:1;transform:translateY(0);}}')
    out.append('</style>')

    # title
    total = data.get("stats", {}).get("total_text", "")
    out.append(f'<text x="{PAD_L}" y="26" font-size="14" fill="{TEXT}" font-weight="700">'
               f'Contribution activity</text>')
    if total:
        out.append(f'<text x="{W-20}" y="26" text-anchor="end" font-size="12" fill="{DIM}">{total}</text>')

    # cells, diagonal stagger
    for ci, col in enumerate(cols):
        for ri, d in enumerate(col):
            lvl = d["level"] if d else 0
            color = PALETTE[min(lvl, len(PALETTE) - 1)]
            x = PAD_L + ci * (CELL + GAP)
            y = PAD_T + ri * (CELL + GAP)
            delay = (ci + ri) * 0.012
            out.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                       f'fill="{color}" style="animation-delay:{delay:.3f}s"/>')

    # legend
    ly = PAD_T + 7 * (CELL + GAP) + 22
    out.append(f'<text x="{PAD_L}" y="{ly+11}" font-size="11" fill="{DIM}">Less</text>')
    for i, c in enumerate(PALETTE):
        lx = PAD_L + 40 + i * (CELL + 2)
        out.append(f'<rect x="{lx}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
    out.append(f'<text x="{PAD_L + 40 + len(PALETTE)*(CELL+2) + 6}" y="{ly+11}" font-size="11" fill="{DIM}">More</text>')

    # stats footer
    st = data.get("stats", {})
    foot = f'Current streak: {st.get("current_streak",0)}d   ·   Longest: {st.get("longest_streak",0)}d'
    out.append(f'<text x="{W-20}" y="{ly+11}" text-anchor="end" font-size="11" fill="{ACCENT}">{foot}</text>')

    out.append('</svg>')
    with open("contrib-heatmap.svg", "w") as f:
        f.write("\n".join(out))
    print(f"wrote contrib-heatmap.svg ({ncols} weeks)")

if __name__ == "__main__":
    main()
