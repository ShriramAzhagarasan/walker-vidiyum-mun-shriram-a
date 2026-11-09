#!/usr/bin/env python3
"""Conform audio + build the film's own media (no retiming of narration). Adapted from the A5 reel's make_media.py for A6.

  python3 tools/make_media.py [--only B04 ...]

* Log stills (evidence/terminal_*.png): lines copied verbatim from the recorded logs in logs/ (selected by substring,
  long lines truncated with a visible ellipsis; nothing typed by hand). Header rows name the log file.
* Table stills (evidence/table_*.png): rows copied verbatim from CHANGE-BRIEF.md / TEST-REPORT.md, located by anchor.
* Engine stills: evidence/a5/*.png (scripted captures), evidence/a5/human/*.png (Shriram's screenshots),
  evidence/standard_generated_sphere.png; an optional labelled crop zooms on the status bar.
* Movie-maker clips: capture/glow_motion.avi (scripted capture, tools/capture_glow_motion.gd), cut by frame range,
  played at the labelled speed. If narration outlasts the media, the last frame is held and labelled HELD FRAME.
Writes media/<B>.mp4 (exact frames), mp3/conformed/<B>.wav, actual_duration_s; resolves Remotion cue_fracs.
"""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
FPS = 30
FONTS = REPO.parents[0] / 'brutalist.art/runtime/fonts'
MONO = str(FONTS / 'PT_Mono/PTMono-Regular.ttf')
BOLD = str(FONTS / 'Lato/static/Lato-Bold.ttf')
SYMBOLS = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
FRAME_W, FRAME_H, FRAME_X, FRAME_Y = 3264, 1836, 288, 116
BG = '0x07080c'
DURATION_PATTERNS = ('BrutalistHesitantWriter', 'GodotDevWorkbench', 'GodotDesignFigure', 'GodotDesignBoard')

def sh(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)

def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                                capture_output=True, text=True, check=True).stdout)

def frames_of(p):
    return int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                               'stream=nb_read_frames', '-of', 'csv=p=0', str(p)], capture_output=True, text=True, check=True).stdout.strip())

# ---------- verbatim text stills ----------
def text_png(rows, out, title, max_size=56):
    W, H = FRAME_W, FRAME_H
    im = Image.new('RGB', (W, H), (16, 17, 22))
    d = ImageDraw.Draw(im)
    tf = ImageFont.truetype(BOLD, 44)
    d.rectangle((0, 0, W, 86), fill=(36, 38, 46))
    d.text((40, 18), title, font=tf, fill=(235, 235, 240))
    size = min(max_size, int((H - 150) / max(len(rows), 1) / 1.32))
    f = ImageFont.truetype(MONO, size)
    fb = ImageFont.truetype(SYMBOLS, size)          # PT Mono has no ✓; draw that glyph from a fallback font
    # wrap long verbatim lines (continuations indented with '↳'), never truncate
    wrapped = []
    for t, col in rows:
        first = True
        while d.textlength(t, font=f) > W - 96:
            k = len(t)
            while d.textlength(t[:k], font=f) > W - 96:
                k -= 1
            sp = t.rfind(' ', 0, k)
            k = sp if sp > 20 else k
            wrapped.append((t[:k], col)); t = '    ' + t[k:].lstrip(); first = False
        wrapped.append((t, col))
    rows = wrapped
    size2 = min(size, int((H - 150) / max(len(rows), 1) / 1.32))
    if size2 < size:
        size = size2; f = ImageFont.truetype(MONO, size); fb = ImageFont.truetype(SYMBOLS, size)
    y = 120
    for t, col in rows:
        x = 48
        for k, part in enumerate(t.split('✓')):
            if k:
                d.text((x, y), '✓', font=fb, fill=col)
                x += d.textlength('✓', font=fb)
            d.text((x, y), part, font=f, fill=col)
            x += d.textlength(part, font=f)
        y += int(size * 1.32)
    im.save(REEL / out)

