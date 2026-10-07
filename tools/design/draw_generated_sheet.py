"""Character sheet revision 2: the accepted GENERATED state images (as used in the game) at one scale,
with the collision capsule (r 0.28 m, h 1.70 m, feet at y=0) drawn over each, plus a silhouette row.
Inputs are the in-game cutouts (godot/assets/art/hari/*.png: figure 680 px = 1.75 m, feet 4 px above the bottom)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "godot/assets/art/hari"
OUT = ROOT / "design/character/gen"
STATES = ["idle", "walk", "talk", "phone", "notes", "overhear", "startled", "keys", "whiteout", "relief"]
PX_PER_M = 680 / 1.75
f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
cell, H = 300, 760
sheet = Image.new("RGB", (cell * 5, (H + 40) * 2 + 60), (236, 232, 224)); d = ImageDraw.Draw(sheet)
d.text((16, 14), "Hari: generated state images as used in game (FLUX.2 klein 4B, edited from reference B) + collision capsule r 0.28 m x h 1.70 m", font=f, fill=(30, 30, 40))
sil = Image.new("RGB", (cell * 10 // 2, 340), (128, 128, 132)); ds = ImageDraw.Draw(sil)
for i, s in enumerate(STATES):
    im = Image.open(ART / f"{s}.png").convert("RGBA")
    x0 = (i % 5) * cell + cell // 2; top = 60 + (i // 5) * (H + 40); feet = top + H - 40
    ox = x0 - im.width // 2; oy = feet + 4 - im.height
    sheet.paste(im, (ox, oy), im)
    r, h = 0.28 * PX_PER_M, 1.70 * PX_PER_M
    d.rounded_rectangle([x0 - r, feet - h, x0 + r, feet], radius=r, outline=(225, 30, 50), width=3)
    d.line([(x0 - 120, feet), (x0 + 120, feet)], fill=(60, 60, 60), width=2)
    d.text((x0 - 120, feet + 8), f"{i + 1}. {s.upper()}", font=f, fill=(30, 30, 40))
    a = np.array(im)[..., 3] > 128
    small = Image.fromarray(np.where(a, 0, 255).astype(np.uint8)).resize((int(im.width * 300 / im.height), 300))
    mask = Image.fromarray((np.array(small) < 128).astype(np.uint8) * 255)
    sil.paste((0, 0, 0), (i * 150 + 10, 20), mask)
sheet.save(OUT / "poses-generated.jpg", quality=88)
sil.save(OUT / "silhouette-generated.png")
print("wrote", OUT / "poses-generated.jpg", OUT / "silhouette-generated.png")
