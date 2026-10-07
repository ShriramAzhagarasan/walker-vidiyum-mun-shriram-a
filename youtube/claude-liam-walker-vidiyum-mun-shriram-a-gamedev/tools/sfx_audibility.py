#!/usr/bin/env python3
"""Is each SFX event audible above the music in the captured mix? For every sfx_event in the input log,
compare the RMS/peak of capture/<take>.wav in [t, t+1 s] with [t-1 s, t]. Writes capture/<take>-sfx-levels.json.
  python3 tools/sfx_audibility.py [--take run-01]
"""
import argparse, json, subprocess, re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument('--take', default='run-01'); a = ap.parse_args()
wav = R / f'capture/{a.take}.wav'
def lvl(t0, d):
    e = subprocess.run(['ffmpeg', '-nostats', '-ss', f'{max(t0, 0):.3f}', '-t', f'{d:.3f}', '-i', str(wav), '-af', 'volumedetect',
                        '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.search(r'mean_volume: (\S+)', e).group(1)), float(re.search(r'max_volume: (\S+)', e).group(1))
rows = []
for line in (R / f'capture/{a.take}-inputs.jsonl').read_text().splitlines():
    e = json.loads(line)
    if e['event'] != 'sfx_event':
        continue
    b, af = lvl(e['t'] - 1.0, 1.0), lvl(e['t'], 1.0)
    rows.append({'id': e['id'], 'clue': e.get('clue', ''), 't': e['t'], 'before_mean_db': b[0], 'before_max_db': b[1],
                 'after_mean_db': af[0], 'after_max_db': af[1], 'delta_mean_db': round(af[0] - b[0], 1)})
(R / f'capture/{a.take}-sfx-levels.json').write_text(json.dumps(rows, indent=1) + '\n')
print(f"{'event':16} {'t':>8} {'1s before mean/max':>20} {'1s after mean/max':>19} {'Δmean':>6}")
for r in rows:
    print(f"{r['id'] + (' ' + r['clue'] if r['clue'] else ''):16.16} {r['t']:8.2f} {r['before_mean_db']:9.1f}/{r['before_max_db']:6.1f} dB {r['after_mean_db']:9.1f}/{r['after_max_db']:6.1f} dB {r['delta_mean_db']:+6.1f}")
