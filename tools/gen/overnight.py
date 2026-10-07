"""Overnight batch (2026-10-07): every remaining image and audio candidate, run sequentially.
Each generation is logged by gen_image.py / gen_audio.py. Nothing here decides acceptance;
Shriram judges the contact sheets in the morning."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PY = str(ROOT.parent / "virtualenvironments" / "vidiyum-img" / "bin" / "python")
APY = str(ROOT.parent / "virtualenvironments" / "vidiyum-audio" / "bin" / "python")
P = json.loads((ROOT / "prompts/image_prompts.json").read_text())
REF = "design/character/gen/hari-ref.png"
def gen(*args):
    print(">>", " ".join(args[:4]), flush=True)
    subprocess.run([PY, "tools/gen/gen_image.py", *args], cwd=ROOT)
stage = sys.argv[1] if len(sys.argv) > 1 else "all"
if stage in ("all", "poses"):
    for aid, pose in P["poses"].items():
        gen("--asset", aid, "--edit", REF, "--prompt", P["_pose_prefix"] + " " + pose + " " + P["_style"], "--seeds", "301", "302", "--w", "768", "--h", "1344")
if stage in ("all", "npcs"):
    for aid, desc in P["npcs"].items():
        gen("--asset", aid, "--prompt", desc + " " + P["_style"], "--seeds", "401", "402", "403", "--w", "768", "--h", "1344")
    for s in ("401", "402", "403"):
        gen("--asset", "NPC-MANI-PHONE", "--tag", f"from{s}", "--edit", f"gen/raw/NPC-MANI-IDLE_klein_s{s}.png", "--prompt", P["npc_edits"]["NPC-MANI-PHONE"] + " " + P["_style"], "--seeds", "501", "--w", "768", "--h", "1344")
if stage in ("all", "env"):
    sizes = {"ENV-VILLA": (1536, 576), "ENV-BEACH": (1536, 576), "ENV-MARBLE": (1024, 1024), "ENV-FIRE": (1024, 832), "ENV-SUV": (1344, 640)}
    for aid, desc in P["env"].items():
        w, h = sizes[aid]
        gen("--asset", aid, "--prompt", desc, "--seeds", "601", "602", "--w", str(w), "--h", str(h))
if stage in ("all", "audio"):
    subprocess.run([APY, "tools/gen/gen_audio.py", "sfx"], cwd=ROOT)
    subprocess.run([APY, "tools/gen/gen_audio.py", "music"], cwd=ROOT)
print("OVERNIGHT DONE", flush=True)
