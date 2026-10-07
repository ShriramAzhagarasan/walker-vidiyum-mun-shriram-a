#!/usr/bin/env python3
"""Conform audio and gameplay slots to exact 30 fps frame counts (no retiming).

  python3 tools/conform_timeline.py            # after Kokoro: real audio, gameplay media, durations
  python3 tools/conform_timeline.py --estimate # before Kokoro: durations from word counts (pilot renders only)

Per beat:
  speech = measured Kokoro mp3 (mp3/beat-<id>.mp3); audio = lead_silence_s + speech (+ tail_hold_s), padded.
GAMEPLAY beats (shot.type == GAMEPLAY):
  video = exact frames [start_s*30, end_s*30) of capture/<take>.mp4 at normal speed, reframed at 85 % inside
          title-safe with a caption band; if the narration is longer, the last frame is held and labelled HELD FRAME.
  audio = narration over the slice's own audio from the SAME frames (capture/<take>.wav) at shot.game_audio_db;
          game audio is faded out over the held frames and never continues past the beat.
  B14-style beats (narration_text == ""): audio = the game audio alone, unchanged gain -> mp3/game/<id>.wav.
Writes actual_duration_s = frames/30 so compile.py's ratio is exactly 1.0, and resolves Remotion cue
fractions (props.cue_fracs) into seconds.
"""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[1]
FPS = 30
FONTS = R.parents[2] / 'brutalist.art/runtime/fonts'
WPS = 3.0                      # estimate only (Kokoro am_onyx measured ~2.9-3.4 words/s on the A1 reel)
DURATION_PATTERNS = ('BrutalistHesitantWriter', 'GodotDevWorkbench', 'GodotDesignFigure', 'GodotDesignBoard')

def sh(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)

def dur(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)

def font(name, size):
    return ImageFont.truetype(str(next(f for f in FONTS.rglob('*.ttf') if name in f.name)), size)

FRAME_W, FRAME_H, FRAME_X, FRAME_Y = 3264, 1836, 288, 116
REFRAME = f"scale={FRAME_W}:{FRAME_H}:flags=lanczos,pad=3840:2160:{FRAME_X}:{FRAME_Y}:color=0x07080c"

