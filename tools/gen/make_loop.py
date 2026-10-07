"""Cut a seamless music loop on bar boundaries, and measure the seam.

  python tools/gen/make_loop.py SRC.wav DEST.ogg [--bars 8] [--start-bar 1] [--xfade-ms 40]
Steps (logged to gen/edit_log.jsonl):
  1. librosa beat tracking -> tempo and beat times; bars assumed 4/4
  2. loop = N bars starting at a beat, both ends snapped to the nearest zero crossing (mono sum)
  3. equal-power crossfade: the audio just after the loop end is faded into the loop start
  4. seam metrics: sample step at the wrap point and RMS ratio between the last and first 50 ms
  5. export OGG Vorbis with libsndfile
"""
import argparse, json, subprocess, tempfile
from datetime import datetime
from pathlib import Path
import numpy as np, soundfile as sf, librosa

ROOT = Path(__file__).resolve().parents[2]


def seam_metrics(y, sr):
    step = float(np.max(np.abs(y[0] - y[-1])))
    n = int(0.05 * sr)
    r1, r2 = np.sqrt(np.mean(y[-n:] ** 2)), np.sqrt(np.mean(y[:n] ** 2))
    typical = float(np.median(np.max(np.abs(np.diff(y, axis=0)), axis=1)))
    return {"wrap_sample_step": round(step, 4), "typical_sample_step_median": round(typical, 4),
            "rms_last50ms": round(float(r1), 4), "rms_first50ms": round(float(r2), 4),
            "rms_ratio": round(float(max(r1, r2) / max(1e-6, min(r1, r2))), 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dest")
    ap.add_argument("--bars", type=int, default=8); ap.add_argument("--start-bar", type=int, default=1)
    ap.add_argument("--xfade-ms", type=float, default=40)
    a = ap.parse_args()
    y, sr = sf.read(a.src, always_2d=True)
    mono = y.mean(axis=1)
    tempo, beats = librosa.beat.beat_track(y=mono, sr=sr, units="samples")
    tempo = float(np.atleast_1d(tempo)[0])
    i0 = a.start_bar * 4
    i1 = i0 + a.bars * 4
    if i1 >= len(beats):
        raise SystemExit(f"not enough beats ({len(beats)}) for {a.bars} bars from bar {a.start_bar}")
    zc = np.nonzero(np.diff(np.signbit(mono)))[0]
    snap = lambda s: int(zc[np.argmin(np.abs(zc - s))])
    s0, s1 = snap(beats[i0]), snap(beats[i1])
    x = int(a.xfade_ms / 1000 * sr)
    loop = y[s0:s1].copy()
    tail = y[s1:s1 + x]
    if len(tail) == x:
        t = np.linspace(0, np.pi / 2, x)[:, None]
        loop[:x] = loop[:x] * np.sin(t) + tail * np.cos(t)
    m = seam_metrics(loop, sr)
    Path(a.dest).parent.mkdir(parents=True, exist_ok=True)
    sf.write(a.dest, loop, sr, format="OGG", subtype="VORBIS")
    row = {"time": datetime.now().isoformat(timespec="seconds"), "src": a.src, "dest": a.dest,
           "edits": [f"beat-tracked tempo {tempo:.1f} bpm", f"loop = {a.bars} bars (4/4) from bar {a.start_bar}: samples {s0}-{s1} ({(s1 - s0) / sr:.2f} s), ends snapped to zero crossings",
                     f"equal-power crossfade {a.xfade_ms:.0f} ms of post-loop audio into the loop start", "exported OGG Vorbis (libsndfile)"],
           "seam": m}
    with (ROOT / "gen/edit_log.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps({"dest": a.dest, "tempo": round(tempo, 1), "seconds": round((s1 - s0) / sr, 2), **m}))


if __name__ == "__main__":
    main()
