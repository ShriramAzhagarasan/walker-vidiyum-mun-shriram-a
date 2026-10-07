"""Background removal plus trim and scale for character/prop sprites, with an edit log.

  python tools/gen/cutout.py SRC.png DEST.png [--model isnet-anime] [--height 680] [--feet-pad 4]
Steps (each recorded in gen/edit_log.jsonl):
  1. rembg background removal (model selectable), alpha matting off by default
  2. alpha cleanup: alpha < 16 -> 0 (kills grey haze), keep the largest connected blob region
  3. trim to the alpha bounding box, scale to --height px tall (LANCZOS), pad with transparent margin
     so the feet sit --feet-pad px above the bottom edge (Godot anchors the sprite at its feet)
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image
from rembg import new_session, remove

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "gen" / "edit_log.jsonl"


def largest_component(mask):
    from collections import deque
    h, w = mask.shape; seen = np.zeros_like(mask, bool); best = None; best_n = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys[::997], xs[::997]):  # seed sampling is enough for a single figure
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)]); seen[y0, x0] = True; comp = []
        while q:
            y, x = q.popleft(); comp.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
        if len(comp) > best_n:
            best_n, best = len(comp), comp
    keep = np.zeros_like(mask, bool)
    if best:
        yy, xx = zip(*best); keep[list(yy), list(xx)] = True
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dest")
    ap.add_argument("--model", default="isnet-anime")
    ap.add_argument("--height", type=int, default=680)
    ap.add_argument("--feet-pad", type=int, default=4)
    ap.add_argument("--keep-all", action="store_true", help="skip largest-component filter (props with gaps)")
    a = ap.parse_args()
    src = Image.open(a.src).convert("RGB")
    cut = remove(src, session=new_session(a.model))
    arr = np.array(cut)
    alpha = arr[..., 3]
    alpha[alpha < 16] = 0
    if not a.keep_all:
        alpha[~largest_component(alpha > 0)] = 0
    arr[..., 3] = alpha
    im = Image.fromarray(arr)
    bbox = im.getbbox(); im = im.crop(bbox)
    scale = a.height / im.height
    im = im.resize((max(1, round(im.width * scale)), a.height), Image.LANCZOS)
    pad = 8
    out = Image.new("RGBA", (im.width + pad * 2, im.height + pad + a.feet_pad), (0, 0, 0, 0))
    out.paste(im, (pad, pad), im)
    Path(a.dest).parent.mkdir(parents=True, exist_ok=True)
    out.save(a.dest)
    row = {"time": datetime.now().isoformat(timespec="seconds"), "src": a.src, "dest": a.dest,
           "edits": [f"rembg background removal ({a.model})", "alpha<16 -> 0",
                     "kept largest connected region" if not a.keep_all else "kept all regions",
                     f"trimmed to bbox {bbox}", f"scaled to {a.height}px tall (LANCZOS)",
                     f"padded {pad}px, feet {a.feet_pad}px above bottom"]}
    with LOG.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print("wrote", a.dest, out.size)


if __name__ == "__main__":
    main()
