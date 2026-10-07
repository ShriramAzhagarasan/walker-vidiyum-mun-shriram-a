#!/usr/bin/env python3
"""Build the asset-trace evidence images for the PHONE pose (design -> engine).

Inputs are the game repo's own files, copied byte-for-byte into evidence/asset-trace/
(hash recorded in evidence/asset-trace/HASHES.txt). The composed boards add only
labels, a highlight box and a crop/bbox overlay; they never repaint the art.

  python3 tools/make_trace_images.py
Writes evidence/asset-trace/*.png and media/*-evidence.png used by result beats.
"""
import hashlib, json, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
FONTS = REPO.parents[0] / 'brutalist.art/runtime/fonts'
OUT = REEL / 'evidence/asset-trace'
INK, ACCENT, PAGE, MUTED = (61, 57, 41), (217, 119, 87), (250, 249, 245), (110, 100, 85)

COPIES = {
    'poses-spec.png': 'design/character/poses-spec.png',
    'hari-ref.png': 'design/character/gen/hari-ref.png',
    'CHAR-HARI-POSES-1.jpg': 'design/gen-contact/CHAR-HARI-POSES-1.jpg',
    'CHAR-HARI-PHONE_klein_s301.png': 'gen/raw/CHAR-HARI-PHONE_klein_s301.png',
    'CHAR-HARI-PHONE_klein_s302.png': 'gen/raw/CHAR-HARI-PHONE_klein_s302.png',
    'phone.png': 'godot/assets/art/hari/phone.png',
    'R1-lighting-before.jpg': 'evidence/revisions/R1-lighting-before.jpg',
    'R1-lighting-after.jpg': 'evidence/revisions/R1-lighting-after.jpg',
}

def font(name, size):
    return ImageFont.truetype(str(next(f for f in FONTS.rglob('*.ttf') if name in f.name)), size)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def log_row(path, asset, seed):
    for line in (REPO / path).read_text().splitlines():
        row = json.loads(line)
        if row.get('asset') == asset and row.get('seed') == seed:
            return row
    raise SystemExit(f'no log row for {asset} seed {seed}')

def edit_row(src):
    for line in (REPO / 'gen/edit_log.jsonl').read_text().splitlines():
        row = json.loads(line)
        if row.get('src') == src and row.get('dest', '').startswith('godot/'):
            return row
    raise SystemExit('no edit row for ' + src)

def checker(w, h, s=24):
    im = Image.new('RGB', (w, h), (235, 235, 235))
    d = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x // s + y // s) % 2:
                d.rectangle((x, y, x + s - 1, y + s - 1), fill=(205, 205, 205))
    return im

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def spec_board():
    im = Image.open(OUT / 'poses-spec.png').convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle((905, 95, 1215, 590), outline=ACCENT, width=7)          # PHONE column, spec sheet coords
    d.text((1000, 600), 'highlight added for the film', font=font('Lato-Bold', 22), fill=ACCENT)
    im.save(OUT / 'B-spec-board.png')

def prompt_board(row):
    W, H = 3000, 1500
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    ref = Image.open(OUT / 'hari-ref.png').convert('RGBA')
    ref.thumbnail((620, 1180))
    bg = Image.new('RGB', ref.size, (205, 205, 205)); bg.paste(ref, mask=ref.split()[3])
    im.paste(bg, (60, 200))
    d.text((60, 120), 'Edit reference (edit_refs)', font=font('Lato-Bold', 40), fill=INK)
    d.text((60, 200 + ref.size[1] + 20), 'design/character/gen/hari-ref.png', font=font('PTMono-Regular', 30), fill=MUTED)
    x0 = 760
    d.text((x0, 60), 'gen/log.jsonl  ·  asset CHAR-HARI-PHONE  ·  seed %d  ·  exact prompt' % row['seed'], font=font('Lato-Bold', 44), fill=INK)
    f = font('PTMono-Regular', 46)
    pose = 'Holding a dark smartphone to his ear with his elbow clearly raised out to the side'
    y = 150
    for line in wrap(d, row['prompt'], f, W - x0 - 60):
        d.text((x0, y), line, font=f, fill=INK)
        y += 64
    # Underline the pose-specific clause (the part that differs per state).
    start = row['prompt'].index(pose)
    d.text((x0, y + 30), 'Pose clause (differs per state):', font=font('Lato-Bold', 40), fill=ACCENT)
    for line in wrap(d, row['prompt'][start:row['prompt'].index('.', start) + 1], font('PTMono-Regular', 46), W - x0 - 60):
        y += 0
        d.text((x0, y + 90), line, font=font('PTMono-Regular', 46), fill=ACCENT)
        y += 64
    im.save(OUT / 'B-prompt-board.png')

