#!/usr/bin/env python3
"""Run the game's own tests on the isolated capture copy and render the REAL stdout for beat B13.

  python3 tools/render_test_output.py [--take run-01]
Writes evidence/tests/*.txt (full stdout, verbatim) and evidence/tests/B13-test-output.png
(selected verbatim lines + the capture driver's own summary row). Nothing is typed by hand.
"""
import argparse, json, os, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
GODOT = os.environ.get('GODOT', '/Users/shriramalagarasan/Downloads/Godot.app/Contents/MacOS/Godot')
FONTS = REEL.parents[2] / 'brutalist.art/runtime/fonts'
OUT = REEL / 'evidence/tests'

def run(test):
    r = subprocess.run([GODOT, '--headless', '--path', str(REEL / 'capture-project'), '-s', f'res://tests/{test}'],
                       capture_output=True, text=True, timeout=600)
    text = r.stdout + r.stderr
    (OUT / test.replace('.gd', '.txt')).write_text(f'$ godot --headless --path capture-project -s res://tests/{test}\n# exit {r.returncode}\n' + text)
    return text, r.returncode

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--take', default='run-01'); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    results = {}
    for test in ['test_sound_triggers.gd', 'test_audio_mix.gd', 'test_loop_logic.gd', 'test_slice_smoke.gd', 'test_assets_present.gd']:
        text, code = run(test)
        last = [l for l in text.splitlines() if 'checks' in l and ('PASS' in l or 'FAIL' in l)]
        results[test] = {'exit': code, 'summary': last[-1] if last else '(no summary line)'}
    (OUT / 'summary.json').write_text(json.dumps(results, indent=1) + '\n')
    sound = (OUT / 'test_sound_triggers.txt').read_text().splitlines()
    pick = [l for l in sound if l.startswith('[') and 'exact count' in l and not l.startswith('[PASS] muted')]
    pick += [l for l in sound if 'mute: same trigger counts' in l]
    pick += [results['test_sound_triggers.gd']['summary']]
    log = REEL / f'capture/{a.take}-inputs.jsonl'
    summary = None
    if log.exists():
        rows = [json.loads(l) for l in log.read_text().splitlines() if l.strip()]
        summary = next((r for r in reversed(rows) if r['event'] == 'summary'), None)
    W, H = 3000, 1500
    im = Image.new('RGB', (W, H), (32, 37, 49))
    d = ImageDraw.Draw(im)
    mono = ImageFont.truetype(str(next(FONTS.rglob('PTMono-Regular.ttf'))), 40)
    bold = ImageFont.truetype(str(next(FONTS.rglob('Lato-Bold.ttf'))), 44)
    d.text((60, 40), '$ godot --headless --path capture-project -s res://tests/test_sound_triggers.gd', font=mono, fill=(139, 199, 243))
    y = 120
    for l in pick:
        while l:
            chunk, l = l[:118], l[118:]
            d.text((60, y), chunk, font=mono, fill=(237, 241, 247) if 'FAIL' not in chunk else (229, 72, 77))
            y += 56
    y += 40
    d.text((60, y), f'capture/{a.take}-inputs.jsonl · driver summary row (counts SoundBank.trigger_counts in the filmed run)', font=bold, fill=(217, 119, 87))
    y += 70
    if summary:
        line = json.dumps({'counts': summary['counts'], 'ended': summary['ended'], 'failed': summary['failed']})
        while line:
            chunk, line = line[:118], line[118:]
            d.text((60, y), chunk, font=mono, fill=(237, 241, 247)); y += 56
    else:
        d.text((60, y), '(no capture summary yet)', font=mono, fill=(229, 72, 77))
    im.save(OUT / 'B13-test-output.png')
    print(json.dumps(results, indent=1))

if __name__ == '__main__':
    main()
