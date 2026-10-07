"""Code-drawn storyboard thumbnails for Vidiyum Mun (16:9, 1280x720).

Written by Claude from Shriram's storyboard idea (design/input/STORY-BIBLE-v1.md, section 13).
These are design sketches drawn with Pillow primitives, NOT generative-model output.
Run: python tools/design/draw_storyboard.py  ->  design/storyboard/NN-*.png + contact.png
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = Path(__file__).resolve().parents[2] / "design" / "storyboard"
PAPER = (244, 241, 234)
INK = (40, 40, 48)
SOFT = (150, 150, 160)
CYAN = (60, 190, 210)
WARM = (245, 175, 80)
FIRE = (240, 110, 40)
DAWN = (240, 160, 150)
NIGHT = (52, 60, 92)
HAND = "/System/Library/Fonts/Noteworthy.ttc"
UNI = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def font(size, path=HAND):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def jline(d, pts, w=3, col=INK, passes=2, jit=1.6, seed=None):
    """Sketchy polyline: draw it twice with small jitter."""
    rnd = random.Random(seed if seed is not None else hash(tuple(pts)) & 0xFFFF)
    for _ in range(passes):
        q = [(x + rnd.uniform(-jit, jit), y + rnd.uniform(-jit, jit)) for x, y in pts]
        d.line(q, fill=col, width=w, joint="curve")


def jrect(d, x0, y0, x1, y1, **k):
    jline(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], **k)


def jcircle(d, cx, cy, r, w=3, col=INK, fill=None):
    if fill:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    pts = [(cx + r * math.cos(t / 20 * 2 * math.pi), cy + r * math.sin(t / 20 * 2 * math.pi)) for t in range(21)]
    jline(d, pts, w=w, col=col)


def hatch(d, x0, y0, x1, y1, col=SOFT, step=10, w=1):
    for i in range(int(x0) - int(y1 - y0), int(x1), step):
        a = (max(i, x0), y1 - max(0, max(i, x0) - i))
        b = (min(i + (y1 - y0), x1), y1 - (min(i + (y1 - y0), x1) - i))
        d.line([a, b], fill=col, width=w)


def figure(d, x, feet, h, pose="idle", face=1, col=INK, label=None, shirt=None):
    """Simple mannequin. h = full height in px. face = +1 right, -1 left."""
    head_r = h * 0.075
    neck = feet - h + head_r * 2
    hip = feet - h * 0.47
    sh = neck + h * 0.05
    hx = x + (h * 0.02 * face if pose in ("talk", "keys") else 0)
    jcircle(d, hx, feet - h + head_r, head_r, w=3, col=col)
    if shirt:
        d.polygon([(x - h * .11, sh), (x + h * .11, sh), (x + h * .09, hip), (x - h * .09, hip)], fill=shirt)
    jline(d, [(x - h * .11, sh), (x + h * .11, sh), (x + h * .09, hip), (x - h * .09, hip), (x - h * .11, sh)], col=col)
    # legs
    stride = {"walk": .16, "relief": .05}.get(pose, .05)
    jline(d, [(x - h * .05, hip), (x - h * stride * face, feet)], col=col)
    jline(d, [(x + h * .05, hip), (x + h * stride * face * (1 if pose == "walk" else 1), feet)], col=col)
    # arms by pose: (end offsets relative to shoulder, in units of h)
    arms = {
        "idle": [(-.13, .30), (.13, .30)],
        "walk": [(-.10 * face, .28), (.14 * face, .26)],
        "talk": [(-.12, .30), (.24 * face, .10)],
        "phone": [(-.12, .30), (.05 * face, -.02)],
        "notes": [(.06 * face, .18), (.12 * face, .18)],
        "startled": [(-.20, .02), (.08 * face, .12)],
        "keys": [(-.12, .30), (.20 * face, -.06)],
        "shield": [(.10 * face, -.10), (-.14, .26)],
        "relief": [(-.06, -.08), (.06, -.08)],
        "overhear": [(-.08 * face, .22), (.10 * face, .05)],
        "speaker": [(-.12, .30), (.18 * face, .02)],
        "lean": [(-.16 * face, .22), (.12, .30)],
    }[pose]
    for i, (ax, ay) in enumerate(arms):
        sx = x + (-h * .11 if i == 0 else h * .11)
        jline(d, [(sx, sh), (x + ax * h, sh + ay * h)], col=col)
    if pose == "phone":
        jrect(d, hx + face * head_r * .7, feet - h + head_r * .6, hx + face * head_r * 1.3, feet - h + head_r * 1.8, w=2)
    if pose == "keys":
        kx, ky = x + .20 * face * h, sh - .06 * h
        jcircle(d, kx, ky - 6, 6, w=2, col=WARM)
    if pose == "speaker":
        jrect(d, x + .16 * face * h, sh - .02 * h, x + .26 * face * h, sh + .06 * h, w=2)
    if label:
        d.text((x - 40, feet + 6), label, font=font(20), fill=col)


def deck_perspective(d, horizon=300, vp=(640, 300), col=SOFT):
    for x in range(-600, 1900, 160):
        jline(d, [(x, H - 90), (vp[0] + (x - vp[0]) * 0.18, horizon + 60)], w=1, col=col, passes=1)
    for i, y in enumerate([H - 90, 560, 470, 420]):
        jline(d, [(0, y), (W, y)], w=1, col=col, passes=1)


def string_lights(d, y0=120, sag=40, x0=40, x1=1240):
    pts = [(x, y0 + sag * math.sin((x - x0) / (x1 - x0) * math.pi)) for x in range(x0, x1 + 1, 40)]
    jline(d, pts, w=2, col=SOFT, passes=1)
    for (x, y) in pts[1:-1:2]:
        d.ellipse([x - 6, y - 2, x + 6, y + 10], fill=WARM)


def caption(img, n, title, shot, view, note):
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 64, W, H], fill=(28, 28, 34))
    d.text((18, H - 56), f"{n:02d}  {title}", font=font(28), fill=(250, 250, 250))
    d.text((18, H - 24), f"{shot}  ·  {view}", font=font(17), fill=(200, 200, 210))
    if note:
        d.text((W - 18 - d.textlength(note, font=font(17)), H - 24), note, font=font(17), fill=WARM)
    jrect(d, 4, 4, W - 4, H - 4, w=3)


def hud_clock(d, text, x=24, y=20):
    d.rounded_rectangle([x, y, x + 150, y + 40], 10, fill=(30, 30, 40))
    d.text((x + 14, y + 4), text, font=font(24), fill=(255, 255, 255))


def panel_01():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 250], fill=(222, 224, 236))
    # sea band + coastline seen from above
    d.polygon([(0, 250), (W, 250), (W, 330), (0, 360)], fill=(205, 220, 232))
    jline(d, [(0, 360), (300, 345), (700, 335), (1280, 330)], w=2)
    # ECR road (top of frame = inland is bottom here; road at bottom)
    jline(d, [(0, 600), (1280, 560)], w=4); jline(d, [(0, 630), (1280, 590)], w=4)
    d.text((1010, 600), "ECR (sound only)", font=font(20), fill=INK)
    # villa block + pool deck
    jrect(d, 360, 420, 640, 540, w=3); hatch(d, 362, 422, 638, 538, col=(205, 205, 210))
    d.text((420, 470), "glass villa", font=font(22), fill=INK)
    jrect(d, 360, 370, 700, 420, w=2); d.rectangle([420, 380, 560, 410], fill=CYAN)
    d.text((585, 380), "deck", font=font(18), fill=INK)
    # private beach + rock + fence
    jcircle(d, 520, 330, 14, fill=(120, 110, 100)); d.text((475, 290), "the rock", font=font(18), fill=INK)
    jline(d, [(760, 300), (770, 560)], w=3); d.text((780, 470), "old fence", font=font(18), fill=INK)
    for i in range(8):
        jline(d, [(760 + i * 1.3, 300 + i * 32), (770, 300 + i * 32)], w=1)
    # village side: boats + fire
    for bx in (880, 960, 1060):
        jline(d, [(bx, 320), (bx + 50, 316), (bx + 44, 330), (bx + 6, 332), (bx, 320)], w=2)
    d.ellipse([1130, 300, 1170, 340], fill=FIRE); d.text((1110, 345), "village fire", font=font(18), fill=INK)
    # camera push-in note
    jline(d, [(150, 180), (330, 330)], w=2, col=SOFT); d.polygon([(330, 330), (312, 322), (322, 312)], fill=SOFT)
    d.text((60, 140), "slow push-in", font=font(20), fill=SOFT)
    d.text((W // 2 - 150, 40), "VIDIYUM MUN", font=font(54), fill=NIGHT)
    d.text((W // 2 - 120, 120), "(Before Dawn)", font=font(34), fill=NIGHT)
    caption(img, 1, "Title: the last night on 'their' beach", "WIDE · BIRD'S-EYE", "DESIGN VIEW (title)", "push-in")
    return img


def panel_02():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 300], fill=(214, 216, 232))
    jrect(d, 60, 60, 760, 300, w=3)  # villa glass
    for x in range(60, 760, 100):
        jline(d, [(x, 60), (x, 300)], w=2)
        d.rectangle([x + 8, 70, x + 92, 290], fill=(250, 226, 180))
    string_lights(d, 40, 30)
    deck_perspective(d)
    d.polygon([(820, 430), (1240, 430), (1280, 520), (780, 520)], fill=CYAN)
    figure(d, 560, 600, 330, "phone", 1, shirt=(160, 70, 80))
    hud_clock(d, "8:00 PM")
    d.rounded_rectangle([900, 40, 1250, 140], 14, fill=(30, 30, 40))
    d.text((920, 52), "Amma calling…", font=font(30), fill=(255, 255, 255))
    d.text((920, 96), "(phone buzzes)", font=font(20), fill=WARM)
    caption(img, 2, "8:00 PM: Amma's call, the loop begins", "MEDIUM · EYE LEVEL", "GAMEPLAY VIEW", "SFX phone_buzz")
    return img


def panel_03():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 360], fill=(200, 204, 224))
    # SUV and Manikandan, seen over Hari's shoulder
    jline(d, [(620, 470), (660, 330), (980, 320), (1100, 400), (1160, 470), (620, 470)], w=4)
    jcircle(d, 720, 480, 34); jcircle(d, 1060, 480, 34)
    figure(d, 900, 600, 300, "lean", -1, label="Manikandan")
    # Hari's back/shoulder, big in the foreground (left)
    d.ellipse([60, 260, 300, 500], fill=(70, 70, 82))
    d.polygon([(0, 720), (0, 520), (120, 450), (380, 450), (470, 720)], fill=(160, 70, 80))
    jline(d, [(0, 520), (120, 450), (380, 450), (470, 720)], w=4)
    d.rounded_rectangle([960, 150, 1180, 200], 10, fill=(30, 30, 40))
    d.text((978, 158), "E — Talk", font=font(26), fill=(255, 255, 255))
    jline(d, [(500, 640), (640, 600)], w=2, col=SOFT); d.polygon([(640, 600), (622, 597), (630, 612)], fill=SOFT)
    caption(img, 3, "Core action: talk to the people no one talks to", "MEDIUM · OVER-THE-SHOULDER", "GAMEPLAY VIEW (gate framing)", "party music quieter")
    return img


def panel_04():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=(205, 200, 190))
    hatch(d, 0, 0, W, H, col=(190, 185, 176), step=16)
    # marble floor seen from above, chappal feet, hand holding phone
    d.ellipse([300, 520, 420, 600], fill=(70, 120, 190)); d.ellipse([460, 530, 580, 610], fill=(70, 120, 190))
    d.text((300, 610), "rubber chappals", font=font(20), fill=INK)
    d.polygon([(740, 720), (700, 470), (820, 430), (900, 720)], fill=(141, 90, 59))
    d.rounded_rectangle([540, 120, 860, 560], 30, fill=(25, 25, 30))
    d.rounded_rectangle([556, 140, 844, 540], 20, fill=(250, 248, 240))
    jline(d, [(600, 150), (700, 260), (690, 330)], w=1, col=SOFT)  # crack
    d.text((580, 160), "Notes", font=font(30), fill=INK)
    d.text((580, 220), "Mani anna's nephew", font=font(24), fill=INK)
    d.text((580, 252), "= Selvam. From the", font=font(24), fill=INK)
    d.text((580, 284), "village. Scared about", font=font(24), fill=INK)
    d.text((580, 316), "tonight.", font=font(24), fill=INK)
    d.text((580, 480), "saved  1:31 AM", font=font(22), fill=(40, 140, 80))
    caption(img, 4, "Success: a clue saved to Hari's phone", "CLOSE-UP · HIGH ANGLE (looking down)", "UI / DESIGN VIEW", "SFX clue_saved")
    return img


def panel_05():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 420], fill=(40, 46, 74))
    string_lights(d, 60, 20)
    # low angle: big wheel arch foreground, Advay towering
    d.ellipse([-120, 470, 260, 850], fill=(30, 30, 36))
    figure(d, 640, 640, 470, "speaker", -1, col=(250, 250, 250), label="")
    d.text((600, 650), "Advay", font=font(24), fill=INK)
    figure(d, 980, 640, 380, "idle", -1, col=(220, 220, 230))
    d.text((920, 650), "Manikandan", font=font(24), fill=INK)
    # keys arc
    jline(d, [(930, 330), (820, 250), (720, 300)], w=3, col=WARM)
    d.polygon([(720, 300), (742, 296), (732, 282)], fill=WARM)
    d.text((760, 205), "keys", font=font(26), fill=WARM)
    d.rounded_rectangle([300, 450, 980, 520], 10, fill=(30, 30, 40))
    d.text((320, 462), "\"Keys kudunga anna. Morning naane drive pannikaren, bro.\"", font=font(22), fill=(255, 255, 255))
    hud_clock(d, "1:40 AM")
    caption(img, 5, "1:40 AM: Advay takes the keys", "MEDIUM-WIDE · LOW ANGLE", "GAMEPLAY VIEW (scripted moment)", "SFX keys_exchanged")
    return img


def panel_06():
    img = Image.new("RGB", (W, H), PAPER).rotate(0)
    d = ImageDraw.Draw(img)
    base = Image.new("RGB", (W + 400, H + 400), PAPER); b = ImageDraw.Draw(base)
    for i in range(H + 400):
        t = i / (H + 400)
        col = tuple(int(DAWN[k] * (1 - t) + (250, 240, 230)[k] * t) for k in range(3))
        b.line([(0, i), (W + 400, i)], fill=col)
    b.rectangle([0, 560, W + 400, H + 400], fill=(225, 215, 200))
    figure(b, 700, 760, 230, "shield", 1)
    for a in (-0.35, -0.2, -0.05):  # headlight sweep from the road side
        b.line([(W + 380, 300), (700 - 900 * math.cos(a), 420 + 900 * math.sin(a))], fill=(255, 250, 220), width=26)
    base = base.rotate(-9, resample=Image.BICUBIC)
    img.paste(base.crop((200, 200, 200 + W, 200 + H)))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], outline=(255, 255, 255), width=40)
    d.text((70, 70), "HORN… brake screech…", font=font(34), fill=INK)
    d.text((70, 120), "camera shake, then white-out", font=font(24), fill=INK)
    hud_clock(d, "5:52 AM", 1080, 20)
    caption(img, 6, "Failure: dawn on ECR (the crash is never shown)", "WIDE · DUTCH (tilted)", "GAMEPLAY VIEW", "SFX dawn_crash · music stops")
    return img


def panel_07():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    hatch(d, 0, 0, W, H, col=(220, 215, 205), step=22)
    # high angle close-up: head and shoulders from above, hand on damp shirt
    d.polygon([(330, 720), (380, 470), (900, 470), (950, 720)], fill=(160, 70, 80))
    for x in range(380, 900, 40):
        jline(d, [(x, 470), (x - 20, 720)], w=1, col=(230, 210, 180), passes=1)
    jcircle(d, 640, 330, 130, fill=(141, 90, 59)); d.chord([510, 190, 770, 330], 180, 360, fill=(26, 20, 18))
    jline(d, [(590, 350), (610, 345)], w=4); jline(d, [(670, 345), (690, 350)], w=4)  # wide eyes
    jcircle(d, 600, 345, 10); jcircle(d, 680, 345, 10)
    d.polygon([(600, 600), (700, 560), (760, 620), (650, 660)], fill=(141, 90, 59))
    for (x, y) in [(470, 560), (520, 600), (800, 590), (840, 640)]:
        d.ellipse([x, y, x + 10, y + 14], fill=(90, 140, 200))
    d.text((860, 520), "damp patches", font=font(22), fill=INK)
    d.text((860, 560), "+ sand in pocket", font=font(22), fill=INK)
    hud_clock(d, "8:00 PM"); d.text((200, 26), "LOOP 2", font=font(26), fill=INK)
    caption(img, 7, "Recovery: 8:00 PM again, and he remembers", "CLOSE-UP · HIGH ANGLE", "GAMEPLAY VIEW (camera push-in)", "SFX phone_buzz · music restarts")
    return img


def panel_08():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 360], fill=(200, 204, 224))
    jline(d, [(700, 470), (740, 340), (1060, 330), (1180, 410), (1240, 470), (700, 470)], w=4)
    figure(d, 420, 610, 320, "talk", 1, shirt=(160, 70, 80), label="Hari")
    figure(d, 820, 610, 310, "keys", -1, label="Manikandan")
    d.rounded_rectangle([140, 90, 760, 230], 12, fill=(30, 30, 40))
    d.text((160, 100), "> Ask about Selvam", font=font(30), fill=WARM)
    d.text((160, 146), "   Just getting some air", font=font(26), fill=(200, 200, 210))
    d.text((160, 186), "(option exists only because of loop 1's clues)", font=font(18), fill=(160, 160, 170))
    hud_clock(d, "12:55 AM", 1080, 20)
    caption(img, 8, "Success, loop 2: the keys stay with Manikandan", "MEDIUM · EYE LEVEL", "GAMEPLAY VIEW", "SFX keys_exchanged + clue_saved")
    return img


def panel_09():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    for i in range(420):
        t = i / 420
        d.line([(0, i), (W, i)], fill=tuple(int(DAWN[k] * t + (170, 180, 215)[k] * (1 - t)) for k in range(3)))
    d.rectangle([0, 420, W, 520], fill=(190, 205, 220))
    d.ellipse([1050, 360, 1170, 480], fill=FIRE)  # fire glow still on the village side
    d.text((1000, 330), "the fire still burns", font=font(20), fill=INK)
    # low angle from the sand looking up at the deck railing
    jline(d, [(0, 300), (W, 260)], w=4); [jline(d, [(x, 300 - x * 0.03), (x, 380 - x * 0.03)], w=3) for x in range(40, 1280, 90)]
    figure(d, 520, 300, 170, "relief", 1, shirt=(160, 70, 80))
    d.rectangle([0, 520, W, 656], fill=(210, 195, 170))
    jcircle(d, 300, 600, 40, fill=(120, 110, 100))
    d.text((240, 545), "the rock", font=font(18), fill=INK)
    d.rounded_rectangle([640, 60, 1240, 160], 10, fill=(20, 20, 26))
    d.text((680, 70), "…but someone is missing.", font=font(34), fill=(255, 255, 255))
    caption(img, 9, "End of session: a safe dawn that isn't safe", "WIDE · LOW ANGLE", "GAMEPLAY VIEW, then END CARD", "SFX safe_dawn · music stopped")
    return img


PANELS = [
    ("01-title", panel_01), ("02-amma-call", panel_02), ("03-talk-manikandan", panel_03),
    ("04-clue-saved", panel_04), ("05-keys-taken", panel_05), ("06-dawn-failure", panel_06),
    ("07-loop2-wake", panel_07), ("08-keys-stay", panel_08), ("09-end-card", panel_09),
]

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    thumbs = []
    for name, fn in PANELS:
        im = fn(); im.save(OUT / f"{name}.png"); thumbs.append(im.resize((426, 240)))
        print("wrote", name)
    sheet = Image.new("RGB", (426 * 3 + 40, 240 * 3 + 40), (20, 20, 24))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (10 + (i % 3) * 436, 10 + (i // 3) * 250))
    sheet.save(OUT / "contact.png"); print("wrote contact.png")
