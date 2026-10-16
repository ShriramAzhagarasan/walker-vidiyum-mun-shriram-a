#!/usr/bin/env python3
"""Conform audio + build the film's own media (no retiming of narration).

  python3 tools/make_media.py [--only B04 ...]

* Test-output stills: evidence/check_a3_*.png rendered from the ACTUAL headless stdout captured in
  evidence/check_a3_*.out.txt (lines verbatim; long lines truncated with an ellipsis, a few blocks elided
  with a visible "…" row; nothing typed by hand).
* Recording clips: cut from Shriram's screen recording (blendersession.mov, not copied into git) into
  clips/<beat>-<n>.mp4, sped up only by the labelled factor (setpts), optional crop; reframed at 85 %
  inside title-safe with a caption band. If narration outlasts the clip, its last frame is held and
  labelled HELD FRAME.
* Engine stills: evidence/a3/godot-*.png (real engine screenshots) with their own caption.
Writes media/<B>.mp4 (exact frames), mp3/conformed/<B>.wav, actual_duration_s; resolves Remotion cue_fracs.
"""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
FPS = 30
REC = Path('/Users/shriramalagarasan/Desktop/blendersession.mov')
FONTS = REPO.parents[0] / 'brutalist.art/runtime/fonts'
MONO = str(FONTS / 'PT_Mono/PTMono-Regular.ttf')
BOLD = str(FONTS / 'Lato/static/Lato-Bold.ttf')
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

# ---------- terminal stills from real stdout ----------
def terminal_png(src, out, keep, title):
    lines = [l.rstrip() for l in (REEL / src).read_text().splitlines()]
    rows = []
    for item in keep:
        if item == '…':
            rows.append(('…', (140, 140, 150)))
            continue
        a, b = item
        for l in lines[a:b]:
            if l.startswith('exit='):
                continue
            t = l if len(l) <= 112 else l[:111] + '…'
            col = (120, 220, 140) if '[PASS]' in t or '-> PASS' in t else ((240, 120, 110) if 'FAIL' in t else (225, 225, 230))
            if t.startswith('=='):
                col = (240, 190, 110)
            rows.append((t, col))
    W, H = FRAME_W, FRAME_H
    im = Image.new('RGB', (W, H), (16, 17, 22))
    d = ImageDraw.Draw(im)
    tf = ImageFont.truetype(BOLD, 44)
    d.rectangle((0, 0, W, 86), fill=(36, 38, 46))
    d.text((40, 18), title, font=tf, fill=(235, 235, 240))
    size = min(52, int((H - 150) / max(len(rows), 1) / 1.32))
    f = ImageFont.truetype(MONO, size)
    y = 120
    for t, col in rows:
        if d.textlength(t, font=f) > W - 96:          # truncate long lines visibly at the frame edge
            while d.textlength(t + '…', font=f) > W - 96:
                t = t[:-1]
            t += '…'
        d.text((48, y), t, font=f, fill=col)
        y += int(size * 1.32)
    im.save(REEL / out)

def make_terminal_stills():
    terminal_png('evidence/check_a3_assets.out.txt', 'evidence/check_a3_assets.png',
                 [(2, 3), (4, 16), '…', (17, 18), (19, 20), (25, 26), '…', (29, 30), (31, 32), (37, 38), '…', (41, 42)],
                 'godot --headless --script res://tests/check_a3_assets.gd   (stdout excerpt, verbatim)')
    terminal_png('evidence/check_a3_selftest.out.txt', 'evidence/check_a3_selftest.png', [(2, 21)],
                 'godot --headless --script res://tests/check_a3_selftest.gd   (stdout, verbatim)')

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

