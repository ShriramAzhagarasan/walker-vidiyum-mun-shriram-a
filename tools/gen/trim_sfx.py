"""Trim a generated SFX for game use; logged to gen/edit_log.jsonl.
  python tools/gen/trim_sfx.py SRC.wav DEST.ogg [--max-s 3.0] [--fade-ms 120] [--peak-db -1]
Steps: trim leading silence (first sample above -40 dBFS, minus 5 ms), cut to --max-s, fade out,
normalise peak to --peak-db, write OGG Vorbis (libsndfile)."""
import argparse, json
from datetime import datetime
from pathlib import Path
import numpy as np, soundfile as sf
ROOT = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dest")
ap.add_argument("--max-s", type=float, default=3.0); ap.add_argument("--fade-ms", type=float, default=120)
ap.add_argument("--peak-db", type=float, default=-1.0)
ap.add_argument("--rms-db", type=float, default=None, help="loudness target (RMS dBFS); soft-limited so peaks stay under --peak-db")
a = ap.parse_args()
y, sr = sf.read(a.src, always_2d=True)
env = np.max(np.abs(y), axis=1); thr = 10 ** (-40 / 20) * env.max()
start = max(0, int(np.argmax(env > thr)) - int(0.005 * sr))
y = y[start:start + int(a.max_s * sr)].copy()
f = min(len(y), int(a.fade_ms / 1000 * sr)); y[-f:] *= np.linspace(1, 0, f)[:, None]
ceil = 10 ** (a.peak_db / 20)
if a.rms_db is None:
    y *= ceil / max(1e-9, np.max(np.abs(y)))
else:
    # raise to the RMS target, then soft-limit (tanh) so transients never exceed the ceiling
    y *= (10 ** (a.rms_db / 20)) / max(1e-9, np.sqrt(np.mean(y ** 2)))
    y = ceil * np.tanh(y / ceil)
Path(a.dest).parent.mkdir(parents=True, exist_ok=True); sf.write(a.dest, y, sr, format="OGG", subtype="VORBIS")
row = {"time": datetime.now().isoformat(timespec="seconds"), "src": a.src, "dest": a.dest,
       "edits": [f"trimmed {start / sr * 1000:.0f} ms leading silence (-40 dBFS gate)", f"cut to {len(y) / sr:.2f} s", f"{a.fade_ms:.0f} ms fade-out", (f"loudness to {a.rms_db} dBFS RMS, tanh soft-limit at {a.peak_db} dBFS (playtest: SFX masked by music)" if a.rms_db is not None else f"peak normalised to {a.peak_db} dBFS"), "OGG Vorbis (libsndfile)"]}
with (ROOT / "gen/edit_log.jsonl").open("a") as fh: fh.write(json.dumps(row) + "\n")
print(a.dest, row["edits"][:2])