def colour(t):
    if t.startswith('=='):
        return (240, 190, 110)
    if t.startswith('('):
        return (150, 150, 160)
    if '[PASS]' in t or '-> PASS' in t:
        return (120, 220, 140)
    if 'FAIL' in t or 'SHADER ERROR' in t:
        return (240, 120, 110)
    return (225, 225, 230)

def pick(log, needles, first_only=()):
    """Lines of a recorded log that contain any needle, verbatim, in file order (needles in first_only: first hit only)."""
    out, seen = [], set()
    for l in (REPO / log).read_text().splitlines():
        for n in needles:
            if n in l and not (n in first_only and n in seen):
                out.append(l.rstrip()); seen.add(n); break
    return out

def text_rows(log, needles, first_only=()):
    return [(l, None) for l in pick(log, needles, first_only)]

def make_text_stills():
    log = 'logs/test_footstep_scuff_trigger_60fps.log'
    rows = [(f'== {log}', None)] + text_rows(log, ['[PASS]', '[FAIL]', 'checks,'])
    text_png([(t, colour(t)) for t, _ in rows], 'evidence/terminal_trigger.png',
             'test_footstep_scuff_trigger.gd through scripts/run-test.sh at 60   (log lines, verbatim)', 50)
    log = 'logs/test_string_light_moths_controller_60fps.log'
    rows = [(f'== {log}   (selected lines; all 63 pass)', None)] + text_rows(log, [
        'MothsWest.emitting == true at load', 'real P paused', 'MothsWest.can_process() == false', 'byte-equal',
        'rule 4 (hide): MothsWest.emitting', 'rule 4 (show, active): MothsWest', 'reached 1740',
        'rule 2: MothsWest.emitting == false after', 'container still visible immediately', 'hid the group',
        'rule 4 (show, inactive): MothsWest', 'checks,'])
    text_png([(t, colour(t)) for t, _ in rows], 'evidence/terminal_controller.png',
             'test_string_light_moths_controller.gd at 60, real E / P / T keys   (log lines, verbatim)', 50)
    rows = []
    for log, note in [('logs/a6-mutations/m1_godot3_name.log', 'M1: SoftDust initial_velocity_min = 0.25 -> initial_velocity = 0.25'),
                      ('logs/a6-mutations/m2_value_drift.log', 'M2: SoftDust spread 80 -> 30, brief unchanged')]:
        rows.append((f'== {log}   ({note})', None))
        rows += text_rows(log, ['[FAIL]', 'checks,'])
    rows.append(('(exit status 1 for each run; scene restored with git checkout: TEST-REPORT.md A6.2)', None))
    rows.append(('', None))
    for log in ('logs/test_footstep_scuff_config_60fps.log', 'logs/test_string_light_moths_config_60fps.log'):
        rows.append((f'== {log}   (current build)', None))
        rows += text_rows(log, ['checks,'])
    text_png([(t, colour(t)) for t, _ in rows], 'evidence/terminal_mutations.png',
             'Two mutations by Shriram, and the configuration tests today   (log lines, verbatim)', 52)
    log = 'logs/cost_effects_60fps.log'
    rows = [(f'== {log}   (scripts/run-test.sh cost_effects.gd 60 300)', None)] + text_rows(log, ['[COST]', 'checks,'])
    text_png([(t, colour(t)) for t, _ in rows], 'evidence/terminal_cost.png',
             'Headless CPU price per frame, n = 300 per case   (log lines, verbatim)', 52)

