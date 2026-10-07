"""Contact sheet of generation candidates: each shown large and at in-game size (default 300 px tall).

  python tools/gen/contact_sheet.py OUT.jpg gen/raw/CHAR-HARI-REF_*.png [--game-px 300] [--bg 30,35,64]
Committed sheets (JPEG, small) are the record of accepted and rejected outputs.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("images", nargs="+")
    ap.add_argument("--game-px", type=int, default=300)
    ap.add_argument("--big-px", type=int, default=520)
    ap.add_argument("--bg", default="236,232,224", help="background behind the in-game-size copies")
    a = ap.parse_args()
    bg = tuple(int(v) for v in a.bg.split(","))
    ims = [Image.open(p).convert("RGBA") for p in a.images]
    cell_w = max(int(im.width * a.big_px / im.height) for im in ims) + 20
    W, H = cell_w * len(ims), a.big_px + a.game_px + 90
    sheet = Image.new("RGB", (W, H), (24, 24, 28)); d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except OSError:
        f = ImageFont.load_default()
    d.rectangle([0, a.big_px + 40, W, H], fill=bg)
    for i, (p, im) in enumerate(zip(a.images, ims)):
        x = i * cell_w + 10
        big = im.resize((int(im.width * a.big_px / im.height), a.big_px), Image.LANCZOS)
        sheet.paste(big, (x, 10), big)
        d.text((x, a.big_px + 14), f"{chr(65 + i)}  {Path(p).stem}", font=f, fill=(240, 240, 240))
        small = im.resize((int(im.width * a.game_px / im.height), a.game_px), Image.LANCZOS)
        sheet.paste(small, (x + (big.width - small.width) // 2, a.big_px + 60), small)
    d.text((10, H - 24), f"bottom row: real in-game size ({a.game_px} px tall)", font=f, fill=(40, 40, 40))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=82)
    print("wrote", a.out, sheet.size)


if __name__ == "__main__":
    main()
