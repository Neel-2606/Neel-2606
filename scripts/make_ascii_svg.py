#!/usr/bin/env python3
"""Monochrome self-typing ASCII art SVG.

If a prepped grayscale image (source-prepped.png) exists AND pillow/numpy are
installed, it converts the photo. Otherwise it falls back to a built-in
hand-authored ASCII block so the card always renders.
Each row wipes in left-to-right with a cursor, staggered top->bottom, then freezes.
"""
import os

RAMP = " .`:-=+*cs#%@"  # bright(sparse) -> dark(dense)
FILL = "#c9d1d9"
CURSOR = "#1E90FF"
BG = "#0d1117"
COLS, ROWS_N = 104, 46

def from_photo():
    try:
        import numpy as np
        from PIL import Image
    except Exception:
        return None
    if not os.path.exists("source-prepped.png"):
        return None
    img = Image.open("source-prepped.png").convert("L")
    w, h = img.size
    aspect = 0.5  # chars are ~2x tall
    tw = COLS
    th = max(1, int(tw * (h / w) * aspect))
    img = img.resize((tw, th))
    a = np.asarray(img)
    lines = []
    n = len(RAMP)
    for row in a:
        # v=0 (black) maps to index 0 (space), v=255 (white) maps to index n-1 (@)
        line = "".join(RAMP[min(n - 1, int(v / 255 * (n - 1)))] for v in row)
        lines.append(line.rstrip())
    return [l for l in lines]

# Fallback hand-authored portrait (a clean terminal bust silhouette + monogram).
FALLBACK = r"""
                  .:-==+++++==-:.
               :-=*#%%%######%%%#*=-:
             :=*%%################%%*=:
           .=#%####################%%#=.
          -#%########################%#-
         =%############################%=
        -%##############################%-
        %###%%##%%%%%%%%%%%%%%%%##%%###%%#%
       :%###*.                      .*###%:
       =###%.   .:-==++++++++==-:.   .%###=
       *###+  .=*%################%*=. +###*
       *###- .#%####################%#. -###*
       *###- =%######%%%%%%%%######%%#= -###*
       *###= .%####%-          -%####%. =###*
       *###*  *###%   N E E L    %###*  *###*
       =####. .%###.  P R A J .  .###%. .####=
        %###%  -%###%%%%%%%%%%###%-  %###%
        :%###*  .=*%##########%*=.  *###%:
         =%###%:    .:-====-:.    :%###%=
          -#%###%*=:.        .:=*%###%#-
           .=#%#####%%%%%%%%#####%%#=.
             :=*%%##############%%*=:
               :-=*#%%%%%%%%%%#*=-:
                  .:-==++++==-:.
""".strip("\n").split("\n")

def build():
    lines = from_photo() or FALLBACK
    # normalize width
    maxw = max(len(l) for l in lines)
    cw, ch = 7.2, 12.0
    W = int(maxw * cw + 24)
    H = int(len(lines) * ch + 24)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="Fira Code, Consolas, monospace">']
    out.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>')
    total = 0.9
    per = total / max(1, len(lines))
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = 16 + i * ch
        begin = round(i * per, 3)
        clip = f"clip{i}"
        text = (line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        lw = len(line) * cw
        out.append(f'<defs><clipPath id="{clip}"><rect x="12" y="{y-ch}" width="0" height="{ch+2}">'
                   f'<animate attributeName="width" from="0" to="{lw}" begin="{begin}s" dur="{round(per,3)}s" fill="freeze"/>'
                   f'</rect></clipPath></defs>')
        out.append(f'<text x="12" y="{y}" font-size="11" letter-spacing="0" '
                   f'fill="{FILL}" xml:space="preserve" clip-path="url(#{clip})">{text}</text>')
        # cursor block rides the wipe edge, disappears after
        out.append(f'<rect x="12" y="{y-9}" width="6" height="11" fill="{CURSOR}">'
                   f'<animate attributeName="x" from="12" to="{12+lw}" begin="{begin}s" dur="{round(per,3)}s" fill="freeze"/>'
                   f'<animate attributeName="opacity" from="1" to="0" begin="{round(begin+per,3)}s" dur="0.05s" fill="freeze"/>'
                   f'</rect>')
    out.append('</svg>')
    open("neel-ascii.svg", "w").write("\n".join(out))
    print(f"wrote neel-ascii.svg ({maxw}x{len(lines)})")

if __name__ == "__main__":
    build()
