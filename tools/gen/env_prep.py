"""Prepare environment textures from accepted raw generations; every edit is logged to gen/edit_log.jsonl.
  python tools/gen/env_prep.py villa|beach|marble|fire SRC DEST"""
import json, sys
from datetime import datetime
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageOps
ROOT = Path(__file__).resolve().parents[2]
kind, src, dest = sys.argv[1:4]
im = Image.open(src).convert("RGB"); edits = []
if kind == "villa":
    edits.append("no change (opaque night sky kept; shown as backdrop quad)")
elif kind == "beach":
    im = ImageOps.mirror(im); edits.append("mirrored horizontally so the village/fence side sits toward +x (the railing end of the deck)")
elif kind == "marble":
    d = ImageDraw.Draw(im); w, h = im.size
    for x in (0, w - 1):
        d.line([(x, 0), (x, h)], fill=(165, 165, 168), width=3)
    for y in (0, h - 1):
        d.line([(0, y), (w, y)], fill=(165, 165, 168), width=3)
    edits.append("drew 3px grey grout lines on all four edges so the 2x2 tile pattern repeats seamlessly")
elif kind == "fire":
    a = np.asarray(im).astype(np.float32)
    alpha = np.clip(a.max(axis=2) * 1.6, 0, 255).astype(np.uint8)
    im = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")
    edits.append("black background converted to transparency (alpha = 1.6 x max RGB), keeping the glow")
Path(dest).parent.mkdir(parents=True, exist_ok=True); im.save(dest)
with (ROOT / "gen/edit_log.jsonl").open("a") as f:
    f.write(json.dumps({"time": datetime.now().isoformat(timespec="seconds"), "src": src, "dest": dest, "edits": edits}) + "\n")
print("wrote", dest, im.size, edits)
