#!/usr/bin/env python3
"""Conform audio + build the film's own media (no retiming of narration). Adapted from the A3 reel's make_media.py.

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
    y = 120
    for t, col in rows:
        if d.textlength(t, font=f) > W - 96:
            while d.textlength(t + '…', font=f) > W - 96:
                t = t[:-1]
            t += '…'
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

def make_text_stills():
    rows = []
    for fps in (30, 60, 144):
        log = f'logs/test_night_skip_{fps}fps.log'
        rows.append((f'== {log}', None))
        rows += [(l, None) for l in pick(log, ['frame period', 'R1 R2 R3 fade-in', 'R1 R2 R3 fade-out', 'takes 0.5 s of real frames', 'checks,'])]
    text_png([(t, colour(t)) for t, _ in rows], 'evidence/terminal_timings.png',
             'test_night_skip.gd through scripts/run-test.sh at 30 / 60 / 144 fps   (log lines, verbatim)', 52)
    rows = []
    for log, needles, note in [
            ('logs/mutations/m1_semicolon_deleted_60fps.log', ['SHADER ERROR', '[FAIL]', 'checks,'], 'm1: `;` deleted from night_skip.gdshader line 8'),
            ('logs/mutations/m2_uniform_renamed_60fps.log', ['[FAIL]', 'R1 R2 R3 fade-in', 'R4 re-press', 'checks,'], 'm2: skip_amount renamed to skip_amt in the shader only'),
            ('logs/mutations/m3_source_color_removed_60fps.log', ['[FAIL]', 'checks,'], 'm3: source_color removed from deck_marble.gdshader line 5')]:
        rows.append((f'== {log}   ({note})', None))
        rows += [(l, None) for l in pick(log, needles, first_only=('SHADER ERROR',))]
    rows.append(('(exit status 1 for each run, and each file restored: TEST-REPORT.md A5.2)', None))
    text_png([(t, colour(t)) for t, _ in rows], 'evidence/terminal_mutations.png',
             'Three mutations by Shriram, each run through scripts/run-test.sh   (log lines, verbatim)', 46)

def doc_rows(rel, anchor, n):
    lines = (REPO / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    assert len(hits) == 1, (rel, anchor, len(hits))
    s = hits[0]
    return s + 1, lines[s:s + n]

def make_table_stills():
    s, rows = doc_rows('TEST-REPORT.md', '| skip_amount | P1 battery (200, 31) captured', 6)
    text_png([(f'== TEST-REPORT.md lines {s}–{s + 5} (A5.4)', colour('=='))] + [(r, (225, 225, 230)) for r in rows],
             'evidence/table_glow.png', 'Glow: captured vs predicted on screen   (rows verbatim)', 60)
    s1, r1 = doc_rows('CHANGE-BRIEF.md', '| Quad | band 64 | band 128 | band 192 |', 4)
    s2, r2 = doc_rows('TEST-REPORT.md', '| Quad | band 64 | band 128 | band 192 | Prediction |', 4)
    rows = ([(f'== PREDICTED by Shriram · CHANGE-BRIEF.md lines {s1}–{s1 + 3} (§2.5)', colour('=='))]
            + [(r, (225, 225, 230)) for r in r1] + [('', (0, 0, 0))]
            + [(f'== CAPTURED · TEST-REPORT.md lines {s2}–{s2 + 3} (A5.6)', colour('=='))] + [(r, (225, 225, 230)) for r in r2])
    text_png(rows, 'evidence/table_hint.png', 'Hint experiment: predicted vs captured   (rows verbatim)', 72)

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
