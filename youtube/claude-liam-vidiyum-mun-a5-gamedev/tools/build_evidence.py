#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) from the CURRENT
godot/ tree, beat_sheet.json and the rendered media. Adapted from the A3 reel.

  python3 tools/build_evidence.py          # fails if paired media is missing
  python3 tools/build_evidence.py --draft  # skeleton: missing media hashes left empty (pre-render)

Every inventoried file (all of godot/ except .godot/ and *.uid, as verify_gamedev.py counts them) is mapped to an
A5 component by the RULES below; files with no rule are listed as exclusions (A2/A3 scope, unchanged by A5).
"""
import fnmatch, hashlib, json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GODOT = REEL.parents[1] / 'godot'
REV = (REEL / 'evidence/source-revision.txt').read_text().split()[0]

COMPONENTS = {
    'night-skip': ("The 'night is slipping' glow: night_skip.gdshader (canvas_item, hand-written by Shriram; colour line "
                   "at line 8) on the status bar's own node (status_bar.gd, split out of hud.gd so only the bar glows), "
                   "driven every frame by night_skip_driver.gd from LoopState.fast_forward during Phase.NIGHT with "
                   "move_toward by delta (0.25 s in, 0.5 s out), checked by test_night_skip.gd at 30/60/144 fps "
                   "through real key input, including the uniform-list assertion that catches a parse failure or a rename.",
                   ['B02', 'B03', 'B04', 'B05', 'B06', 'B16', 'B17']),
    'marble': ("The marble deck: deck_marble.gdshader (spatial; albedo sampled as colour with source_color, roughness and "
               "an OpenGL normal map as data; world-XZ UVs; five ranged uniforms in two groups), two ShaderMaterials "
               "(marble_dry.tres with the defaults on three floors; marble_wet.tres, roughness 0.3 / specular 0.8, on "
               "FloorBack), wired in slice.tscn; Poly Haven Marble 01 textures with explicit import settings; the "
               "normal-map curl check calibrated on Floor Tiles 06; the material audit and its test.",
               ['B09', 'B10', 'B11', 'B12', 'B17', 'B18']),
    'hint-experiment': ("The hint experiment: write_hint_strip.gd writes a 3x1 PNG (greys 64, 128, 192) imported lossless "
                        "without mipmaps; hint_experiment.gdshader binds it to a source_color sampler and a plain one; two "
                        "materials pick one each on two quads in hint_experiment.tscn (Linear tonemap, exposure 1.0).",
                        ['B07', 'B08']),
    'language': ("Step 4: a StandardMaterial3D with albedo, roughness and normal map, converted in the editor to "
                 "standard_generated.gdshader (unused by the game) on the sphere in scratch_standard.tscn; compared "
                 "line by line with deck_marble.gdshader.",
                 ['B13', 'B14', 'B15']),
    'captures': ("tools/capture_a5.gd: scripted real-renderer captures (glow at fixed values, hint quads, marble at a "
                 "held 10 PM, the uniform sweep) that print measured pixels next to the predictions.",
                 ['B04', 'B08', 'B10']),
}

RULES = [
    ('shaders/night_skip.gdshader', 'night-skip', 'hand-written canvas_item shader (Shriram)'),
    ('materials/night_skip.tres', 'night-skip', 'ShaderMaterial on HUD/StatusBar'),
    ('ui/night_skip_driver.gd', 'night-skip', 'driver: state -> skip_amount by delta'),
    ('ui/status_bar.gd', 'night-skip', 'the status bar as its own Control (A5 split)'),
    ('ui/hud.gd', 'night-skip', 'the rest of the HUD after the status bar moved out'),
    ('tests/test_night_skip.gd', 'night-skip', 'headless rule test at 30/60/144 fps, real key input'),
    ('shaders/deck_marble.gdshader', 'marble', 'spatial marble shader (Shriram, with ChatGPT help)'),
    ('materials/marble_*.tres', 'marble', 'dry / wet ShaderMaterial'),
    ('scenes/slice.tscn', 'marble', 'the night slice: floor material_override and the StatusBar node'),
    ('assets/textures/marble_01/*', 'marble', 'Poly Haven Marble 01 (CC0), import settings, attribution'),
    ('tests/data/curl/*', 'marble', 'Floor Tiles 06 normal maps (CC0), curl calibration only'),
    ('tests/normal_map_check.gd', 'marble', "normal-map convention check (the course's curl_ratio)"),
    ('tests/test_materials.gd', 'marble', 'material audit test (audit agent, reviewed)'),
    ('MATERIALS.md', 'marble', 'material audit (audit agent, reviewed)'),
    ('shaders/hint_experiment.gdshader', 'hint-experiment', 'two samplers, one file (Shriram, with ChatGPT help)'),
    ('materials/hint_*.tres', 'hint-experiment', 'quad materials, one per bool value'),
    ('assets/textures/hint_strip_3x1.png*', 'hint-experiment', 'the 3x1 grey strip and its lossless import'),
    ('tools/write_hint_strip.gd', 'hint-experiment', 'writes the strip'),
    ('scenes/hint_experiment.tscn', 'hint-experiment', 'two quads, Linear tonemap'),
    ('shaders/standard_generated.gdshader', 'language', 'editor-generated from a StandardMaterial3D'),
    ('scenes/scratch_standard.tscn', 'language', 'scratch sphere using the generated shader'),
    ('tools/capture_a5.gd', 'captures', 'scripted real-renderer captures'),
]
EXCLUDE_REASON = ("A2/A3 file (runtime, art, audio, UI, models or earlier tests), unchanged in A5 except where noted in the "
                  "components; explained in the A2 and A3 films.")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def inventory():
    return sorted(p.relative_to(GODOT).as_posix() for p in GODOT.rglob('*')
                  if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GODOT).parts) and p.suffix != '.uid')

OBSERVATIONS = {
    'B03': 'Real-renderer captures at skip_amount 0, 0.5, 1 and 2: the bar moves toward orange; P1/P2 match the predicted on-screen blend within 1 per channel; 2.0 is not clamped.',
    'B05': 'Movie-maker capture with T held via input events: skip_amount rises over 8 frames and falls over 15 at 30 fps; Shriram\'s playtest screenshot; recorded fade timings at 30/60/144 fps.',
    'B07': 'Captured hint quads: 64/128/192 with source_color, 137/188/225 without, equal to the predictions in CHANGE-BRIEF.md 2.5.',
    'B09': 'The marble under the slice lights at a held 10 PM, and each float uniform swept to both ends of its hint_range.',
    'B11': "Shriram's editor screenshots: a shader edit darkens all four floors; a wet-material tint changes only FloorBack.",
    'B13': 'The generated shader rendering the scratch sphere with the three marble textures (camera and light added by the capture script).',
    'B16': 'Recorded logs: deleting a semicolon fails 4 checks (empty uniform list), renaming skip_amount fails 2 while the rule checks pass, removing source_color fails the material test.',
}

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
    pairs = []
    for cb in code_beats:
        rb = order[order.index(cb) + 1]
        media = beats[rb].get('shot', {}).get('evidence_media', f'media/{rb}.mp4')
        mp = REEL / media
        if not mp.exists() and not draft:
            sys.exit(f'paired media missing for {cb}->{rb}: {media}')
        pairs.append({'code_beat': cb, 'result_beat': rb, 'observation': OBSERVATIONS.get(cb, ''),
                      'media': {'path': media, 'sha256': sha(mp) if mp.exists() else ''}})
    data = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
            'game': {'project': 'godot/', 'build_id': sheet['metadata']['game']['build_id'], 'git': REV},
            'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
            'code_result_pairs': pairs}
    (REEL / 'gamedev-evidence.json').write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    print(f"wrote gamedev-evidence.json · {len(files)} files · {len(components)} components · {len(excerpts)} excerpts · "
          f"{len(pairs)} pairs · {len(exclusions)} exclusions{' (DRAFT)' if draft else ''}")

if __name__ == '__main__':
    main()
