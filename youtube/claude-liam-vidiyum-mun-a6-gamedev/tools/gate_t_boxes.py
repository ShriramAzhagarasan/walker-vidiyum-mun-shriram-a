#!/usr/bin/env python3
"""Draw GATE T's flagged blobs on the mid-beat frame (the frame type_check samples) for each FAIL beat in TYPECHECK.md."""
import re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
REEL = Path(__file__).resolve().parents[1]
txt = (REEL / 'TYPECHECK.md').read_text()
fails = re.findall(r'^\| (B\d\d) \|.*\*\*FAIL\*\*', txt, re.M)
for bid in fails:
    sec = txt.split(f'### {bid} ')[1].split('\n### ')[0] if f'### {bid} ' in txt else ''
    boxes = [tuple(map(int, m)) for m in re.findall(r'blob@\((\d+),(\d+)\)–\((\d+),(\d+)\)', sec)]
    mp = REEL / f'media/{bid}.mp4'
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mp)],
                             capture_output=True, text=True).stdout)
    out = REEL / f'_qc/gate-t/gt_{bid}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{d / 2:.3f}', '-i', str(mp), '-frames:v', '1', '-vf', 'scale=3840:2160', str(out)], check=True)
    im = Image.open(out).convert('RGB'); dr = ImageDraw.Draw(im)
    for b in boxes:
        dr.rectangle(b, outline=(255, 0, 255), width=8)
    im.resize((1920, 1080)).save(out)
    print(bid, len(boxes), 'boxes', out.name)
