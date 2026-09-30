"""Turn assets/photo.jpg into two animated ASCII-portrait SVGs (dark + light GitHub themes).

Pipeline: crop -> upscale -> cut-out (rembg, GrabCut fallback) -> bilateral -> CLAHE
          -> darkening curve (v/255)^1.7 -> character ramp -> SMIL typing animation.
"""
import argparse, os
import cv2
import numpy as np
from PIL import Image
from xml.sax.saxutils import escape

COLS = 90
FONT_SIZE = 12.9
CHAR_W = 7.74            # 0.600 em at 12.9px
LINE_H = CHAR_W / 0.48   # monospace cells are ~2x taller than wide
RAMP = " .,:;-=+*#%@"    # blank -> densest
ROW_STAGGER = 0.09
ROW_DUR = 0.9
COLORS = {"dark": "#a78bfa", "light": "#5b21b6"}


def cutout(rgb):
    """Return a 0/1 subject mask."""
    try:
        from rembg import remove
        out = np.array(remove(Image.fromarray(rgb)))
        return (out[..., 3] > 128).astype(np.uint8)
    except Exception as e:  # rembg missing / model unavailable
        print(f"[warn] rembg unavailable ({type(e).__name__}); using GrabCut fallback")
        h, w = rgb.shape[:2]
        mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
        mask[int(h*.05):int(h*.95), int(w*.12):int(w*.88)] = cv2.GC_PR_FGD
        mask[int(h*.25):int(h*.75), int(w*.30):int(w*.70)] = cv2.GC_FGD
        mask[:int(h*.03), :] = cv2.GC_BGD
        bgd, fgd = np.zeros((1, 65)), np.zeros((1, 65))
        cv2.grabCut(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), mask, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
        m = np.isin(mask, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
        return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))


def prepare(path, crop):
    im = Image.open(path).convert("RGB").crop(crop)
    if im.width < 1200:  # upscale so thin features survive the downscale
        s = 1200 / im.width
        im = im.resize((1200, round(im.height * s)), Image.LANCZOS)
    rgb = np.array(im)
    mask = cutout(rgb)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 50, 50)
    gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
    t = (gray / 255.0) ** 1.7            # the darkening curve
    return t, mask


def to_rows(t, mask, theme):
    h, w = t.shape
    rows = round(COLS * (h / w) * 0.48)
    t = cv2.resize(t, (COLS, rows), interpolation=cv2.INTER_AREA)
    m = cv2.resize(mask.astype(np.float32), (COLS, rows), interpolation=cv2.INTER_AREA) > 0.5
    dens = t if theme == "dark" else 1 - t     # dark card: light skin = dense; light card: shadow = dense
    dens = np.where(m, np.clip(dens, 0.15, 1), 0)
    idx = np.clip((dens * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
    return ["".join(RAMP[i] for i in r) for r in idx]


def build_svg(lines, theme):
    W, H = COLS * CHAR_W, len(lines) * LINE_H
    col = COLORS[theme]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-label="ASCII portrait">',
         f'<g font-family="\'DejaVu Sans Mono\',\'Liberation Mono\',Consolas,monospace" font-size="{FONT_SIZE}" fill="{col}" xml:space="preserve">']
    for i, row in enumerate(lines):
        y, begin = i * LINE_H, i * ROW_STAGGER
        txt = row.rstrip()
        if not txt:
            continue
        p.append(f'<clipPath id="c{i}"><rect x="0" y="{y:.2f}" width="0" height="{LINE_H:.2f}">'
                 f'<animate attributeName="width" from="0" to="{W:.1f}" dur="{ROW_DUR}s" begin="{begin:.2f}s" fill="freeze"/></rect></clipPath>')
        # textLength pins the row width, so Windows fonts with a different advance render identically
        p.append(f'<text clip-path="url(#c{i})" x="0" y="{y + LINE_H * 0.78:.2f}" textLength="{len(txt) * CHAR_W:.2f}" lengthAdjust="spacing">{escape(txt)}</text>')
        p.append(f'<rect x="0" y="{y + 2:.2f}" width="{CHAR_W:.2f}" height="{LINE_H - 4:.2f}" fill="{col}" opacity="0">'
                 f'<set attributeName="opacity" to="1" begin="{begin:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="x" from="0" to="{W:.1f}" dur="{ROW_DUR}s" begin="{begin:.2f}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0" begin="{begin + ROW_DUR:.2f}s" fill="freeze"/></rect>')
    p.append("</g></svg>")
    return "\n".join(p)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", default="assets/photo.jpg")
    ap.add_argument("--crop", default="100,50,430,430", help="x0,y0,x1,y1 in original pixels")
    ap.add_argument("--out", default="assets")
    a = ap.parse_args()
    t, mask = prepare(a.photo, tuple(int(v) for v in a.crop.split(",")))
    os.makedirs(a.out, exist_ok=True)
    for theme in ("dark", "light"):
        lines = to_rows(t, mask, theme)
        open(f"{a.out}/portrait-{theme}.svg", "w").write(build_svg(lines, theme))
        if theme == "light":
            open(f"{a.out}/portrait-preview.txt", "w").write("\n".join(lines))
    print(f"done: {len(lines)} rows x {COLS} cols")