def label_png(path, text, held, accent=False):
    im = Image.new('RGBA', (3840, 2160), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = FRAME_Y + FRAME_H + 22
    f = font('Lato-Bold', 50)
    if accent:
        w = d.textlength(text, font=f)
        d.rounded_rectangle((FRAME_X - 16, y - 12, FRAME_X + w + 16, y + 68), 14, fill=(217, 119, 87, 255))
    d.text((FRAME_X, y), text, font=f, fill=(255, 255, 255, 255))
    if held:
        tag = 'HELD FRAME · final frame of the action'
        w = d.textlength(tag, font=f)
        d.rounded_rectangle((FRAME_X + FRAME_W - w - 40, y - 12, FRAME_X + FRAME_W, y + 68), 14, fill=(217, 119, 87, 255))
        d.text((FRAME_X + FRAME_W - w - 20, y), tag, font=f, fill=(255, 255, 255, 255))
    im.save(path)

def resolve_cues(shot, total):
    rem = shot.get('remotion') or {}
    props = rem.get('props')
    if props is None or rem.get('pattern') not in DURATION_PATTERNS:
        return
    props['durationSeconds'] = total
    if 'cue_fracs' in props:
        cues = []
        for c in props['cue_fracs']:
            row = {k: v for k, v in c.items() if k != 'frac'}
            row['at'] = round(c['frac'] * total, 2)
            cues.append(row)
        props['cues'] = cues

def main():
    estimate = '--estimate' in sys.argv
    sheet_path = R / 'beat_sheet.json'
    sheet = json.loads(sheet_path.read_text())
    build8 = sheet['metadata']['game']['build_id'][:8]
    for d in ('mp3/conformed', 'mp3/game', '_qc/labels', 'media'):
        (R / d).mkdir(parents=True, exist_ok=True)
    report = []
    for b in sheet['beats']:
        bid, shot = b['beat_id'], b.get('shot', {})
        text = b.get('narration_text', '')
        lead, tail = float(b.get('lead_silence_s', 0.0)), float(b.get('tail_hold_s', 0.0))
        speech_file = R / f'mp3/beat-{bid}.mp3'
        if text:
            speech = len(text.split()) / WPS if estimate else dur(speech_file)
        else:
            speech = 0.0
        need = lead + speech + tail
        frames = math.ceil(need * FPS - 1e-9)
        if shot.get('type') == 'GAMEPLAY' and '--skip-gameplay' in sys.argv:
            continue
        if shot.get('type') == 'GAMEPLAY':
            cap = shot['capture']
            f0, f1 = round(cap['start_s'] * FPS), round(cap['end_s'] * FPS)
            action = f1 - f0
            frames = max(action, frames)
            hold = frames - action
            if not estimate:
                video = R / f"capture/{cap['id']}.mp4"
                game_wav = R / f"capture/{cap['id']}.wav"
                live_png, held_png = R / f'_qc/labels/{bid}-live.png', R / f'_qc/labels/{bid}-held.png'
                text_label = shot['label'] + ' · build ' + build8
                label_png(live_png, text_label, False, accent=not text)
                label_png(held_png, text_label, True, accent=not text)
                live = R / f'_qc/labels/{bid}-live.mp4'
                sh('ffmpeg', '-v', 'error', '-y', '-i', video, '-i', live_png, '-filter_complex',
                   f'[0:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS,{REFRAME}[g];[g][1:v]overlay=0:0,format=yuv420p[v]',
                   '-map', '[v]', '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', live)
                parts = [live]
                if hold:
                    last = R / f'_qc/labels/{bid}-last.png'
                    sh('ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', f'select=eq(n\\,{f1 - 1})', '-frames:v', '1', last)
                    held = R / f'_qc/labels/{bid}-held.mp4'
                    sh('ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', FPS, '-i', last, '-i', held_png,
                       '-filter_complex', f'[0:v]{REFRAME}[g];[g][1:v]overlay=0:0,format=yuv420p[v]', '-map', '[v]',
                       '-frames:v', hold, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', held)
                    parts.append(held)
                lst = R / f'_qc/labels/{bid}.txt'
                lst.write_text(''.join(f"file '{p}'\n" for p in parts))
                sh('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', R / f'media/{bid}.mp4')
                got = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                                          'stream=nb_read_frames', '-of', 'csv=p=0', str(R / f'media/{bid}.mp4')],
                                         capture_output=True, text=True, check=True).stdout.strip())
                assert got == frames, (bid, got, frames)
                # Game audio from exactly the same frame range, then (if narrated) narration on top.
                a0, alen = f0 / FPS, action / FPS
                total = frames / FPS
                g = R / f'mp3/game/{bid}.wav'
                gain = float(shot.get('game_audio_db', -16.0))
                fade = f',afade=t=out:st={max(alen - 0.4, 0):.3f}:d=0.4' if hold else ''
                sh('ffmpeg', '-v', 'error', '-y', '-ss', f'{a0:.6f}', '-t', f'{alen:.6f}', '-i', game_wav, '-af',
                   f'aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB{fade},apad', '-t', f'{total:.6f}',
                   '-ar', '48000', '-c:a', 'pcm_s16le', g)
                if text:
                    out = R / f'mp3/conformed/{bid}.wav'
                    delay = round(lead * 1000)
                    sh('ffmpeg', '-v', 'error', '-y', '-i', speech_file, '-i', g, '-filter_complex',
                       f'[0:a]aresample=48000,aformat=channel_layouts=stereo,adelay={delay}|{delay},apad[n];'
                       f'[n][1:a]amix=inputs=2:duration=longest:normalize=0[m]', '-map', '[m]', '-t', f'{total:.6f}',
                       '-ar', '48000', '-c:a', 'pcm_s16le', out)
                    b['audio_file'] = f'mp3/conformed/{bid}.wav'
                else:
                    b['audio_file'] = f'mp3/game/{bid}.wav'
            b['action_duration_s'] = round(action / FPS, 6)
            b['hold_s'] = round(hold / FPS, 6)
        elif not estimate:
            total = frames / FPS
            wav = R / f'mp3/conformed/{bid}.wav'
            delay = round(lead * 1000)
            sh('ffmpeg', '-v', 'error', '-y', '-i', speech_file, '-af',
               f'aresample=48000,aformat=channel_layouts=stereo,adelay={delay}|{delay},apad',
               '-t', f'{total:.6f}', '-ar', '48000', '-c:a', 'pcm_s16le', wav)
            b['audio_file'] = f'mp3/conformed/{bid}.wav'
        total = frames / FPS
        if estimate:
            b['estimated_duration_s'] = total
        else:
            b['speech_duration_s'] = round(speech, 3)
            b['actual_duration_s'] = total
            b['render_duration_s'] = total
        resolve_cues(shot, total)
        report.append((bid, frames, round(total, 2), round(speech, 2), b.get('hold_s', '')))
    sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
    for row in report:
        print(*row)
    print('total', round(sum(r[2] for r in report), 2), 's', '(ESTIMATE)' if estimate else '')

if __name__ == '__main__':
    main()
