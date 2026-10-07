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

COMPONENTS = {
    'hari-asset': ("Hari's generated art as a game asset: ten state PNGs (FLUX.2 klein edits, rembg cutout, trim, "
                   "680 px leg-centred) shown on a fixed-Y, unshaded billboard Sprite3D sized to 1.75 m; hari.gd maps "
                   "Story.hari_state to <state>.png, walks camera-relative and flips the sprite to face left.",
                   ['B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09']),
    'night-logic': ("The loop: LoopState owns the clock (8 PM to 5:55 AM in 180 s, x8 while T is held), knowledge that "
                    "persists, per-loop flags and one-shot timeline events; Story runs dialogue and Hari's state; Controls "
                    "turns keys into logic calls; dialogue.json holds every line.",
                    ['B10', 'B11', 'B15', 'B16']),
    'sound': ("SoundBank listens to five LoopState signals (phone_buzz, clue_saved, keys_exchanged, dawn_crash, safe_dawn) "
              "and two music loops on separate buses; it never changes game state and counts every request for tests.",
              ['B03', 'B12', 'B13', 'B15']),
    'world': ("The 3D deck: slice.tscn/slice.gd build the marble deck, backdrops, NPC billboards, SUV, lights and a sky "
              "driven by the clock (revision R1 retuned the night values); a Telltale-style follow camera blends zone presets.",
              ['B02', 'B11', 'B16', 'B17', 'B18']),
    'ui': ("Screen-space twins of every sound: phone card, notes card, captions, white-out, pause overlay and end card, "
           "plus the phone-style HUD clock and mute indicators.",
           ['B11', 'B15', 'B16']),
    'intro': ("The main scene: a title screen and a four-panel intro motion comic (generated stills, captions, gaana music, "
              "the dawn horn on panel 4); Enter advances, Esc skips, then it changes to slice.tscn, where loop 1 starts itself.",
              ['B02']),
    'tests': ("Headless tests (exact sound counts over two scripted loops, loop logic, scene smoke, asset presence) and the "
              "scripted screenshot tool used for TEST-REPORT evidence; they use the test API, not played input.",
              ['B13', 'B19', 'B18']),
}

# (glob, component, role) — first match wins.
RULES = [
    ('assets/art/hari/*.png', 'hari-asset', 'generated Hari state image (FLUX.2 klein edit, edited per gen/edit_log.jsonl)'),
    ('assets/art/hari/*.import', 'hari-asset', 'import settings for a Hari state image'),
    ('assets/art/hari/.gitkeep', 'hari-asset', 'directory marker'),
    ('scenes/hari.gd', 'hari-asset', 'player body, camera-relative movement, state -> art file, facing flip'),
    ('scenes/billboard_art.gd', 'hari-asset', 'billboard Sprite3D: loads art, sizes it to height_m, feet at y = 0'),
    ('scenes/blob_shadow.gd', 'hari-asset', 'contact shadow under Hari'),
    ('logic/hari_spec.gd', 'hari-asset', "Hari's size, capsule and speed constants"),
    ('autoload/loop_state.gd', 'night-logic', 'clock, loop, knowledge, per-loop flags, timeline events'),
    ('autoload/story.gd', 'night-logic', "dialogue flow, interaction latch, Hari's state"),
    ('autoload/controls.gd', 'night-logic', 'keyboard -> logic (just-pressed polling, T fast-forward)'),
    ('logic/input_setup.gd', 'night-logic', 'key bindings registered in code'),
    ('logic/story_data.gd', 'night-logic', 'reads dialogue.json'),
    ('data/dialogue.json', 'night-logic', 'every dialogue line, caption and clue text'),
    ('project.godot', 'night-logic', 'autoload order, main scene, Forward+ renderer, window'),
    ('autoload/sound_bank.gd', 'sound', 'listens to logic signals; SFX and music buses'),
    ('default_bus_layout.tres', 'sound', 'Music and SFX buses, pause low-pass'),
    ('assets/audio/*', 'sound', 'generated audio file, import settings or directory marker'),
    ('assets/audio/*/*', 'sound', 'generated audio file, import settings or directory marker'),
    ('scenes/intro.gd', 'intro', 'title screen + intro motion comic; changes scene to the slice'),
    ('scenes/intro.tscn', 'intro', 'the main scene (project.godot run/main_scene)'),
    ('assets/art/intro/*', 'intro', 'generated intro panel still or its import settings'),
    ('tools/capture_intro.gd', 'tests', 'scripted screenshot tool for the intro'),
    ('scenes/slice.gd', 'world', 'scene controller: signals -> visuals, clock-driven sky and lights'),
    ('scenes/slice.tscn', 'world', 'the saved 3D scene'),
    ('scenes/*.gd', 'world', 'set dressing / camera / surfaces built in code'),
    ('assets/art/env/*', 'world', 'generated environment art or its import settings'),
    ('assets/art/npc/*', 'world', 'generated NPC art or its import settings'),
    ('assets/art/ui/*', 'world', 'directory marker'),
    ('assets/art/*', 'world', 'art directory content'),
    ('ui/*.gd', 'ui', 'screen-space card / HUD drawing'),
    ('tests/*', 'tests', 'headless test'),
    ('tools/capture_shots.gd', 'tests', 'scripted screenshot tool (test API)'),
    ('icon.svg*', 'night-logic', 'project icon'),
]

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
    if unmatched:
        sys.exit('No ledger rule for: ' + ', '.join(unmatched))
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
        'B08': 'In real play the call closes and PHONE becomes IDLE, then WALK and TALK: each state swaps the billboard image, at one height.',
        'B10': 'Holding T, the HUD shows >> x8 and the clock races; at 1:21 the overheard call and its clue fire once; at 1:40 at 1x Advay takes the keys once.',
        'B12': 'Recorded test output: exact per-event request counts (2/3/2/1/1), identical with both buses muted, matching the filmed run’s driver summary.',
        'B17': 'R1 before/after screenshots: lavender sky and washed-out marble become a night sky with warm pools under the string lights.',
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
            'game': {'project': 'godot/', 'build_id': sheet['metadata']['game']['build_id']},
            'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': [],
            'code_result_pairs': pairs}
    (REEL / 'gamedev-evidence.json').write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    print(f"wrote gamedev-evidence.json · {len(files)} files · {len(components)} components · {len(excerpts)} excerpts · "
          f"{len(pairs)} pairs{' (DRAFT)' if draft else ''}")

if __name__ == '__main__':
    main()
