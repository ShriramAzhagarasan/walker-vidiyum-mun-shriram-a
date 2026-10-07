"""Run one logged image generation with mflux (FLUX.2 klein / Z-Image) and append to gen/log.jsonl.

Every call records: asset id, model, exact prompt, seed, size, steps, quantisation, reference
images, the command line, wall time and the output path. ASSET-LOG.md is built from this log
plus the human accept/reject decisions.

Example:
  python tools/gen/gen_image.py --asset CHAR-HARI-REF --seeds 11 12 --w 768 --h 1344 \
      --prompt-file prompts/hari_ref.txt
  python tools/gen/gen_image.py --asset CHAR-HARI-WALK --edit gen/raw/CHAR-HARI-REF_s12.png --prompt "..."
"""
import argparse
import json
import shlex
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENV = ROOT.parent / "virtualenvironments" / "vidiyum-img" / "bin"
RAW = ROOT / "gen" / "raw"
LOG = ROOT / "gen" / "log.jsonl"
MODELS = {"klein": "flux2-klein-4b", "zimage": "z-image-turbo"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset", required=True)
    ap.add_argument("--model", default="klein", choices=MODELS)
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--seeds", type=int, nargs="+", default=[1])
    ap.add_argument("--w", type=int, default=768); ap.add_argument("--h", type=int, default=1344)
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--q", type=int, default=8)
    ap.add_argument("--edit", nargs="*", default=None, help="reference image(s): uses the flux2 edit pipeline")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    prompt = a.prompt or Path(a.prompt_file).read_text().strip()
    RAW.mkdir(parents=True, exist_ok=True)
    for seed in a.seeds:
        name = f"{a.asset}{('_' + a.tag) if a.tag else ''}_{a.model}_s{seed}.png"
        out = RAW / name
        if a.edit:
            cmd = [str(VENV / "mflux-generate-flux2-edit"), "--model", MODELS[a.model], "--image-paths", *a.edit]
        elif a.model == "zimage":
            cmd = [str(VENV / "mflux-generate-z-image-turbo")]
        else:
            cmd = [str(VENV / "mflux-generate-flux2"), "--model", MODELS[a.model]]
        cmd += ["--prompt", prompt, "--seed", str(seed), "--width", str(a.w), "--height", str(a.h),
                "-q", str(a.q), "--output", str(out), "--metadata"]
        if a.steps:
            cmd += ["--steps", str(a.steps)]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        row = {
            "time": datetime.now().isoformat(timespec="seconds"), "asset": a.asset, "model": MODELS[a.model],
            "prompt": prompt, "seed": seed, "width": a.w, "height": a.h, "steps": a.steps, "quantize": a.q,
            "edit_refs": a.edit, "output": str(out.relative_to(ROOT)), "seconds": round(time.time() - t0, 1),
            "ok": r.returncode == 0 and out.exists(), "cmd": " ".join(shlex.quote(c) for c in cmd[1:]),
        }
        if not row["ok"]:
            row["error"] = (r.stderr or r.stdout)[-800:]
        with LOG.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(("OK  " if row["ok"] else "FAIL"), name, f"{row['seconds']}s", row.get("error", "")[-300:])


if __name__ == "__main__":
    main()
