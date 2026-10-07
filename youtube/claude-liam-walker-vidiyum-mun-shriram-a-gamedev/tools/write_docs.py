#!/usr/bin/env python3
"""Regenerate SHOTLIST.md and COMPONENTS.md from beat_sheet.json + gamedev-evidence.json (no hand drift)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sheet = json.loads((R / 'beat_sheet.json').read_text())
ev = json.loads((R / 'gamedev-evidence.json').read_text())
rows = ['# SHOTLIST — ' + sheet['metadata']['title'], '',
        f"Build `{sheet['metadata']['game']['build_id'][:12]}…` · capture log `{sheet['metadata'].get('capture_log', '')}` · 3840×2160, 30 fps.", '',
        '| Beat | Act | Visual | Source / range | Dur (s) | Words |', '|---|---|---|---|---|---|']
total = 0.0
for b in sheet['beats']:
    s = b['shot']
    if s.get('type') == 'GAMEPLAY':
        c = s['capture']
        vis, src = 'GAMEPLAY · ' + s['label'].split(' · ')[0], f"{c['id']} {c['start_s']:.2f}–{c['end_s']:.2f} s, game audio {s.get('game_audio_db')} dB"
    else:
        p = s['remotion']['props']
        vis = s['remotion']['pattern']
        src = p.get('path') or p.get('title') or p.get('greeting') or p.get('contextTitle') or ''
    d = b.get('actual_duration_s') or b.get('estimated_duration_s') or 0
    total += d
    rows.append(f"| {b['beat_id']} | {b['act']} | {vis} | {src} | {d:.2f} | {len(b['narration_text'].split())} |")
rows += ['', f'**Total ≈ {total:.1f} s ({total/60:.2f} min).**', '',
         'Code → result pairs: ' + ', '.join(f"{p['code_beat']}→{p['result_beat']}" for p in ev['code_result_pairs']) +
         '. B14 is the no-narration game-audio segment (not a component beat, not a result, not between a pair).']
(R / 'SHOTLIST.md').write_text('\n'.join(rows) + '\n')
c = ['# COMPONENTS — what the film explains', '', 'Generated from `gamedev-evidence.json` (every file under `godot/` except `.godot/` and `*.uid`).', '']
for comp in ev['components']:
    c += [f"## {comp['id']}  (beats {', '.join(comp['beat_ids'])})", '', comp['explanation'], '', 'Files: ' + ', '.join(f'`{f}`' for f in comp['files']), '']
c += ['## Excerpts shown (verbatim)', ''] + [f"- {e['beat_id']}: `godot/{e['path']}` lines {e['start_line']}–{e['end_line']}" for e in ev['excerpts']]
c += ['', '## Code → visible result', ''] + [f"- {p['code_beat']} → {p['result_beat']}: {p['observation']} (`{p['media']['path']}`)" for p in ev['code_result_pairs']]
(R / 'COMPONENTS.md').write_text('\n'.join(c) + '\n')
print('wrote SHOTLIST.md, COMPONENTS.md · total', round(total, 1), 's')
