#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) from the CURRENT
godot/ tree, beat_sheet.json and the rendered media. Adapted from the A5 reel for A6.

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
    'scuff': ("Effect A, the sand scuff: footstep_scuff.tscn (SoftDust 10 + FineGrit 5 CPUParticles3D, one-shot, explosive, "
              "box emission, velocity/gravity/damping, scale curves, colour ramps, procedural GradientTexture2D quads, "
              "particle billboards); footstep_scuff_trigger.gd turns Hari's walked distance (_travel) into foot contacts "
              "every 0.84 m and instances a new scuff per contact (overlap, at most 4 alive), freed after 1.15 s; wired "
              "under FootstepScuffs in slice.tscn; fixture preview; tuning r1 (alpha ramp) and r2 (texture gradient).",
              ['B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10']),
    'moths': ("Effect B, moths at the string lights: string_light_moths.tscn (3 GPUParticles3D sharing one "
              "ParticleProcessMaterial with turbulence and attractor interaction, preprocess 2.4 s, plus 3 "
              "GPUParticlesAttractorSphere3D); the procedural moth texture (tools/moth_texture.gd, written to moth.tres / "
              "moth.png by tools/write_moth_texture.gd); string_light_moths_controller.gd drives emitting from "
              "LoopState.phase == NIGHT and clock_minutes < 1740, restarts on edges, hides after 2.4 s; fixture preview; "
              "tuning r1 (quad 3x), r2 (umber ramp), r3 (solid texture).",
              ['B02', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20']),
    'generated': ("particles_generated.gdshader: Godot's conversion of MothsWest's ParticleProcessMaterial, made and saved "
                  "by Shriram in the editor; unused by the game; two lines annotated by the film beside the brief settings.",
                  ['B21']),
    'tests-price': ("Configuration read-back tests (A 128 checks, B 255), the state tests (A 19, B 63) and the headless "
                    "CPU cost script with an empty-scene control; the debug keys F10/F11 used for Shriram's vsync-off "
                    "FPS comparison.",
                    ['B06', 'B20', 'B22', 'B23', 'B24']),
}

RULES = [
    ('effects/footstep_scuff.tscn', ['scuff'], 'Effect A scene: SoftDust + FineGrit CPUParticles3D'),
    ('effects/footstep_scuff_trigger.gd', ['scuff'], 'foot contacts from walked distance; one new instance per contact'),
    ('previews/footstep_scuff_preview.*', ['scuff'], 'fixture preview over the real level (fixed seed on the preview only)'),
    ('effects/string_light_moths.tscn', ['moths'], 'Effect B scene: 3 GPUParticles3D + 3 attractors'),
    ('effects/string_light_moths_controller.gd', ['moths'], 'state -> emitting / restart / hide; reads, never writes'),
    ('effects/moth.*', ['moths'], 'procedural moth texture (generated, committed)'),
    ('tools/moth_texture.gd', ['moths'], 'moth silhouette generator (r3: smoothstep)'),
    ('tools/write_moth_texture.gd', ['moths'], 'writes moth.png / moth.tres'),
    ('previews/string_light_moths_preview.*', ['moths'], 'fixture preview over the real level (seeds 101/202/303)'),
    ('scenes/slice.tscn', ['scuff', 'moths'], 'the night slice: FootstepScuffs, StringLightMoths, EffectsDebugKeys nodes'),
    ('shaders/particles_generated.gdshader', ['generated'], 'editor conversion of the moth ParticleProcessMaterial (Shriram)'),
    ('tests/test_footstep_scuff_config.gd', ['tests-price'], 'Effect A configuration read-back'),
    ('tests/test_footstep_scuff_trigger.gd', ['tests-price'], 'Effect A state test, real keys'),
    ('tests/test_string_light_moths_config.gd', ['tests-price'], 'Effect B configuration read-back'),
    ('tests/test_string_light_moths_controller.gd', ['tests-price'], 'Effect B state test, real keys'),
    ('tests/cost_effects.gd', ['tests-price'], 'headless CPU price with control'),
    ('effects/effects_debug_keys.gd', ['tests-price'], 'debug keys F10 vsync / F11 effects, for the GPU price check'),
]
EXCLUDE_REASON = ("A2/A3/A5 file (runtime, art, audio, UI, shaders, materials or earlier tests), unchanged in A6 except "
                  "where listed in a component; explained in the A2, A3 and A5 films.")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def inventory():
    return sorted(p.relative_to(GODOT).as_posix() for p in GODOT.rglob('*')
                  if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GODOT).parts) and p.suffix != '.uid')

OBSERVATIONS = {
    'B03': 'Fixture strip r0 (preview over the real level, Movie Maker 30 fps): one scuff at Hari\'s feet from file 9, gone by file 34; then Shriram\'s screenshot of the running preview.',
    'B05': 'Scripted Movie Maker capture of the real game with D held through input events: a new scuff per footfall, up to three alive at once (evidence/walk_effects_frames.txt); Shriram\'s play screenshot; the recorded state test (19/19).',
    'B07': 'Fixture strips r0 vs r1 (same seed): identical start, the puff lasts to about trig+30 instead of +20; TUNING.md prediction vs measurement and verdict.',
    'B09': "Shriram's r1 play screenshot ('cotton balls'), fixture strips r1 vs r2, TUNING.md comparison and verdict.",
    'B11': "Fixture strip r0 of the moths (present on the first active frame), Shriram's 'do you see dots there' screenshot, Claude's zoom.",
    'B13': "Claude's zooms of r1/r2 fixture frames and Shriram's live screenshots: still not visible; r2 prediction failed.",
    'B15': "Claude's 6x renders of the texture before r3 and at r3, fixture strips r2 vs r3, Shriram's r3 screenshot.",
    'B17': 'Fixture Movie Maker capture of the current preview made for the film: moths wander near the bulbs; after frame 70 they fade.',
    'B19': "Recorded controller test (63/63, selected lines), the scripted capture paused mid-walk, Shriram's pause screenshot.",
    'B22': 'Recorded mutation logs: M1 Godot 3 name fails initial_velocity_min (0.0), M2 spread drift fails; current config totals 128 and 255.',
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
        files.append({'path': rel, 'sha256': sha(GODOT / rel), 'role': rule[2], 'component_ids': list(rule[1])})
        for c in rule[1]:
            comp_files[c].append(rel)
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