def doc_rows(rel, anchor, n):
    lines = (REPO / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    assert len(hits) == 1, (rel, anchor, len(hits))
    s = hits[0]
    return s + 1, lines[s:s + n]

def block(rel, anchor, n, label):
    s, rows = doc_rows(rel, anchor, n)
    return [(f'== {rel} lines {s}–{s + n - 1} ({label})', colour('=='))] + [(r, (225, 225, 230)) for r in rows]

def make_table_stills():
    W = (225, 225, 230)
    rows = (block('TUNING.md', '**Claude\'s prediction for r1**', 3, 'Effect A r1, prediction') + [('', W)]
            + block('TUNING.md', '| r0 | 70.9 | 73.5 | 76.7 | 74.1', 2, 'measured: brightness change in the scuff patch, 0-255') + [('', W)]
            + block('TUNING.md', '**My verdict** (Shriram, running preview, 1280×720): **kept** — "keep it"', 4, 'verdict; wording disclosed'))
    text_png(rows, 'evidence/table_a_r1.png', 'Effect A r1: Claude\'s prediction, the measurement, Shriram\'s verdict   (verbatim)', 50)
    rows = (block('TUNING.md', '**Claude\'s prediction for r2:** every frame dimmer', 3, 'Effect A r2, prediction') + [('', W)]
            + block('TUNING.md', '| r2 | 61.4 | 64.4', 1, 'measured; r1 was 70.9 ... 36.9') + [('', W)]
            + block('TUNING.md', '- **Doesn\'t match:** brightness fell by', 2, 'comparison') + [('', W)]
            + block('TUNING.md', '**kept** — "they look like dust now', 2, 'verdict'))
    text_png(rows, 'evidence/table_a_r2.png', 'Effect A r2: prediction, measurement, verdict   (verbatim)', 50)
    rows = (block('godot/effects/string_light_moths.tscn', '[sub_resource type="Gradient" id="MothGrad"]', 3, 'r2 colour ramp today') + [('', W)]
            + block('CHANGE-BRIEF.md', '- **§B.3 colour and alpha ramp** (r2)', 3, 'revision 4'))
    text_png(rows, 'evidence/table_b_r2.png', 'Effect B r2: cream -> dark umber, alphas unchanged   (verbatim)', 50)
    rows = block('TEST-REPORT.md', '- **Visual Profiler:** the GPU column reads', 11, 'A6.6, GPU price, human check by Shriram')
    text_png(rows, 'evidence/table_gpu.png', 'GPU price: what could and could not be measured   (verbatim)', 50)

# ---------- fixture strips (real frames, cropped and enlarged, labelled) ----------
def strip_png(out, title, rows, crop, tiles_note):
    W, H = FRAME_W, FRAME_H
    im = Image.new('RGB', (W, H), (16, 17, 22))
    d = ImageDraw.Draw(im)
    tf = ImageFont.truetype(BOLD, 64); lf = ImageFont.truetype(MONO, 80)
    d.rectangle((0, 0, W, 86), fill=(36, 38, 46))
    d.text((40, 14), title, font=tf, fill=(235, 235, 240))
    x0, y0, x1, y1 = crop
    n = max(len(files) for _, _, files in rows)
    gap = 16
    tw = (W - 80 - gap * (n - 1)) // n
    th = round(tw * (y1 - y0) / (x1 - x0))
    avail = H - 86 - 100 - len(rows) * (80 + 104)
    if th * len(rows) > avail:
        th = avail // len(rows); tw = round(th * (x1 - x0) / (y1 - y0))
    y = 120
    for rlabel, d_, files in rows:
        d.text((40, y), rlabel, font=ImageFont.truetype(BOLD, 68), fill=(240, 190, 110)); y += 80
        x = 40
        for f, cap in files:
            tile = Image.open(REPO / d_ / f).convert('RGB').crop(crop).resize((tw, th), Image.LANCZOS)
            im.paste(tile, (x, y))
            d.text((x, y + th + 8), cap, font=lf, fill=(220, 220, 228))
            x += tw + gap
        y += th + 104
    nf = ImageFont.truetype(MONO, 64)
    while d.textlength(tiles_note, font=nf) > W - 80:
        nf = ImageFont.truetype(MONO, nf.size - 1)
    d.text((40, H - 84), tiles_note, font=nf, fill=(200, 200, 210))
    im.save(REEL / out)

def make_strips():
    A = (450, 470, 690, 640)
    tag = lambda k: f'{k:02d} · +{k - 9}' if k >= 9 else f'{k:02d} · before'
    fa = [9, 14, 19, 29, 34]
    files = lambda ks: [(f'frame000000{k:02d}.png', tag(k)) for k in ks]
    note = 'Caption: file · frames after trigger (file 09 = brief frame 10).'
    strip_png('evidence/strip_a_r0.png', 'FIXTURE strip · Effect A r0 · captures/footstep_scuff/r0-dark/ (seed 6, dark gate)',
              [('r0 (as briefed)', 'captures/footstep_scuff/r0-dark', files([9, 14, 19])), ('r0, continued', 'captures/footstep_scuff/r0-dark', files([24, 29, 34]))], A, note)
    strip_png('evidence/strip_a_r0_r1.png', 'FIXTURE strips · Effect A r0 vs r1 · same seed, dark gate',
              [('BEFORE · r0', 'captures/footstep_scuff/r0-dark', files(fa)),
               ('AFTER · r1 (SoftDust alpha 0.30 / 0.15 at 50 / 70 % life)', 'captures/footstep_scuff/r1-dark', files(fa))], A, note)
    strip_png('evidence/strip_a_r1_r2.png', 'FIXTURE strips · Effect A r1 vs r2 · same seed, dark gate',
              [('BEFORE · r1', 'captures/footstep_scuff/r1-dark', files(fa)),
               ('AFTER · r2 (softer gradient texture)', 'captures/footstep_scuff/r2-dark', files(fa))], A, note)
    Bc = (500, 70, 840, 230)
    btag = {8: 'file 08 · before', 9: 'file 09 · on', 29: 'file 29', 69: 'file 69 · off', 84: 'file 84', 144: 'file 144'}
    bf = lambda ks: [(f'frame{k:08d}.png', btag[k]) for k in ks]
    bnote = 'Moths on at file 09, condition off at file 69.'
    strip_png('evidence/strip_b_r0.png', 'FIXTURE strip · Effect B r0 · captures/string_light_moths/r0/ (seeds 101/202/303)',
              [('r0 (as briefed)', 'captures/string_light_moths/r0', bf([8, 9])), ('r0, continued', 'captures/string_light_moths/r0', bf([29, 69]))], Bc, bnote)
    strip_png('evidence/strip_b_r2_r3.png', 'FIXTURE strips · Effect B r2 vs r3 · same seeds',
              [('BEFORE · r2 (umber ramp, hazy texture)', 'captures/string_light_moths/r2', bf([8, 29, 69])),
               ('AFTER · r3 (solid texture)', 'captures/string_light_moths/r3', bf([8, 29, 69]))], Bc, bnote)
    # texture before / after: Claude's 6x renders, side by side
    a = Image.open(REPO / 'evidence/a6/effect-b-tuning/claude-moth-texture-before-r3-6x.png').convert('RGB')
    b = Image.open(REPO / 'evidence/a6/effect-b-tuning/claude-moth-texture-r3-6x.png').convert('RGB')
    im = Image.new('RGB', (FRAME_W, FRAME_H), (16, 17, 22)); d = ImageDraw.Draw(im)
    tw = (FRAME_W - 120) // 2; th = round(tw * a.height / a.width)
    f = ImageFont.truetype(BOLD, 52)
    for i, (img, lab) in enumerate([(a, 'BEFORE r3 · 16 of 2560 texels above 0.8 alpha'), (b, 'r3 · 794 texels above 0.8 alpha')]):
        x = 40 + i * (tw + 40)
        im.paste(img.resize((tw, th), Image.NEAREST), (x, 200))
        d.text((x, 120), lab, font=f, fill=(240, 190, 110))
    d.text((40, 200 + th + 30), 'evidence/a6/effect-b-tuning/claude-moth-texture-*-6x.png (Claude, during tuning) · counts: TUNING.md, Effect B r2-r3',
           font=ImageFont.truetype(MONO, 44), fill=(200, 200, 210))
    im.save(REEL / 'evidence/texture_before_after.png')

# ---------- captions ----------
def caption_png(path, text, held=False):
    im = Image.new('RGBA', (3840, 2160), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = FRAME_Y + FRAME_H + 22
    f = ImageFont.truetype(BOLD, 50)
    w = d.textlength(text, font=f)
    if w > FRAME_W - 40:
        f = ImageFont.truetype(BOLD, int(50 * (FRAME_W - 40) / w))
    d.text((FRAME_X, y), text, font=f, fill=(255, 255, 255, 255))
    if held:
        tag = 'HELD FRAME · last frame of the clip'
        tw = d.textlength(tag, font=f)
        d.rounded_rectangle((FRAME_X + FRAME_W - tw - 40, y - 12, FRAME_X + FRAME_W, y + 68), 14, fill=(217, 119, 87, 255))
        d.text((FRAME_X + FRAME_W - tw - 20, y), tag, font=f, fill=(255, 255, 255, 255))
    im.save(path)

FIT = (f"scale={FRAME_W}:{FRAME_H}:force_original_aspect_ratio=decrease:flags=lanczos,"
       f"pad={FRAME_W}:{FRAME_H}:(ow-iw)/2:(oh-ih)/2:color={BG},pad=3840:2160:{FRAME_X}:{FRAME_Y}:color={BG}")

def enc(out):
    return ['-r', FPS, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', out]

def crop_f(s):
    if 'crop' not in s:
        return ''
    x0, y0, x1, y1 = s['crop']
    return f'crop={x1 - x0}:{y1 - y0}:{x0}:{y0},'

def src_path(s):
    p = REPO / s['src']
    return p if p.exists() else REEL / s['src']

def build_own(b, total_frames):
    bid, shot = b['beat_id'], b['shot']
    work = REEL / '_qc/labels'; work.mkdir(parents=True, exist_ok=True)
    segs = shot['segments']
    clip_frames = {i: round((s['end_frame'] - s['start_frame']) / s['speed'])
                   for i, s in enumerate(segs) if s['kind'] == 'clip'}
    still_idx = [i for i, s in enumerate(segs) if s['kind'] == 'still']
    rest = max(total_frames - sum(clip_frames.values()), sum(round(segs[i].get('min', 2.0) * FPS) for i in still_idx))
    alloc, acc = {}, 0
    ws = [segs[i].get('w', 1.0) for i in still_idx]
    for k, i in enumerate(still_idx):
        n = rest - acc if k == len(still_idx) - 1 else round(rest * ws[k] / sum(ws))
        alloc[i] = n; acc += n
    parts, hold = [], 0
    for i, s in enumerate(segs):
        cap = work / f'{bid}-{i}.png'; caption_png(cap, s.get('label', shot['label']))
        part = work / f'{bid}-{i}.mp4'
        src = src_path(s)
        if s['kind'] == 'clip':
            n = clip_frames[i]
            # frames [start_frame, end_frame) of the 30 fps capture, slowed by the labelled factor (no retiming of speech)
            sh('ffmpeg', '-v', 'error', '-y', '-i', src, '-i', cap, '-filter_complex',
               f"[0:v]trim=start_frame={s['start_frame']}:end_frame={s['end_frame']},setpts=(PTS-STARTPTS)/{s['speed']},"
               f"fps={FPS},{crop_f(s)}{FIT}[g];[g][1:v]overlay=0:0,format=yuv420p[v]",
               '-map', '[v]', '-frames:v', n, *enc(part))
            got = frames_of(part)
            if got < n:
                hold += n - got
                tmp = work / f'{bid}-{i}-pad.mp4'
                sh('ffmpeg', '-v', 'error', '-y', '-i', part, '-vf', f'tpad=stop_mode=clone:stop={n - got}', *enc(tmp))
                tmp.replace(part)
        else:
            sh('ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', FPS, '-i', src, '-i', cap, '-filter_complex',
               f'[0:v]{crop_f(s)}{FIT}[g];[g][1:v]overlay=0:0,format=yuv420p[v]', '-map', '[v]', '-frames:v', alloc[i], *enc(part))
        parts.append(part)
    made = sum(frames_of(p) for p in parts)
    if made < total_frames:
        last = work / f'{bid}-last.png'
        sh('ffmpeg', '-v', 'error', '-y', '-sseof', '-0.1', '-i', parts[-1], '-frames:v', '1', '-update', '1', last)
        hp = work / f'{bid}-held.png'; caption_png(hp, '', held=True)
        held = work / f'{bid}-held.mp4'
        sh('ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', FPS, '-i', last, '-i', hp, '-filter_complex',
           '[0:v][1:v]overlay=0:0,format=yuv420p[v]', '-map', '[v]', '-frames:v', total_frames - made, *enc(held))
        parts.append(held); hold += total_frames - made
    lst = work / f'{bid}.txt'
    lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    sh('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', REEL / f'media/{bid}.mp4')
    return frames_of(REEL / f'media/{bid}.mp4'), hold

def resolve_cues(shot, total):
    rem = shot.get('remotion') or {}
    props = rem.get('props')
    if props is None or rem.get('pattern') not in DURATION_PATTERNS:
        return
    props['durationSeconds'] = total
    if 'cue_fracs' in props:
        props['cues'] = [{**{k: v for k, v in c.items() if k != 'frac'}, 'at': round(c['frac'] * total, 2)} for c in props['cue_fracs']]

def main():
    only = set(a for a in sys.argv[sys.argv.index('--only') + 1:] if not a.startswith('--')) if '--only' in sys.argv else None
    sheet_path = REEL / 'beat_sheet.json'
    sheet = json.loads(sheet_path.read_text())
    for d in ('mp3/conformed', 'media', '_qc/labels'):
        (REEL / d).mkdir(parents=True, exist_ok=True)
    make_text_stills()
    make_table_stills()
    make_strips()
    for b in sheet['beats']:
        bid, shot = b['beat_id'], b['shot']
        if only and bid not in only:
            continue
        lead, tail = float(b.get('lead_silence_s', 0)), float(b.get('tail_hold_s', 0))
        speech_file = REEL / f'mp3/beat-{bid}.mp3'
        speech = dur(speech_file)
        frames = math.ceil((lead + speech + tail + (0.5 if shot.get('source') == 'own' else 0.3)) * FPS)
        if shot.get('source') == 'own':
            got, hold = build_own(b, frames)
            frames = max(frames, got)
            b['hold_s'] = round(hold / FPS, 3)
        total = frames / FPS
        wav = REEL / f'mp3/conformed/{bid}.wav'
        delay = round(lead * 1000)
        sh('ffmpeg', '-v', 'error', '-y', '-i', speech_file, '-af',
           f'aresample=48000,aformat=channel_layouts=stereo,adelay={delay}|{delay},apad', '-t', f'{total:.6f}',
           '-ar', '48000', '-c:a', 'pcm_s16le', wav)
        b['audio_file'] = f'mp3/conformed/{bid}.wav'
        b['speech_duration_s'] = round(speech, 3)
        b['actual_duration_s'] = total
        b['render_duration_s'] = total
        resolve_cues(shot, total)
        print(bid, frames, round(total, 2), round(speech, 2), b.get('hold_s', ''), flush=True)
    sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
    print('total', round(sum(b.get('actual_duration_s', 0) for b in sheet['beats']), 2))

if __name__ == '__main__':
    main()
