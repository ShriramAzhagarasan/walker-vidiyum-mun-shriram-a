#!/usr/bin/env python3
"""Merge the parallel work back into beat_sheet.json: own-media beats (_qc/own_beats.json, from make_media.py --side)
and Remotion beats rendered in a scratch copy of this reel (argv[1]; media + provenance stamps copied back)."""
import json, shutil, sys
from pathlib import Path
REEL = Path(__file__).resolve().parents[1]
other = Path(sys.argv[1]); ids = sys.argv[2:]
sheet = json.loads((REEL / 'beat_sheet.json').read_text())
own = {b['beat_id']: b for b in json.loads((REEL / '_qc/own_beats.json').read_text())}
ob = {b['beat_id']: b for b in json.loads((other / 'beat_sheet.json').read_text())['beats']}
for i, b in enumerate(sheet['beats']):
    bid = b['beat_id']
    if bid in own:
        sheet['beats'][i] = own[bid]
    elif bid in ids:
        sheet['beats'][i] = ob[bid]
        shutil.copy2(other / f'media/{bid}.mp4', REEL / f'media/{bid}.mp4')
(REEL / 'beat_sheet.json').write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
print('merged', sorted(own), ids)
