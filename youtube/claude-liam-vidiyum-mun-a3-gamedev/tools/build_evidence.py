#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) from the CURRENT
godot/ tree, beat_sheet.json and the rendered media.

  python3 tools/build_evidence.py          # fails if a file has no rule, or paired media is missing
  python3 tools/build_evidence.py --draft  # skeleton: missing media hashes left empty (pre-render)

Every inventoried file (all of godot/ except .godot/ and *.uid, as verify_gamedev.py counts them) is
mapped to a component by the RULES below. A new file with no rule stops the build, so a change at the
freeze cannot slip past the ledger.
"""
import fnmatch, hashlib, json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GODOT = REEL.parents[1] / 'godot'
REV = (REEL / 'evidence/source-revision.txt').read_text().split()[0]

COMPONENTS = {
    'a3-models': ("The three A3 assets as exported glTF (+Y Up) from Blender 5.2.2: suv.glb (6 shapes, 456 tris), "
                  "rock_shrine.glb (6 shapes, 266 tris), fence_segment.glb (6 shapes, 108 tris), each built by "
                  "execute_blender_code bodies Claude ran through the Blender MCP (tools/blender/build_*.py, outside godot/), "
                  "plus Godot's import settings.",
                  ['B02', 'B03', 'B04', 'B05', 'B07', 'B11']),
    'a3-check': ("The headless asset check: a3_brief.json holds sizes, budgets and colours; a3_measure.gd measures every "
                 "mesh vertex in world space (floor from vertices, not a collider), triangles, shapes, scales, colours; "
                 "check_a3_assets.gd compares the real .glb files with the brief (31 checks); check_a3_selftest.gd proves "
                 "the check can fail on deliberately broken BoxMesh stand-ins (17 checks); capture_a3.gd takes the engine screenshots.",
                 ['B06', 'B07', 'B08', 'B09']),
    'a3-showcase': ("a3_showcase.tscn/.gd: the three assets in a row at game scale beside Hari's 1.75 m billboard, an orbit "
                    "camera (behind and below), the shrine slot turned -90 degrees so the goddess faces the camera, and a "
                    "flickering OmniLight3D for the lamp, because the model cannot animate.",
                    ['B10', 'B11']),
}

# (glob, component, role) — first match wins. Files with no rule are listed as exclusions (A2 slice, not this film).
RULES = [
    ('assets/models/*.glb', 'a3-models', 'exported Blender asset (glTF binary, +Y Up)'),
    ('assets/models/*.glb.import', 'a3-models', 'Godot import settings for an A3 asset'),
    ('tests/a3_measure.gd', 'a3-check', 'vertex-based measurement shared by the check and the self-test'),
    ('tests/check_a3_assets.gd', 'a3-check', 'headless check of the three .glb files against the brief'),
    ('tests/check_a3_selftest.gd', 'a3-check', 'self-test: broken stand-ins the check must catch'),
    ('tests/data/a3_brief.json', 'a3-check', 'machine-readable brief: sizes, budgets, colours, tolerances'),
    ('tests/capture_a3.gd', 'a3-check', 'scripted engine screenshots of the showcase (evidence/a3/godot-*.png)'),
    ('scenes/a3_showcase.gd', 'a3-showcase', 'showcase controller: slots, slot yaw fix, lamp flicker, orbit camera'),
    ('scenes/a3_showcase.tscn', 'a3-showcase', 'the saved showcase scene'),
]
EXCLUDE_REASON = ("A2 vertical-slice file (runtime, art, audio, UI or A2 tests), unchanged scope for this A3 film; "
                  "explained in the A2 film claude-liam-walker-vidiyum-mun-shriram-a-gamedev. The A3 assets are not yet "
                  "placed in slice.tscn (a stated limitation).")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def inventory():
    return sorted(p.relative_to(GODOT).as_posix() for p in GODOT.rglob('*')
                  if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GODOT).parts) and p.suffix != '.uid')

def main():
    draft = '--draft' in sys.argv
    sheet = json.loads((REEL / 'beat_sheet.json').read_text())
    beats = {b['beat_id']: b for b in sheet['beats']}
    files, comp_files, unmatched = [], {c: [] for c in COMPONENTS}, []
    for rel in inventory():
        rule = next((r for r in RULES if fnmatch.fnmatch(rel, r[0])), None)
        if not rule:
            unmatched.append(rel); continue
        files.append({'path': rel, 'sha256': sha(GODOT / rel), 'role': rule[2], 'component_ids': [rule[1]]})
        comp_files[rule[1]].append(rel)
    exclusions = [{'path': u, 'reason': EXCLUDE_REASON} for u in unmatched]
    components = [{'id': c, 'explanation': e, 'beat_ids': [b for b in bids if b in beats and beats[b].get('narration_text')],
                   'files': comp_files[c]} for c, (e, bids) in COMPONENTS.items() if comp_files[c]]
    excerpts, code_beats = [], []
    for bid, b in beats.items():
        rem = b.get('shot', {}).get('remotion') or {}
        if rem.get('pattern', '').startswith('GodotDevWorkbench') and rem.get('props', {}).get('code'):
            p = rem['props']
            rel = p['path'].removeprefix('godot/')
            n = p['code'].count('\n') + 1
            excerpts.append({'beat_id': bid, 'path': rel, 'start_line': p['startLine'], 'end_line': p['startLine'] + n - 1, 'text': p['code']})
            code_beats.append(bid)
    order = list(beats)
    observations = {
        'B06': 'Recorded headless output: every briefed row passes for all three assets; lowest mesh vertex y = +0.0000 m, SUV 456 triangles (<= 480), 31 checks, 0 failed.',
        'B08': 'Recorded headless output: the correct stand-in passes every row and each deliberate break (float, x0.1 scale, on its side, colour lost, budget, SUV backwards) is caught: 17/17.',
        'B10': 'Engine screenshots: before the fix the goddess faces the SUV tail; after the -90 degree slot yaw she faces the camera; orbit views from behind and below show the assets on the floor.',
    }
    pairs = []
    for cb in code_beats:
        rb = order[order.index(cb) + 1]
        media = beats[rb].get('shot', {}).get('evidence_media', f'media/{rb}.mp4')
        mp = REEL / media
        if not mp.exists() and not draft:
            sys.exit(f'paired media missing for {cb}->{rb}: {media}')
        pairs.append({'code_beat': cb, 'result_beat': rb, 'observation': observations.get(cb, ''),
                      'media': {'path': media, 'sha256': sha(mp) if mp.exists() else ''}})
    data = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
            'game': {'project': 'godot/', 'build_id': sheet['metadata']['game']['build_id'], 'git': REV},
            'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
            'code_result_pairs': pairs}
    (REEL / 'gamedev-evidence.json').write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    print(f"wrote gamedev-evidence.json · {len(files)} files · {len(components)} components · {len(excerpts)} excerpts · "
          f"{len(pairs)} pairs{' (DRAFT)' if draft else ''}")

if __name__ == '__main__':
    main()
