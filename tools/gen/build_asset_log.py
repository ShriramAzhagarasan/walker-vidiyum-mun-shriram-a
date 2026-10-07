"""Build ASSET-LOG.md from the machine logs plus the human decisions.

Inputs:
  gen/log.jsonl         image generations (tools/gen/gen_image.py)
  gen/audio_log.jsonl   audio generations (tools/gen/gen_audio.py)
  gen/edit_log.jsonl    edits (cutout.py, loop/trim tools)
  gen/decisions.json    {"<output path>": {"outcome": "accepted|edited|rejected", "by": "Shriram",
                         "reason": "...", "used": "godot/... (panel N)"}}
Rows without a decision are listed as "not yet judged". Rows are never deleted.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(p):
    p = ROOT / p
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def main():
    gens = load("gen/log.jsonl") + load("gen/audio_log.jsonl")
    edits = load("gen/edit_log.jsonl")
    dec = json.loads((ROOT / "gen/decisions.json").read_text()) if (ROOT / "gen/decisions.json").exists() else {}
    by_src = {}
    for e in edits:
        by_src.setdefault(e.get("src", ""), []).append(e)
    lines = ["# Asset log", "",
             "Built by `tools/gen/build_asset_log.py` from the generation logs (`gen/*.jsonl`) and the human decisions (`gen/decisions.json`).",
             "All models ran locally on a MacBook Pro M1 Pro (16 GB); licences are in SOURCES.md. Contact sheets of every candidate (accepted and rejected) are in `design/gen-contact/`.",
             "**Reproduce an image:** `mflux-generate-flux2 <cmd>` from the row. **Reproduce audio:** `tools/gen/gen_audio.py` with the same prompt and seed.", ""]
    assets = []
    for g in gens:
        if g["asset"] not in assets:
            assets.append(g["asset"])
    for a in assets:
        lines += [f"## {a}", "", "| # | Model | Prompt and settings | Outcome (who, why) | Edits | Where used |", "|---|---|---|---|---|---|"]
        for i, g in enumerate([x for x in gens if x["asset"] == a], 1):
            out = g["output"]
            d = dec.get(out, {})
            settings = f"seed {g['seed']}"
            if "width" in g:
                settings += f", {g['width']}×{g['height']}, q{g.get('quantize')}, steps {g.get('steps') or 'default'}"
                if g.get("edit_refs"):
                    settings += f", reference: `{', '.join(g['edit_refs'])}`"
            else:
                settings += f", {g.get('duration_s')} s, guidance {g.get('guidance')}" + (f", steps {g['steps']}" if g.get("steps") else "")
                if g.get("negative_prompt"):
                    settings += f", negative: \"{g['negative_prompt']}\""
            prompt = g["prompt"].replace("|", "/").replace("\n", " ")
            outcome = f"**{d['outcome']}** ({d.get('by', '?')}): {d.get('reason', '')}" if d else "not yet judged"
            ed = "; ".join(x for e in by_src.get(out, []) for x in e["edits"]) or d.get("edits", "—")
            lines.append(f"| {i} | {g['model']} | \"{prompt}\" — {settings}. Output `{out}` | {outcome} | {ed} | {d.get('used', '—')} |")
        lines.append("")
    (ROOT / "ASSET-LOG.md").write_text("\n".join(lines) + "\n")
    print("ASSET-LOG.md:", len(gens), "generations,", len(dec), "decisions")


if __name__ == "__main__":
    main()