def build_own(b, total_frames):
    bid, shot = b['beat_id'], b['shot']
    work = REEL / '_qc/labels'; work.mkdir(parents=True, exist_ok=True)
    (REEL / 'clips').mkdir(exist_ok=True)
    segs = shot['segments']
    # fixed-length clip segments first, stills share the rest
    clip_frames = {}
    for i, s in enumerate(segs):
        if s['kind'] == 'clip':
            clip_frames[i] = round((s['end'] - s['start']) / s['speed'] * FPS)
    still_idx = [i for i, s in enumerate(segs) if s['kind'] == 'still']
    rest = total_frames - sum(clip_frames.values())
    min_still = sum(round(segs[i].get('min', 0) * FPS) for i in still_idx)
    if still_idx and rest < min_still:
        rest = min_still
    alloc = {}
    if still_idx:
        ws = [segs[i].get('w', 1.0) for i in still_idx]
        acc = 0
        for k, i in enumerate(still_idx):
            n = rest - acc if k == len(still_idx) - 1 else round(rest * ws[k] / sum(ws))
            alloc[i] = n; acc += n
    parts, hold = [], 0
    for i, s in enumerate(segs):
        cap_text = s.get('label', shot['label'])
        cap = work / f'{bid}-{i}.png'; caption_png(cap, cap_text)
        part = work / f'{bid}-{i}.mp4'
        if s['kind'] == 'clip':
            raw = REEL / f'clips/{bid}-{i}.mp4'
            crop = ''
            if 'crop' in s:
                x0, y0, x1, y1 = s['crop']; crop = f'crop={x1 - x0}:{y1 - y0}:{x0}:{y0},'
            n = clip_frames[i]
            # the clip as used: trimmed from the recording, sped by the labelled factor, 30 fps
            sh('ffmpeg', '-v', 'error', '-y', '-ss', f"{s['start']:.3f}", '-t', f"{s['end'] - s['start']:.3f}", '-i', REC,
               '-an', '-vf', f"{crop}setpts=PTS/{s['speed']},fps={FPS},scale=1920:-2", '-frames:v', n,
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', raw)
            sh('ffmpeg', '-v', 'error', '-y', '-ss', f"{s['start']:.3f}", '-t', f"{s['end'] - s['start']:.3f}", '-i', REC, '-i', cap,
               '-filter_complex', f"[0:v]{crop}setpts=PTS/{s['speed']},fps={FPS},{FIT}[g];[g][1:v]overlay=0:0,format=yuv420p[v]",
               '-map', '[v]', '-frames:v', n, *enc(part))
            got = frames_of(part)
            if got < n:                      # short read at the end: pad by cloning, counted as held
                hold += n - got
                tmp = work / f'{bid}-{i}-pad.mp4'
                sh('ffmpeg', '-v', 'error', '-y', '-i', part, '-vf', f'tpad=stop_mode=clone:stop={n - got}', *enc(tmp))
                tmp.replace(part)
            parts.append(part)
        else:
            n = alloc[i]
            src = REPO / s['src'] if (REPO / s['src']).exists() else REEL / s['src']
            sh('ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', FPS, '-i', src, '-i', cap, '-filter_complex',
               f'[0:v]{FIT}[g];[g][1:v]overlay=0:0,format=yuv420p[v]', '-map', '[v]', '-frames:v', n, *enc(part))
            parts.append(part)
    made = sum(frames_of(p) for p in parts)
    if made < total_frames:              # narration outlasts the last clip: labelled held frame
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
    got = frames_of(REEL / f'media/{bid}.mp4')
    return got, hold

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
    for d in ('mp3/conformed', 'media', '_qc/labels', 'clips'):
        (REEL / d).mkdir(parents=True, exist_ok=True)
    make_terminal_stills()
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
    if '--side' in sys.argv:            # own beats built while Remotion renders: merge later (tools/merge_side.py)
        (REEL / '_qc/own_beats.json').write_text(json.dumps([b for b in sheet['beats'] if not only or b['beat_id'] in only], indent=1, ensure_ascii=False))
        return
    sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
    print('total', round(sum(b.get('actual_duration_s', 0) for b in sheet['beats']), 2))

if __name__ == '__main__':
    main()
