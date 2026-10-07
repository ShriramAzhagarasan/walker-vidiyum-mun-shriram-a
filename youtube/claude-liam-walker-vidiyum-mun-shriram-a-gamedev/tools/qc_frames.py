#!/usr/bin/env python3
"""Frame + audio QC of the final export: frames at 15/50/85 % of every beat (contact sheets for reading),
and per-beat loudness of the exported audio (mean/max dB), written to _qc/levels.json.

  python3 tools/qc_frames.py <export.mp4>
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[1]
src = Path(sys.argv[1])
sheet = json.loads((R / 'beat_sheet.json').read_text())
out = R / '_qc/frames'; out.mkdir(parents=True, exist_ok=True)
t0, rows, levels = 0.0, [], {}
for b in sheet['beats']:
    d = b.get('render_duration_s') or b['actual_duration_s']
    tiles = []
    for f in (0.15, 0.5, 0.85):
        p = out / f"{b['beat_id']}-{int(f*100):02d}.png"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0 + d * f:.3f}', '-i', str(src), '-frames:v', '1',
                        '-vf', 'scale=960:-1', str(p)], check=True)
        tiles.append(p)
    r = subprocess.run(['ffmpeg', '-nostats', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', str(src), '-vn',
                        '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
    mean = re.search(r'mean_volume: (-?[\d.]+|-inf)', r.stderr); mx = re.search(r'max_volume: (-?[\d.]+|-inf)', r.stderr)
    levels[b['beat_id']] = {'start_s': round(t0, 3), 'dur_s': round(d, 3), 'mean_db': mean and mean.group(1), 'max_db': mx and mx.group(1),
                            'narrated': bool(b.get('narration_text'))}
    rows.append((b['beat_id'], tiles))
    t0 += d
# contact sheets, 6 beats per sheet
font = ImageFont.load_default()
for k in range(0, len(rows), 6):
    chunk = rows[k:k + 6]
    sheet_im = Image.new('RGB', (3 * 960, len(chunk) * 560), 'white')
    dr = ImageDraw.Draw(sheet_im)
    for i, (bid, tiles) in enumerate(chunk):
        for j, p in enumerate(tiles):
            sheet_im.paste(Image.open(p), (j * 960, i * 560 + 20))
        dr.text((6, i * 560 + 2), bid, fill='black', font=font)
    sheet_im.save(R / f'_qc/contact-{k // 6 + 1}.jpg', quality=88)
(R / '_qc/levels.json').write_text(json.dumps(levels, indent=1) + '\n')
print(json.dumps(levels, indent=1))
print('timeline end', round(t0, 3))
