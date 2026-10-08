"""TEST-REPORT comparison boards: (1) each storyboard panel beside its in-engine screenshot,
(2) each Hari state: character-sheet spec pose | accepted generated image | in engine facing right | facing left."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[2]
SB, SH, OUT = ROOT / "design/storyboard", ROOT / "evidence/shots", ROOT / "evidence/comparisons"
OUT.mkdir(parents=True, exist_ok=True)
f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22); fs = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 17)
PAIRS = [("01-title", "intro_title", "design view: title (intro still), not the 3D scene"), ("02-amma-call", "p02_amma_call", "matches"),
         ("03-talk-manikandan", "p03_talk_manikandan", "not over-the-shoulder (follow camera)"), ("04-clue-saved", "p04_clue_saved", "no close-up shot; the HUD notes card is the close-up"),
         ("05-keys-taken", "p05_keys_taken", "not a low angle; Advay's line is a caption"), ("06-dawn-failure", "p06_whiteout", "no Dutch tilt; shake + white-out"),
         ("07-loop2-wake", "p07_loop2_wake", "no push-in; shock lines added (rev 2)"), ("08-keys-stay", "p08_keys_stay", "matches"),
         ("09-end-card", "p09_end_card", "not a low angle; railing view + end card")]
W, H = 640, 360
board = Image.new("RGB", (W * 2 + 30, (H + 50) * len(PAIRS) + 60), (24, 24, 28)); d = ImageDraw.Draw(board)
d.text((10, 14), "Storyboard panel (left, code-drawn spec)  vs  in-engine screenshot at 13f772c (right, scripted capture)", font=f, fill=(240, 240, 240))
for i, (a, b, note) in enumerate(PAIRS):
    y = 60 + i * (H + 50)
    board.paste(Image.open(SB / f"{a}.png").convert("RGB").resize((W, H)), (10, y))
    board.paste(Image.open(SH / f"{b}.jpg").convert("RGB").resize((W, H)), (W + 20, y))
    d.text((10, y + H + 6), f"Panel {a}  ->  {b}.jpg   |   {note}", font=fs, fill=(230, 210, 150))
board.save(OUT / "storyboard-vs-slice.jpg", quality=85)
STATES = ["idle", "walk", "talk", "phone", "notes", "overhear", "startled", "keys", "whiteout", "relief"]
spec = Image.open(ROOT / "design/character/poses-spec.png").convert("RGB")
cw, ch = spec.width // 5, (spec.height - 60) // 2
cell = 230
sheet = Image.new("RGB", (cell * 4 + 50, (cell + 40) * len(STATES) + 70), (236, 232, 224)); d = ImageDraw.Draw(sheet)
d.text((10, 12), "State: sheet spec | generated image (in game) | in engine facing right | facing left (flip_h)", font=f, fill=(30, 30, 40))
for i, s in enumerate(STATES):
    y = 60 + i * (cell + 40)
    sp = spec.crop(((i % 5) * cw, 60 + (i // 5) * ch, (i % 5 + 1) * cw, 60 + (i // 5 + 1) * ch - 60)); sp.thumbnail((cell, cell)); sheet.paste(sp, (10, y))
    g = Image.open(ROOT / f"godot/assets/art/hari/{s}.png").convert("RGBA"); g.thumbnail((cell, cell)); bgc = Image.new("RGB", g.size, (200, 200, 205)); bgc.paste(g, (0, 0), g); sheet.paste(bgc, (cell + 20, y))
    for j, side in enumerate(("right", "left")):
        e = Image.open(SH / f"state_{s}_{side}.jpg").convert("RGB"); e = e.crop((e.width // 2 - 260, 60, e.width // 2 + 260, e.height - 40)); e.thumbnail((cell, cell)); sheet.paste(e, (2 * cell + 30 + j * (cell + 10), y))
    d.text((10, y + cell + 6), f"{i + 1}. {s.upper()}", font=fs, fill=(30, 30, 40))
sheet.save(OUT / "character-sheet-vs-engine.jpg", quality=85)
print("wrote", OUT)
