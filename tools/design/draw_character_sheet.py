"""Code-drawn character-sheet SPEC images for Hari (Vidiyum Mun).

Written by Claude as the pre-generation specification: pose list, proportions, silhouette,
collision overlay, palette. These are Pillow drawings, NOT generative-model output. The generated
poses are added later as a revision (CHARACTER-SHEET.md, revision 2).
Run: python tools/design/draw_character_sheet.py  ->  design/character/*.png
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[2] / "design" / "character"
HAND = "/System/Library/Fonts/Noteworthy.ttc"

# ---- Palette (hex, also in CHARACTER-SHEET.md) ----
PAL = {
    "shirt_maroon": "#7A2E3A",
    "shirt_check_cream": "#E8D9B5",
    "jeans_indigo": "#2B3A55",
    "skin": "#8D5A3B",
    "hair": "#1A1412",
    "chappal_blue": "#3E6FB0",
    "outline": "#1B1B2A",
}
ENV = {
    "night sky / sea": "#1C2340",
    "white villa glass (lit)": "#F1E3C8",
    "marble deck (warm lit)": "#EDE6DA",
    "pool water": "#35D0E0",
    "dawn sky": "#F6A6A0",
}

# ---- Proportions (fractions of full height H; Hari = 1.75 m) ----
HEIGHT_M = 1.75
CAPSULE_R_M, CAPSULE_H_M = 0.28, 1.70
HEAD_R, NECK, SHOULDER_Y, SHOULDER_W, HIP_Y, HIP_W = .066, .145, .185, .125, .53, .085
UPPER_ARM, FOREARM, THIGH, SHIN = .19, .17, .245, .235


def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(s):
    try:
        return ImageFont.truetype(HAND, s)
    except OSError:
        return ImageFont.load_default()


def pt(o, L, deg):
    a = math.radians(deg)
    return (o[0] + L * math.sin(a), o[1] + L * math.cos(a))


# pose: torso lean (deg, + = forward), head tilt, arms (back, front) as (upper, fore) angles,
# legs (back, front) as (thigh, shin) angles. 0 = straight down, +90 = forward (facing right).
POSES = {
    "idle":     dict(lean=0, head=0, arms=((-8, -4), (8, 4)), legs=((-3, -3), (3, 3)), note="held"),
    "walk":     dict(lean=4, head=0, arms=((22, 40), (-24, -10)), legs=((-22, -30), (24, 8)), note="held while moving"),
    "talk":     dict(lean=3, head=4, arms=((-6, -2), (40, 95)), legs=((-4, -4), (6, 6)), note="held in dialogue"),
    "phone":    dict(lean=0, head=-6, arms=((-8, -4), (35, 165)), legs=((-3, -3), (5, 5)), note="held during call"),
    "notes":    dict(lean=6, head=22, arms=((10, 85), (18, 95)), legs=((-3, -3), (3, 3)), note="held ~1.5 s (clue)"),
    "overhear": dict(lean=-6, head=-10, arms=((-15, -30), (20, 150)), legs=((-8, -8), (6, 6)), note="held while listening"),
    "startled": dict(lean=-8, head=-8, arms=((-35, -70), (25, 120)), legs=((-10, -6), (8, 4)), note="held ~1.2 s (loop start)"),
    "keys":     dict(lean=2, head=-4, arms=((-6, -2), (120, 160)), legs=((-4, -4), (5, 5)), note="held ~1.5 s"),
    "whiteout": dict(lean=-12, head=-14, arms=((-20, -40), (110, 200)), legs=((-14, -10), (10, 6)), note="held to white"),
    "relief":   dict(lean=0, head=-18, arms=((155, 215), (160, 220)), legs=((-5, -5), (5, 5)), note="held at end"),
}
STATE_ID = {k: k.upper() for k in POSES}


def draw_hari(d, x, feet, H, pose, face=1, solid=None, check=True, view="34"):
    """Draw Hari at full height H px, feet at y=feet, facing right (face=1)."""
    p = POSES[pose]
    O = hexrgb(PAL["outline"]) if not solid else solid
    c = (lambda k: solid) if solid else (lambda k: hexrgb(PAL[k]))
    ow = max(2, int(H * .012))
    hip = (x, feet - H * (1 - HIP_Y))
    sh_c = pt(hip, H * (HIP_Y - SHOULDER_Y), 180 + p["lean"] * face)
    neck = pt(sh_c, H * .04, 180 + p["lean"] * face)
    head_c = pt(neck, H * (NECK - HEAD_R - .03) + H * HEAD_R, 180 + (p["lean"] + p["head"]) * face)
    sw, hw = H * SHOULDER_W, H * HIP_W
    if view == "side":
        sw, hw = sw * .45, hw * .55
    shL, shR = (sh_c[0] - sw * .55, sh_c[1]), (sh_c[0] + sw * .45, sh_c[1])
    hipL, hipR = (hip[0] - hw * .5, hip[1]), (hip[0] + hw * .5, hip[1])

    def limb(o, a1, a2, L1, L2, w, col, shoe=False):
        a1, a2 = a1 * face, a2 * face
        m = pt(o, H * L1, a1); e = pt(m, H * L2, a2)
        d.line([o, m, e], fill=O, width=int(w + ow * 2), joint="curve")
        d.line([o, m, e], fill=col, width=int(w), joint="curve")
        for q in (o, m):
            d.ellipse([q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2], fill=col)
        if shoe:
            d.ellipse([e[0] - H * .045 + face * H * .02, e[1] - H * .012, e[0] + H * .045 + face * H * .02, e[1] + H * .014],
                      fill=c("chappal_blue"), outline=O, width=ow)
        return m, e

    # back limbs first
    limb(hipL, *POSES[pose]["legs"][0], THIGH, SHIN, H * .062, c("jeans_indigo"), shoe=True)
    limb(shL, *p["arms"][0], UPPER_ARM, FOREARM, H * .042, c("skin"))
    # torso (shirt)
    torso = [shL, shR, hipR, hipL]
    d.polygon(torso, fill=c("shirt_maroon"), outline=O, width=ow)
    if check and not solid:
        for i in range(1, 7):
            t = i / 7
            a = (shL[0] + (shR[0] - shL[0]) * t, shL[1])
            b = (hipL[0] + (hipR[0] - hipL[0]) * t, hipL[1])
            d.line([a, b], fill=c("shirt_check_cream"), width=max(1, ow // 2))
        for j in range(1, 7):
            t = j / 7
            a = (shL[0] + (hipL[0] - shL[0]) * t, shL[1] + (hipL[1] - shL[1]) * t)
            b = (shR[0] + (hipR[0] - shR[0]) * t, shR[1] + (hipR[1] - shR[1]) * t)
            d.line([a, b], fill=c("shirt_check_cream"), width=max(1, ow // 2))
        d.polygon(torso, outline=O, width=ow)
    limb(hipR, *p["legs"][1], THIGH, SHIN, H * .064, c("jeans_indigo"), shoe=True)
    # front arm with half sleeve
    m, e = limb(shR, *p["arms"][1], UPPER_ARM, FOREARM, H * .044, c("skin"))
    sl = ((shR[0] + m[0]) / 2, (shR[1] + m[1]) / 2)
    d.line([shR, sl], fill=O, width=int(H * .06 + ow * 2)); d.line([shR, sl], fill=c("shirt_maroon"), width=int(H * .06))
    # props
    if pose in ("phone", "notes") and not solid:
        d.rectangle([e[0] - H * .012, e[1] - H * .03, e[0] + H * .012, e[1] + H * .01], fill=(20, 20, 24), outline=O)
    if pose == "keys" and not solid:
        d.ellipse([e[0] - H * .02, e[1] - H * .05, e[0] + H * .02, e[1] - H * .01], outline=(240, 190, 80), width=ow)
    # head
    r = H * HEAD_R
    d.ellipse([head_c[0] - r, head_c[1] - r, head_c[0] + r, head_c[1] + r], fill=c("skin"), outline=O, width=ow)
    d.chord([head_c[0] - r * 1.05, head_c[1] - r * 1.15, head_c[0] + r * 1.05, head_c[1] + r * .5], 170, 370, fill=c("hair"))
    if not solid and view != "back":
        ex = head_c[0] + face * r * (.35 if view == "34" else .55 if view == "side" else 0)
        for dx in ((-.28, .28) if view == "front" else (-.22, .2) if view == "34" else (0,)):
            d.ellipse([ex + dx * r - r * .09, head_c[1] - r * .02, ex + dx * r + r * .09, head_c[1] + r * .16], fill=O)
    if view == "back" and not solid:
        d.chord([head_c[0] - r * 1.05, head_c[1] - r * 1.15, head_c[0] + r * 1.05, head_c[1] + r * .9], 0, 360, fill=c("hair"))
    return hip


def capsule(d, x, feet, H, col=(230, 40, 60)):
    ppm = H / HEIGHT_M
    r, h = CAPSULE_R_M * ppm, CAPSULE_H_M * ppm
    top, bot = feet - h, feet
    d.rounded_rectangle([x - r, top, x + r, bot], radius=r, outline=col, width=3)


def lum(rgb):
    def ch(v):
        v /= 255; return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb); return .2126 * r + .7152 * g + .0722 * b


def contrast(a, b):
    la, lb = sorted((lum(hexrgb(a)), lum(hexrgb(b))), reverse=True); return (la + .05) / (lb + .05)


def sheet_poses():
    H = 380; cols = 5; cw, ch = 300, 520
    im = Image.new("RGB", (cw * cols, ch * 2 + 60), (246, 243, 236)); d = ImageDraw.Draw(im)
    d.text((20, 10), "Hari: 10 in-game state poses (SPEC sketches, code-drawn; 3/4 view facing right; left = runtime flip)", font=font(26), fill=(30, 30, 40))
    for i, k in enumerate(POSES):
        cx, top = (i % cols) * cw + cw // 2, 60 + (i // cols) * ch
        draw_hari(d, cx, top + 450, H, k)
        d.text((cx - 120, top + 462), f"{i + 1}. {STATE_ID[k]}", font=font(26), fill=(30, 30, 40))
        d.text((cx - 120, top + 492), POSES[k]["note"], font=font(18), fill=(110, 110, 120))
    return im


def sheet_collision():
    H = 380; cols = 5; cw, ch = 300, 500
    im = Image.new("RGB", (cw * cols, ch * 2 + 60), (246, 243, 236)); d = ImageDraw.Draw(im)
    d.text((20, 10), "Collision overlay: CapsuleShape3D r = 0.28 m, h = 1.70 m (red), feet at y = 0; same scale as poses", font=font(26), fill=(30, 30, 40))
    for i, k in enumerate(POSES):
        cx, top = (i % cols) * cw + cw // 2, 60 + (i // cols) * ch
        draw_hari(d, cx, top + 440, H, k); capsule(d, cx, top + 440, H)
        d.text((cx - 60, top + 452), STATE_ID[k], font=font(22), fill=(30, 30, 40))
    return im


def sheet_silhouette():
    im = Image.new("RGB", (1280, 720), (128, 128, 132)); d = ImageDraw.Draw(im)
    d.text((20, 10), "Silhouette test at real on-screen size in a 1280x720 viewport (solid black)", font=font(26), fill=(255, 255, 255))
    d.text((20, 46), "deck framing: 300 px tall (camera 4.5 m, 50° vertical FOV)  ·  gate framing: 208 px (6.5 m)", font=font(20), fill=(235, 235, 240))
    x = 90
    for k in ("idle", "walk", "talk", "phone", "keys", "whiteout", "relief"):
        draw_hari(d, x, 430, 300, k, solid=(0, 0, 0)); x += 165
    x = 90
    for k in ("idle", "walk", "talk", "phone", "keys", "whiteout", "relief"):
        draw_hari(d, x, 690, 208, k, solid=(0, 0, 0)); x += 165
    return im


def sheet_turnaround():
    H = 520
    im = Image.new("RGB", (1280, 700), (246, 243, 236)); d = ImageDraw.Draw(im)
    d.text((20, 10), "Reference turnaround: front · three-quarter · side · back, same height (SPEC; the generated reference must match)", font=font(24), fill=(30, 30, 40))
    feet = 640
    for i, (v, x) in enumerate((("front", 260), ("34", 520), ("side", 780), ("back", 1040))):
        draw_hari(d, x, feet, H, "idle", view=v)
        d.text((x - 50, feet + 12), {"front": "front", "34": "3/4 (game)", "side": "side", "back": "back"}[v], font=font(22), fill=(30, 30, 40))
    # height bar
    d.line([(90, feet), (90, feet - H)], fill=(30, 30, 40), width=3)
    for m in (0, .5, 1.0, 1.5, 1.75):
        y = feet - H * m / HEIGHT_M
        d.line([(80, y), (100, y)], fill=(30, 30, 40), width=3); d.text((20, y - 14), f"{m:.2f} m", font=font(18), fill=(30, 30, 40))
    for y in (feet - H, feet - H * (1 - HIP_Y), feet - H * (1 - SHOULDER_Y)):
        d.line([(120, y), (1200, y)], fill=(200, 160, 160), width=1)
    d.text((1120, feet - H - 24), "top of hair", font=font(16), fill=(150, 90, 90))
    return im


def sheet_palette():
    im = Image.new("RGB", (1280, 560), (246, 243, 236)); d = ImageDraw.Draw(im)
    d.text((20, 10), "Palette (Hari) and contrast against the environment (WCAG contrast ratio)", font=font(26), fill=(30, 30, 40))
    for i, (k, v) in enumerate(PAL.items()):
        x = 20 + i * 178
        d.rectangle([x, 60, x + 160, 160], fill=hexrgb(v), outline=(30, 30, 40))
        d.text((x, 166), k.replace("_", " "), font=font(17), fill=(30, 30, 40)); d.text((x, 190), v, font=font(17), fill=(30, 30, 40))
    y = 240
    d.text((20, y), "environment:", font=font(20), fill=(30, 30, 40))
    keys = ["shirt_maroon", "shirt_check_cream", "skin", "jeans_indigo"]
    for j, k in enumerate(keys):
        d.text((330 + j * 230, y), k.replace("_", " "), font=font(18), fill=(30, 30, 40))
    for i, (en, ev) in enumerate(ENV.items()):
        yy = y + 40 + i * 50
        d.rectangle([20, yy, 60, yy + 36], fill=hexrgb(ev), outline=(30, 30, 40)); d.text((70, yy + 6), f"{en} {ev}", font=font(18), fill=(30, 30, 40))
        for j, k in enumerate(keys):
            r = contrast(PAL[k], ev)
            d.text((330 + j * 230, yy + 6), f"{r:4.1f}:1", font=font(20), fill=(30, 120, 60) if r >= 3 else (190, 60, 40))
    d.text((20, 520), "Rule: on every background, at least one large shirt colour must reach 3:1 (the check pattern carries both a dark and a light value, plus the dark outline).", font=font(17), fill=(80, 80, 90))
    return im


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("poses", sheet_poses), ("collision", sheet_collision), ("silhouette", sheet_silhouette),
                     ("turnaround", sheet_turnaround), ("palette", sheet_palette)):
        fn().save(OUT / f"{name}-spec.png"); print("wrote", name)
    print("contrast table:")
    for en, ev in ENV.items():
        print(f"  {en:26s}", "  ".join(f"{k}={contrast(v, ev):.1f}" for k, v in PAL.items() if k in ("shirt_maroon", "shirt_check_cream", "skin")))