def raw_board():
    W, H = 3000, 1560
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    for i, (name, label) in enumerate([('CHAR-HARI-PHONE_klein_s301.png', 'seed 301 · in the build now'),
                                       ('CHAR-HARI-PHONE_klein_s302.png', 'seed 302 · rejected: two phones')]):
        r = Image.open(OUT / name).convert('RGB')
        r.thumbnail((760, 1330))
        x = 120 + i * 900
        im.paste(r, (x, 110))
        d.text((x, 30), label, font=font('Lato-Bold', 44), fill=INK if i else ACCENT)
        if i:   # mark the defect Shriram caught: the second phone at the far ear (approximate, raw coords)
            sc = r.size[0] / 768
            d.ellipse((x + 405 * sc, 110 + 150 * sc, x + 545 * sc, 110 + 320 * sc), outline=ACCENT, width=6)
        d.text((x, 110 + r.size[1] + 16), 'gen/raw/' + name, font=font('PTMono-Regular', 24), fill=MUTED)
    d.text((1960, 120), 'RAW MODEL OUTPUT', font=font('Lato-Bold', 64), fill=INK)
    for k, t in enumerate(['FLUX.2 [klein] 4B, reference edit', '768 × 1344 px, 8-bit quantised',
                           'flat grey background, still attached', 'NOT in-engine footage']):
        d.text((1960, 230 + k * 80), t, font=font('Lato-Regular', 46), fill=ACCENT if k == 3 else INK)
    d.text((1960, 620), 'Spec rule F5: elbow clearly out,', font=font('Lato-Bold', 42), fill=INK)
    d.text((1960, 680), 'so PHONE ≠ IDLE at 208 px.', font=font('Lato-Bold', 42), fill=INK)
    im.save(OUT / 'B-raw-board.png')

def edit_board(edit):
    W, H = 3000, 1560
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    raw = Image.open(OUT / 'CHAR-HARI-PHONE_klein_s301.png').convert('RGB')
    s = 1330 / raw.size[1]
    rv = raw.resize((round(raw.size[0] * s), 1330), Image.LANCZOS)
    dv = ImageDraw.Draw(rv)
    bbox = next(e for e in edit['edits'] if e.startswith('trimmed to bbox'))
    x0, y0, x1, y1 = [int(v) for v in bbox.split('(')[1].rstrip(')').split(',')]
    dv.rectangle((x0 * s, y0 * s, x1 * s, y1 * s), outline=ACCENT, width=6)
    im.paste(rv, (80, 140))
    d.text((80, 50), 'Raw s301 + logged trim box (overlay)', font=font('Lato-Bold', 44), fill=INK)
    final = Image.open(OUT / 'phone.png').convert('RGBA')
    k = 1330 / final.size[1]
    fv = final.resize((round(final.size[0] * k), 1330), Image.LANCZOS)
    cb = checker(fv.size[0], fv.size[1]); cb.paste(fv, mask=fv.split()[3])
    fx = 80 + rv.size[0] + 260
    im.paste(cb, (fx, 140))
    ax = 80 + rv.size[0] + 50
    d.rectangle((ax, 790, ax + 110, 820), fill=ACCENT)
    d.polygon([(ax + 110, 760), (ax + 170, 805), (ax + 110, 850)], fill=ACCENT)
    d.text((fx, 50), 'godot/assets/art/hari/phone.png', font=font('PTMono-Regular', 40), fill=INK)
    d.text((fx, 1480), '%d × %d px, transparent' % final.size, font=font('Lato-Regular', 34), fill=MUTED)
    tx = fx + cb.size[0] + 80
    d.text((tx, 140), 'gen/edit_log.jsonl', font=font('PTMono-Regular', 40), fill=INK)
    y = 220
    for e in edit['edits']:
        for line in wrap(d, '• ' + e, font('Lato-Regular', 40), W - tx - 50):
            d.text((tx, y), line, font=font('Lato-Regular', 40), fill=INK)
            y += 54
        y += 18
    im.save(OUT / 'B-edit-board.png')

def r1_board():
    W, H = 3840, 1290
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    for i, (name, label) in enumerate([('R1-lighting-before.jpg', 'BEFORE R1  ·  ambient 1b1a3c, moonlight 0.25'),
                                       ('R1-lighting-after.jpg', 'AFTER R1  ·  ambient 100f26, moonlight 0.08, string lights 2.8')]):
        # The committed R1 images are 3x3 contact grids of 640x360 tiles; show the 1:40 AM tile of each, enlarged.
        box = (0, 360, 640, 720) if i == 0 else (1280, 0, 1920, 360)    # the 1:40 AM tile in each grid (same moment)
        r = Image.open(OUT / name).convert('RGB').crop(box).resize((1860, 1046), Image.LANCZOS)
        im.paste(r, (40 + i * 1900, 150))
        d.text((40 + i * 1900, 60), label, font=font('Lato-Bold', 52), fill=ACCENT if i else INK)
    d.text((40, 1222), 'evidence/revisions/R1-lighting-*.jpg, the 1:40 AM tile of each 3x3 grid, enlarged  ·  scripted in-engine screenshots (test API), not played footage',
           font=font('Lato-Regular', 30), fill=MUTED)
    im.save(OUT / 'B-r1-board.png')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for dst, src in COPIES.items():
        shutil.copyfile(REPO / src, OUT / dst)
        rows.append(f'{sha(OUT / dst)}  {src}')
    row = log_row('gen/log.jsonl', 'CHAR-HARI-PHONE', 301)
    edit = edit_row('gen/raw/CHAR-HARI-PHONE_klein_s301.png')
    (OUT / 'phone-s301-log-row.json').write_text(json.dumps(row, indent=1) + '\n')
    (OUT / 'phone-s301-edit-row.json').write_text(json.dumps(edit, indent=1) + '\n')
    spec_board(); prompt_board(row); raw_board(); edit_board(edit); r1_board()
    for p in sorted(OUT.glob('B-*.png')):
        rows.append(f'{sha(p)}  youtube/{REEL.name}/evidence/asset-trace/{p.name}  (composed board)')
    (OUT / 'HASHES.txt').write_text('\n'.join(rows) + '\n')
    print('\n'.join(rows))

if __name__ == '__main__':
    main()
