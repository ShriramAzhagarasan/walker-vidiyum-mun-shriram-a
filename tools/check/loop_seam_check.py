"""Automated loop-seam check for the in-game music (TEST-REPORT, predicted failure F7).

Decodes each OGG in godot/assets/audio/music, concatenates 3 repetitions, and at each of the two
seams compares the sample step across the seam to the distribution of steps inside the loop.
PASS if the seam step <= the 99.9th percentile of in-loop steps AND the RMS of 20 ms before vs after
the seam differs by < 6 dB. This proves there is no sample discontinuity (click); it does NOT prove
the loop sounds musically seamless (phrase, groove), which needs human listening.
  python tools/check/loop_seam_check.py
"""
import sys
from pathlib import Path
import numpy as np, soundfile as sf
ROOT = Path(__file__).resolve().parents[2]
ok_all = True
for f in sorted((ROOT / "godot/assets/audio/music").glob("*.ogg")):
    y, sr = sf.read(f, always_2d=True)
    n = len(y); rep = np.concatenate([y, y, y])
    steps = np.max(np.abs(np.diff(y, axis=0)), axis=1)
    p999 = float(np.percentile(steps, 99.9))
    w = int(0.02 * sr)
    for k, s in enumerate((n, 2 * n), 1):
        step = float(np.max(np.abs(rep[s] - rep[s - 1])))
        r1 = np.sqrt(np.mean(rep[s - w:s] ** 2)); r2 = np.sqrt(np.mean(rep[s:s + w] ** 2))
        ddb = abs(20 * np.log10(max(r1, 1e-9) / max(r2, 1e-9)))
        ok = step <= p999 and ddb < 6.0
        ok_all &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {f.name} seam {k}: step {step:.4f} (in-loop p99.9 {p999:.4f}), RMS change {ddb:.2f} dB, loop {n / sr:.2f} s @ {sr} Hz")
print("RESULT:", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
