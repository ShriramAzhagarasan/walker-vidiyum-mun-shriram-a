#!/usr/bin/env python3
"""Author beat_sheet.json for the A6 film "Vidiyum Mun, Dust and Moths" (godot-gamedev, walker mode).
Adapted from the A5 reel's author_sheet.py. Code excerpts (godot/...) are located by an anchor line and copied
verbatim (GodotDevWorkbench beats, hash-checked by verify_gamedev.py); each is followed by its result beat
(code-then-result-v1). Board excerpts from root docs and the generated shader are copied verbatim by anchor.
Re-running keeps measured audio fields for beats whose narration did not change.
"""
import json, os, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GODOT = REPO / 'godot'
sys.path.insert(0, str(REEL / 'tools'))
from source_snapshot import snapshot  # noqa: E402

TITLE = "Vidiyum Mun, Dust and Moths"
SLUG = "claude-liam-vidiyum-mun-a6-gamedev"
TOPIC = "WALKER · GODOT GAMEDEV · A6 PARTICLES"
PROJECT = "Vidiyum Mun"
BUILD, _rows = snapshot(REPO)
REV = (REEL / 'evidence/source-revision.txt').read_text().split()[0]
SAY = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
       '8': 'eight', '9': 'nine', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F'}
REV_SPOKEN = ' '.join(SAY[c] for c in REV)
FIX = "FIXTURE · preview scene over the real level · Movie Maker 30 fps · captured by Shriram"
FIXF = "FIXTURE · preview scene over the real level · Movie Maker 30 fps · captured for this film (current build)"
SCRIPTED = "SCRIPTED CAPTURE · real game, keys sent as input events · Movie Maker 30 fps · current build"
SHRIRAM = "SHRIRAM'S OWN SCREENSHOT"
CLAUDEZ = "CLAUDE'S ZOOM of fixture frames (made during tuning)"

def excerpt(root, rel, anchor, n):
    lines = (root / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    if len(hits) != 1:
        raise SystemExit(f'anchor {anchor!r} matched {len(hits)} lines in {rel}')
    s = hits[0]
    return {'path': rel, 'start_line': s + 1, 'end_line': s + n, 'text': '\n'.join(lines[s:s + n])}

def excerpt_at(root, rel, anchor, offset, n):
    """n lines starting `offset` lines after a unique anchor line."""
    lines = (root / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    if len(hits) != 1:
        raise SystemExit(f'anchor {anchor!r} matched {len(hits)} lines in {rel}')
    s = hits[0] + offset
    return {'path': rel, 'start_line': s + 1, 'end_line': s + n, 'text': '\n'.join(lines[s:s + n])}

def line_of(ex, needle):
    for i, l in enumerate(ex['text'].split('\n')):
        if needle in l:
            return ex['start_line'] + i
    raise SystemExit(f'{needle!r} not in excerpt {ex["path"]}')

def doc_line(rel, anchor):
    ex = excerpt(REPO, rel, anchor, 1)
    return ex['start_line'], ex['text']

EX = {
    'B03': excerpt(GODOT, 'effects/footstep_scuff.tscn', 'amount = 10', 13),
    'B05': excerpt(GODOT, 'effects/footstep_scuff_trigger.gd', 'func _contact_index(travel: float) -> int:', 10),
    'B07': excerpt(GODOT, 'effects/footstep_scuff.tscn', '[sub_resource type="Gradient" id="SoftColorRamp"]', 3),
    'B09': excerpt(GODOT, 'effects/footstep_scuff.tscn', '[sub_resource type="Gradient" id="SoftTexGrad"]', 11),
    'B11': excerpt_at(GODOT, 'effects/string_light_moths.tscn', '[node name="MothsWest"', 4, 13),
    'B13': excerpt(GODOT, 'effects/string_light_moths.tscn', '[sub_resource type="QuadMesh" id="MothQuad"]', 3),
    'B15': excerpt(GODOT, 'tools/moth_texture.gd', '# Tuning B r3', 5),
    'B17': excerpt(GODOT, 'effects/string_light_moths.tscn', 'attractor_interaction_enabled = true', 13),
    'B19': excerpt(GODOT, 'effects/string_light_moths_controller.gd', 'e.restart()', 13),
    'B22': excerpt(GODOT, 'tests/test_footstep_scuff_config.gd', 'check("%s spread = %.0f deg"', 4),
}
FIRE_L, FIRE_T = doc_line('CHANGE-BRIEF.md', 'The scuff should fire once for every actual footfall')
NIGHT_L, NIGHT_T = doc_line('CHANGE-BRIEF.md', '- The game phase is `NIGHT`.')
CLOCK_L, CLOCK_T = doc_line('CHANGE-BRIEF.md', '- The game clock is before 5:00 AM')
GEN = 'shaders/particles_generated.gdshader'
G232_L, G232 = doc_line('godot/' + GEN, 'params.initial_velocity_multiplier = mix(')
G434_L, G434 = doc_line('godot/' + GEN, 'USERDATA1.xyz = mix(USERDATA1.xyz, normalize(noise_direction)')
G399_L, G399 = doc_line('godot/' + GEN, 'force = gravity;')
VMIN_L, VMIN = doc_line('godot/effects/string_light_moths.tscn', 'initial_velocity_min = 0.06')
VMAX_L, VMAX = doc_line('godot/effects/string_light_moths.tscn', 'initial_velocity_max = 0.28')
TMIN_L, TMIN = doc_line('godot/effects/string_light_moths.tscn', 'turbulence_influence_min = 0.12')
TMAX_L, TMAX = doc_line('godot/effects/string_light_moths.tscn', 'turbulence_influence_max = 0.3')

def remotion(pattern, props, show, **kw):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "show": show,
            "remotion": {"pattern": pattern, "props": props}, **kw}

def workbench(bid, title, notes, cues, font=27):
    ex = EX[bid]
    return remotion("GodotDevWorkbench", {
        "mode": "code", "title": title, "project": PROJECT, "path": "godot/" + ex['path'],
        "source": f"Godot editor reconstruction · godot/{ex['path']} lines {ex['start_line']}–{ex['end_line']} · git {REV}",
        "code": ex['text'], "startLine": ex['start_line'], "codeFontSize": font,
        "inspectorLabel": "Source notes — not Inspector values", "notes": notes,
        "cue_fracs": [{"frac": f, "line": line_of(ex, needle), "label": lab} for f, needle, lab in cues],
        "cues": [], "output": [f"Godot editor reconstruction · git {REV}"]},
        [{"at": str(f), "event": f"line highlight: {lab}"} for f, _, lab in cues])

def board(title, section, excerpt_text, status, visual, cards, card_fracs, show):
    return remotion("GodotDesignBoard", {
        "title": title, "section": section, "excerpt": excerpt_text, "source": "", "status": status,
        "visualLabel": visual, "layout": "cards", "cards": cards,
        "cue_fracs": [{"frac": f, "card": i} for i, f in enumerate(card_fracs)], "cues": []}, show)

def own(bid, label, show, note, segments):
    """Own media built by tools/make_media.py from real captures, Shriram's screenshots and recorded logs."""
    return {"type": "GAMEPLAY", "class": "SHOW", "source": "own", "treatment": "none", "label": label,
            "segments": segments, "evidence_media": f"media/{bid}.mp4", "show": show, "note": note}

def still(src, label, w=1.0, crop=None):
    s = {"kind": "still", "src": src, "w": w, "label": label}
    if crop: s["crop"] = crop
    return s

def clip(src, a, b, label, speed=1.0, crop=None):
    s = {"kind": "clip", "src": src, "start_frame": a, "end_frame": b, "speed": speed, "label": label}
    if crop: s["crop"] = crop
    return s

E = 'evidence/a6/'
MOTH_CROP = [320, 40, 960, 400]       # 640x360 of the 1280x720 preview: the bulb line, enlarged 2x (labelled)

beats = [
 {"beat_id": "B00", "act": "ASK",
  "role_note": "Walker B00. Illustrative reconstruction of the ask (labelled), never a transcript.",
  "narration_text": "Vanakkam, this is Liam, in for Bear. The prompt on screen is a reconstruction, not a transcript. Assignment six for Vidiyum Mun: two particle effects, the tuning that changed them, and the tests and prices that check them.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Vanakkam, Liam", "topic": "ILLUSTRATIVE RECONSTRUCTION · NOT A TRANSCRIPT", "segment": "Vidiyum Mun · A6",
      "command": "Please use Walker to convert my game design document about Vidiyum Mun, a time-loop mystery at a beach party on ECR, Chennai, into two particle effects: a sand scuff on each of Hari's footsteps, and moths around the string lights at night. Add fixture previews, headless tests and a price check.",
      "runningText": "reading CHANGE-BRIEF.md and godot/…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["footstep_scuff.tscn · config 128/128 · state 19/19.", "string_light_moths.tscn · config 255/255 · state 63/63.",
                 "GPU time: not measurable on this Mac."]},
      [{"at": "0.05", "event": "composer; greeting"}, {"at": "0.15", "event": "topic: ILLUSTRATIVE RECONSTRUCTION"},
       {"at": "0.25", "event": "the Walker ask types"}, {"at": "0.7", "event": "three result lines"}])},
 {"beat_id": "B01", "act": "BLUF", "lead_silence_s": 0.6,
  "role_note": "Hesitant writer; single-word correction 'jump' -> 'step'.",
  "narration_text": "Two particle effects. Dust that marks every step Hari takes, and moths that circle the string lights until five A M. Then the tuning that fixed what looked wrong, and the tests and prices that check what they can.",
  "shot": remotion("BrutalistHesitantWriter", {
      "contextTitle": "What this film shows",
      "text": "Two particle effects.\nDust under every jump.\nMoths at the lights until 5 AM.",
      "triggerWords": "jump", "replacementWords": "step",
      "fontSize": 84, "lineSpacing": 2.6, "align": "center", "seed": "vidiyum-a6",
      "mistakeRate": 2, "hesitateWithin": 0, "hesitateBetween": 1, "charMs": 8,
      "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
      [{"at": "0.08", "event": "line one types"}, {"at": "0.3", "event": "'jump' struck; 'step' typed"},
       {"at": "0.55", "event": "lines two and three"}])},
 {"beat_id": "B02", "act": "SETUP",
  "role_note": "Game, both effects, their jobs, the event and the condition (CHANGE-BRIEF.md A.4 #8, B.1).",
  "narration_text": "The game is Vidiyum Mun, a time loop at a beach party in Chennai. Effect A is a sand scuff: a new burst each time Hari's foot lands, detected from the distance he has walked. Its job is to tie him to the ground. Effect B is ambience: moths around the string lights, only while the phase is night and the clock is before five A M, minute seventeen forty.",
  "shot": board("The game, two effects, two triggers",
      f"CHANGE-BRIEF.md lines {FIRE_L}, {NIGHT_L}–{CLOCK_L} (verbatim) · git {REV}",
      f"{FIRE_T.strip()}\n\nThe moths should only appear when:\n{NIGHT_T}\n{CLOCK_T}",
      "SPEC · Shriram's brief, written before the first build prompt", "Two effects",
      [{"label": "Game", "text": "Vidiyum Mun: a time loop at an ECR beach party"},
       {"label": "A · sand scuff", "text": "2 × CPUParticles3D, one-shot; a new instance per foot contact"},
       {"label": "B · moths", "text": "3 × GPUParticles3D + 3 attractors; turbulence; preprocess 2.4 s"},
       {"label": "B condition", "text": "phase == NIGHT and clock_minutes < 1740 (5:00 AM)"}],
      [0.08, 0.3, 0.6, 0.85],
      [{"at": "0.05", "event": "spec excerpt"}, {"at": "0.3", "event": "Effect A"}, {"at": "0.6", "event": "Effect B + condition"}])},
 {"beat_id": "B03", "act": "CODE",
  "role_note": "Emission / process / draw in the SoftDust node. Paired result B04 (r0 strip).",
  "narration_text": "Every particle system has three parts. Emission: when and where particles appear. Here, ten at once, one shot, from a small box at the foot. Process: how each one moves and changes. Spread, a starting speed between zero point two five and zero point six five metres a second, gravity, damping, a scale curve and a colour ramp. Draw: what each one looks like, this quad mesh, twelve centimetres, facing the camera. A second emitter, Fine Grit, adds five darker grains.",
  "shot": workbench("B03", "Emission, process, draw",
                    [{"label": "emission", "value": "amount 10 · one_shot · box"},
                     {"label": "process", "value": "velocity · gravity · ramps"},
                     {"label": "draw", "value": "mesh = SoftQuad"}],
                    [(0.1, 'amount = 10', 'emission'), (0.2, 'one_shot = true', 'one shot'),
                     (0.3, 'emission_box_extents', 'from a small box'),
                     (0.45, 'initial_velocity_min = 0.25', 'process: speed'), (0.55, 'spread = 80.0', 'process: spread'),
                     (0.75, 'mesh = SubResource("SoftQuad")', 'draw')], font=24)},
 {"beat_id": "B04", "act": "RESULT",
  "role_note": "Result of B03: the first strip r0 (fixture) and Shriram's first look.",
  "narration_text": "The first strip, r zero. A fixture: a preview scene over the real level and camera, with one scuff fired on the brief's frame ten. A cream puff at Hari's feet widens a little and is gone twenty-five frames later, under a second. Shriram watched it running, before reading any frame: the size was decent, visible on the dark floor, but the timing was way too fast.",
  "shot": own("B04", FIX,
              [{"at": "0.0", "event": "r0 strip"}, {"at": "0.6", "event": "Shriram's first look"}],
              "Fixture strip (frames cropped and enlarged), then Shriram's screenshot.",
              [still("evidence/strip_a_r0.png", f"{FIX} · r0, dark gate · cropped and enlarged", 1.6),
               still(E + "effect-a-r0-first-look/1-dark-gate-window.png", f"{SHRIRAM} · running preview, r0, dark gate", 1)])},
 {"beat_id": "B05", "act": "CODE",
  "role_note": "The trigger: foot contact from walked distance; one new instance per contact. Paired result B06.",
  "narration_text": "The game has no footstep signal, so the trigger makes one. Every frame it reads how far Hari has walked, and turns that distance into a contact count: one landing every point eight four metres, two strides. Each new contact gets a new scuff instance at his floor position, freed after one point one five seconds. A new instance, not a restart, so bursts overlap: at most four alive, sixty particles.",
  "shot": workbench("B05", "A footstep event from walked distance",
                    [{"label": "reads", "value": "hari._travel; writes nothing"},
                     {"label": "contact", "value": "every 0.84 m (2 strides)"},
                     {"label": "retrigger", "value": "new instance, overlap"}],
                    [(0.35, 'return int(floor((travel - _HALF_STRIDE) / _DOUBLE_STRIDE))', 'every 0.84 m'),
                     (0.78, 'var scuff := SCUFF_SCENE.instantiate()', 'new instance'),
                     (0.9, 'create_timer(LIFETIME_S, false)', 'freed after 1.15 s')], font=24)},
 {"beat_id": "B06", "act": "RESULT",
  "role_note": "Result of B05: scripted walk in the real game (rapid repeats), the retrigger strip, the state test log.",
  "narration_text": "Here it is in the real game: a scripted capture, D held through real input events, the trigger and effect unchanged, no fixed seed. Each footfall leaves its own puff, and up to three overlap as Hari walks. Shriram's verdict on rapid repeats in play: it stays for a while and then disappears, that is natural. The state test, with real key presses: no scuff on load, in dialogue, standing still or paused, exactly three scuffs for three contacts, two alive at once. Nineteen of nineteen.",
  "shot": own("B06", SCRIPTED,
              [{"at": "0.0", "event": "walking: overlapping scuffs"}, {"at": "0.55", "event": "Shriram's play screenshot"},
               {"at": "0.75", "event": "state test log"}],
              "Scripted capture, Shriram's screenshot, recorded test output.",
              [clip("capture/walk_effects.avi", 40, 104, f"{SCRIPTED} · D held · scuffs overlap"),
               clip("capture/walk_effects.avi", 150, 200, f"{SCRIPTED} · D held, then released"),
               still(E + "effect-a-play/r1-walking-by-pool.png", f"{SHRIRAM} · normal play (r1)", 1),
               still("evidence/terminal_trigger.png", "HEADLESS · logs/test_footstep_scuff_trigger_60fps.log · lines verbatim", 1.4)])},
 {"beat_id": "B07", "act": "CODE",
  "role_note": "Tuning A r1: the SoftDust colour ramp alphas. Paired result B08.",
  "narration_text": "Revision one changed one line, the SoftDust colour ramp. Its alpha at half its life went from zero point one eight to zero point three, and at seventy percent, from zero to zero point one five. Claude proposed it after Shriram's verdict; Shriram approved. The lifetime stayed one point one five seconds, so the overlap rule and the sixty-particle peak still hold.",
  "shot": workbench("B07", "Revision A r1: a slower fade",
                    [{"label": "50 % life", "value": "alpha 0.18 → 0.30"},
                     {"label": "70 % life", "value": "alpha 0 → 0.15"},
                     {"label": "lifetime", "value": "1.15 s, unchanged"}],
                    [(0.2, 'offsets = PackedFloat32Array(0, 0.2, 0.5, 0.7, 1)', 'life offsets'),
                     (0.5, 'colors = PackedColorArray(0.851', 'RGBA per offset')], font=24)},
 {"beat_id": "B08", "act": "RESULT",
  "role_note": "Result of B07: r0 vs r1 strips (fixture), Claude's prediction vs measurement (TUNING.md), verdict.",
  "narration_text": "Claude predicted about twice r zero's opacity, twenty frames after the trigger. Measured: one point three six times, and the puff now lasts to about one second instead of point six seven. The prediction undershot, because ten quads stack their alpha at the centre. Shriram's verdict: keep it.",
  "shot": own("B08", FIX,
              [{"at": "0.0", "event": "r0 vs r1 strip"}, {"at": "0.6", "event": "TUNING.md table"}],
              "Fixture strips before/after, then the recorded comparison rows.",
              [still("evidence/strip_a_r0_r1.png", f"{FIX} · before (r0) / after (r1), same seed · cropped and enlarged", 1.4),
               still("evidence/table_a_r1.png", "TUNING.md · Effect A r1 · rows verbatim", 1)])},
 {"beat_id": "B09", "act": "CODE",
  "role_note": "Tuning A r2: the SoftDust procedural texture gradient. Paired result B10.",
  "narration_text": "Revision two came from play. The SoftDust texture is a procedural gradient in the scene, not an image file. Its alpha went from fully opaque out to sixty percent of the radius, to zero point eight five at the centre, zero point three at forty-five percent, and zero at the edge.",
  "shot": workbench("B09", "Revision A r2: a softer texture",
                    [{"label": "texture", "value": "GradientTexture2D, radial"},
                     {"label": "was", "value": "1.0 / 0.4 / 0 at 0 / 0.6 / 1"},
                     {"label": "now", "value": "0.85 / 0.3 / 0 at 0 / 0.45 / 1"}],
                    [(0.2, 'offsets = PackedFloat32Array(0, 0.45, 1)', 'new offsets'),
                     (0.45, 'colors = PackedColorArray(1, 1, 1, 0.85', 'new alphas'),
                     (0.75, 'fill = 1', 'radial fill')], font=26)},
 {"beat_id": "B10", "act": "RESULT",
  "role_note": "Result of B09: Shriram's play screenshot (cotton balls), r1 vs r2 strips, comparison, verdict.",
  "narration_text": "Why: in the real game, Shriram saw cotton balls, and noticed the scuff lands at Hari's centre, behind the front foot, a limitation they chose to keep. Claude predicted a third to a half dimmer. Measured: thirteen to fourteen percent, but the solid lump became soft blobs. Shriram: they look like dust now, not cotton balls. Kept.",
  "shot": own("B10", FIX,
              [{"at": "0.0", "event": "Shriram's r1 play screenshot"}, {"at": "0.3", "event": "r1 vs r2 strip"}, {"at": "0.7", "event": "table"}],
              "Shriram's screenshot, fixture strips before/after, recorded rows.",
              [still(E + "effect-a-play/r1-walking-by-pool.png", f"{SHRIRAM} · r1 in normal play: 'cotton balls'", 0.8),
               still("evidence/strip_a_r1_r2.png", f"{FIX} · before (r1) / after (r2), same seed · cropped and enlarged", 1.3),
               still("evidence/table_a_r2.png", "TUNING.md · Effect A r2 · rows verbatim", 0.9)])},
 {"beat_id": "B11", "act": "CODE",
  "role_note": "Effect B emitter + attractor: emission, preprocess, draw, attractor. Paired result B12.",
  "narration_text": "Effect B uses GPU particles: twelve moths per emitter, three emitters, thirty-six in all. Lifetime two point four seconds, and preprocess two point four: the system simulates one full lifetime before the first frame, so the moths are already there. Beside each emitter sits an attractor sphere, radius one metre, strength zero point three, a weak pull toward its bulb.",
  "shot": workbench("B11", "Moths: GPU emitter + attractor",
                    [{"label": "emission", "value": "12 × 3 emitters = 36"},
                     {"label": "preprocess", "value": "2.4 s = one lifetime"},
                     {"label": "attractor", "value": "r 1.0 m · strength 0.3"}],
                    [(0.25, 'lifetime = 2.4', 'lifetime 2.4 s'),
                     (0.38, 'preprocess = 2.4', 'preprocess: one lifetime'),
                     (0.6, 'process_material = SubResource("MothPM")', 'process'),
                     (0.7, 'draw_pass_1 = SubResource("MothQuad")', 'draw')], font=24)},
 {"beat_id": "B12", "act": "RESULT",
  "role_note": "Result of B11: r0 moth strip (fixture), Shriram's first look, Claude's zoom.",
  "narration_text": "The r zero strip, a fixture over the real level: moths present on the first active frame, as preprocess predicts, clustered at all three spans. But Shriram could not see them: do you see dots there? Zoomed, each moth was a one to three pixel speck. And the bulbs hang in front of the pale villa wall, not the dark sky the brief planned for.",
  "shot": own("B12", FIX,
              [{"at": "0.0", "event": "r0 strip"}, {"at": "0.45", "event": "Shriram's first look"}, {"at": "0.75", "event": "Claude's zoom"}],
              "Fixture strip, Shriram's screenshot, Claude's zoom.",
              [still("evidence/strip_b_r0.png", f"{FIX} · r0 · bulb line cropped and enlarged", 1.3),
               still(E + "effect-b-r0-first-look/1-preview-live.png", f"{SHRIRAM} · running preview, r0: 'do you see dots there'", 1),
               still(E + "effect-b-r0-first-look/claude-zoom-frame8-vs-30-middle-span.png", f"{CLAUDEZ} · r0, before vs with moths", 0.9)])},
 {"beat_id": "B13", "act": "CODE",
  "role_note": "Tuning B r1 (quad 3x) and r2 (dark umber ramp). Paired result B14.",
  "narration_text": "Two changes followed. Revision one tripled the quad, to twenty-one by thirteen and a half centimetres. Revision two turned the colour ramp from cream to dark umber, to stand out against the pale wall. Claude proposed both, and Shriram approved both.",
  "shot": workbench("B13", "Revisions B r1 and r2: bigger, then darker",
                    [{"label": "r1 quad", "value": "0.07×0.045 → 0.21×0.135 m"},
                     {"label": "r2 ramp", "value": "cream → umber #3B2F25"},
                     {"label": "alphas", "value": "unchanged"}],
                    [(0.2, 'size = Vector2(0.21, 0.135)', 'r1: 3× quad'),
                     ], font=30)},
 {"beat_id": "B14", "act": "RESULT",
  "role_note": "Result of B13: Claude's zooms r1/r2, Shriram's live screenshots; the r2 prediction failed.",
  "narration_text": "Revision one, zoomed: two wing dots and a body line, but live, Shriram still could not see them. Revision two: Claude predicted dark shapes that stand out clearly. They came out as faint grey smudges. That prediction failed, and Shriram still saw no moths.",
  "shot": own("B14", CLAUDEZ,
              [{"at": "0.0", "event": "r1 zoom + live"}, {"at": "0.5", "event": "r2 zoom + live: failed"}],
              "Claude's zooms of fixture frames, Shriram's live screenshots.",
              [still("evidence/table_b_r2.png", "The r2 change, verbatim: string_light_moths.tscn and CHANGE-BRIEF.md revision 4", 0.8),
               still(E + "effect-b-r0-first-look/claude-zoom-r1-frame29-middle-span.png", f"{CLAUDEZ} · r1, file 29, 4×", 0.8),
               still(E + "effect-b-r0-first-look/3-r1-live-shriram.png", f"{SHRIRAM} · r1 live: still not visible", 0.9),
               still(E + "effect-b-tuning/claude-zoom-r0-r1-r2-file29.png", f"{CLAUDEZ} · r0 / r1 / r2 at file 29 · r2 PREDICTION FAILED", 0.9),
               still(E + "effect-b-tuning/r2-live-shriram-1.png", f"{SHRIRAM} · r2 live: still no visible moths", 0.8)])},
 {"beat_id": "B15", "act": "CODE",
  "role_note": "Root cause: the agent-made moth texture; r3 smoothstep lines. Paired result B16.",
  "narration_text": "The real cause was the texture. A Step five agent wrote this generator, and its wings used a squared falloff: sixteen of two thousand five hundred sixty texels above zero point eight alpha. Mostly haze. Size and colour were multiplying an almost transparent image. Revision three uses smoothstep: solid wings and body, with a narrow soft edge.",
  "shot": workbench("B15", "Revision B r3: the texture was haze",
                    [{"label": "before r3", "value": "16 / 2560 texels > 0.8 α"},
                     {"label": "r3", "value": "smoothstep: 794 texels"},
                     {"label": "written by", "value": "Step 5 agent; r3 by Claude"}],
                    [(0.25, 'var wing_mask := smoothstep(1.0, 0.85', 'solid wings'),
                     (0.55, 'var body_mask := smoothstep(1.0, 0.8, body_d)', 'solid body'),
                     (0.8, 'var alpha := clampf(wing_mask + body_mask', 'alpha')], font=28)},
 {"beat_id": "B16", "act": "RESULT",
  "role_note": "Result of B15: texture before/after (Claude's 6x renders), r3 strip (fixture), Shriram's r3 live, verdict.",
  "narration_text": "Seven hundred ninety-four solid texels instead of sixteen. In the r three strip, changed pixels at file twenty-nine rose from thirteen seventy-nine to fifty-one oh eight: two-winged shapes at every span. They read pale grey, not dark umber as predicted. Shriram's verdict: it reads as moths.",
  "shot": own("B16", FIX,
              [{"at": "0.0", "event": "texture before / after"}, {"at": "0.3", "event": "r3 strip"}, {"at": "0.7", "event": "Shriram's r3 live"}],
              "Texture renders, fixture strip, Shriram's screenshot.",
              [still("evidence/texture_before_after.png", "CLAUDE'S 6× RENDERS of the moth texture · before r3 (16 texels > 0.8 α) / r3 (794)", 0.9),
               still("evidence/strip_b_r2_r3.png", f"{FIX} · r2 / r3 · bulb line cropped and enlarged", 1.2),
               still(E + "effect-b-tuning/r3-live-shriram.png", f"{SHRIRAM} · r3 live: 'it reads as moths'", 1)])},
 {"beat_id": "B17", "act": "CODE",
  "role_note": "The feature A doesn't use: attractor interaction + turbulence. Paired result B18.",
  "narration_text": "This is what Effect A doesn't use. Attractor interaction is on, and turbulence: a noise field with strength zero point four five and scale five, whose influence on each moth's velocity is drawn between zero point one two and zero point three. CPU particles in this build have neither.",
  "shot": workbench("B17", "What A doesn't have: turbulence + attractor",
                    [{"label": "attractor", "value": "interaction enabled"},
                     {"label": "noise", "value": "strength 0.45 · scale 5"},
                     {"label": "influence", "value": "0.12 – 0.30 per moth"}],
                    [(0.15, 'attractor_interaction_enabled = true', 'attractors'),
                     (0.4, 'turbulence_enabled = true', 'turbulence'),
                     (0.55, 'turbulence_noise_strength = 0.45', 'strength'),
                     (0.75, 'turbulence_influence_min = 0.12', 'influence')], font=24)},
 {"beat_id": "B18", "act": "RESULT",
  "role_note": "Result of B17: fixture Movie Maker capture of the current preview, in motion (made for this film).",
  "narration_text": "A fixture capture of the current build, made for this film with the preview's fixed seeds. The moths wander and change direction instead of flying straight lines, and stay near their bulbs. At frame seventy the night condition ends: emission stops, and the moths fade out over their remaining life.",
  "shot": own("B18", FIXF,
              [{"at": "0.0", "event": "moths wander (real time)"}, {"at": "0.5", "event": "condition ends at frame 70: fade"}],
              "Fixture motion capture, bulb line enlarged.",
              [clip("capture/moths_r3_preview.avi", 10, 68, f"{FIXF} · bulb line cropped and enlarged · real time", crop=MOTH_CROP),
               clip("capture/moths_r3_preview.avi", 10, 68, f"{FIXF} · the same frames at HALF SPEED", speed=0.5, crop=MOTH_CROP),
               clip("capture/moths_r3_preview.avi", 68, 150, f"{FIXF} · from frame 70 the condition is off · HALF SPEED", speed=0.5, crop=MOTH_CROP)])},
 {"beat_id": "B19", "act": "CODE",
  "role_note": "The controller: reads state, drives emitting only, restart on edges, hide after 2.4 s. Paired result B20.",
  "narration_text": "The controller reads the game state and never writes it. Night, before minute seventeen forty, and visible: then emitting. When the condition turns on, or the group is shown again, restart, so preprocess refills it. When it ends, emitting goes false, and two point four seconds of pausable game time later, the group is hidden. It never touches amount or amount ratio.",
  "shot": workbench("B19", "Start, stop, hide: the moth controller",
                    [{"label": "reads", "value": "phase, clock_minutes"},
                     {"label": "drives", "value": "emitting only"},
                     {"label": "ends", "value": "hide after 2.4 s"}],
                    [(0.12, 'e.restart()', 'restart: preprocess refills'),
                     (0.5, 'e.emitting = active and vis', 'emitting only'),
                     (0.7, '_fade_remaining = LIFETIME_S', '2.4 s fade'),
                     (0.8, 'visible = false', 'hidden')], font=24)},
 {"beat_id": "B20", "act": "RESULT",
  "role_note": "Result of B19: controller test log, scripted capture paused mid-walk, Shriram's pause screenshot.",
  "narration_text": "The state test, with real E, P and T keys: sixty-three of sixty-three. P freezes the emitters. Hidden stops emission, and shown restarts it. Holding T to five A M stops emission, and hides the group two point four seconds later. In the scripted capture, P pauses mid-walk, and scuffs and moths hold still. Shriram checked it in play: they stay exactly where we paused.",
  "shot": own("B20", "HEADLESS · logs/test_string_light_moths_controller_60fps.log · lines verbatim",
              [{"at": "0.0", "event": "state test log"}, {"at": "0.4", "event": "scripted pause"}, {"at": "0.75", "event": "Shriram's pause screenshot"}],
              "Recorded output, scripted capture, Shriram's screenshot.",
              [still("evidence/terminal_controller.png", "HEADLESS · logs/test_string_light_moths_controller_60fps.log · lines verbatim", 1.1),
               clip("capture/walk_effects.avi", 96, 152, f"{SCRIPTED} · P pressed: the tree is paused (frozen)"),
               still(E + "use-it/paused-moths-and-scuffs-frozen.png", f"{SHRIRAM} · paused in play: moths and scuffs frozen", 1)])},
 {"beat_id": "B21", "act": "COMPARE",
  "role_note": "Two annotated lines of particles_generated.gdshader beside the settings they implement. Annotation is the film's (Claude's).",
  "narration_text": "Shriram converted the moth material to shader code in the editor. The notes here are this film's explanation, not Shriram's. Line two thirty-two picks each moth's starting speed: a random mix between the minimum and maximum, the brief's zero point zero six and zero point two eight metres a second. Line four thirty-four is turbulence: velocity bends toward the noise direction by that moth's influence, between zero point one two and zero point three. And line three ninety-nine starts each frame's force from gravity, which the brief set to zero.",
  "shot": board("The process shader Godot generated",
      f"particles_generated.gdshader (generated by Godot, saved by Shriram) and string_light_moths.tscn, verbatim · git {REV}",
      f"{G232_L}: {G232.strip()}\n  tscn:{VMIN_L} {VMIN}  ·  tscn:{VMAX_L} {VMAX}\n\n{G434_L}: {G434.strip()}\n  tscn:{TMIN_L} {TMIN}  ·  tscn:{TMAX_L} {TMAX}",
      "ANNOTATION BY THIS FILM (CLAUDE) · not Shriram's notes", "What the lines do",
      [{"label": f"line {G232_L}", "text": "random start speed between min and max (0.06–0.28 m/s)"},
       {"label": f"line {G434_L}", "text": "turbulence: bend velocity toward the noise, by 0.12–0.30"},
       {"label": f"line {G399_L}", "text": "force starts from gravity: (0, 0, 0) for the moths"},
       {"label": "names", "text": "initial_velocity_min arrives as uniform initial_linear_velocity_min"}],
      [0.12, 0.45, 0.75, 0.88],
      [{"at": "0.05", "event": "two line pairs"}, {"at": "0.75", "event": "gravity line"}])},
 {"beat_id": "B22", "act": "CODE",
  "role_note": "Config read-back test: spread and initial_velocity_min checks. Paired result B23 (mutations).",
  "narration_text": "The configuration tests load each saved scene and read every setting back against the brief. Effect A: one hundred twenty-eight checks. Effect B: two hundred fifty-five, including turbulence, the attractors, and the solid texture. Here are two of A's: spread, and the minimum starting speed.",
  "shot": workbench("B22", "Read every setting back",
                    [{"label": "A config", "value": "128/128"},
                     {"label": "B config", "value": "255/255"},
                     {"label": "shown", "value": "spread · initial_velocity_min"}],
                    [(0.4, 'check("%s spread = %.0f deg"', 'spread'),
                     (0.75, 'check("%s initial_velocity_min', 'initial_velocity_min')], font=30)},
 {"beat_id": "B23", "act": "RESULT",
  "role_note": "Result of B22: the two mutations' recorded logs (Shriram), config totals.",
  "narration_text": "Shriram broke Effect A twice. First, the Godot three name: initial velocity, instead of initial velocity min. The scene loaded with no error, the effect still fired, and the value silently read zero. The test failed, exit one. Second, spread eighty changed to thirty, the brief unchanged: caught as drift, exit one.",
  "shot": own("B23", "HEADLESS · logs/a6-mutations/*.log · recorded output, verbatim lines",
              [{"at": "0.0", "event": "M1 Godot 3 name"}, {"at": "0.5", "event": "M2 drift"}],
              "Recorded output, not reconstructed.",
              [still("evidence/terminal_mutations.png", "HEADLESS · logs/a6-mutations/*.log and the passing config logs · lines verbatim", 1)])},
 {"beat_id": "B24", "act": "PRICE",
  "role_note": "Headless CPU price (cost log) and the GPU price (Shriram's Visual Profiler screenshots, TEST-REPORT A6.6).",
  "narration_text": "The prices. Headless CPU time per frame, three hundred samples each. The empty-scene control: five point eight microseconds. Effect A adds thirteen point two, well inside its zero point one five millisecond budget. Effect B adds three point three, within noise: headless Godot uses a dummy renderer that runs no GPU particle process, so a GPU effect's headless price is near zero by construction. On the GPU, the Visual Profiler read zero point zero milliseconds on every row, on Metal on an M one Pro. GPU time could not be measured. With vsync off: about two eighty frames a second with both effects off, two sixty to two seventy with both on. That's roughly point one three to point two eight milliseconds for both together. Each effect's budget is not confirmed.",
  "shot": own("B24", "HEADLESS · logs/cost_effects_60fps.log · lines verbatim",
              [{"at": "0.0", "event": "cost log"}, {"at": "0.45", "event": "Visual Profiler: GPU 0.0 ms"}, {"at": "0.8", "event": "A6.6 rows"}],
              "Recorded output, Shriram's profiler screenshots, the recorded report.",
              [still("evidence/terminal_cost.png", "HEADLESS · logs/cost_effects_60fps.log · lines verbatim", 1.3),
               still(E + "use-it/visual-profiler-B-heaviest.png", f"{SHRIRAM} · Visual Profiler, B heaviest: GPU column 0.0 ms on every row", 1),
               still("evidence/table_gpu.png", "TEST-REPORT.md A6.6 · lines verbatim", 1.2)])},
 {"beat_id": "B25", "act": "LIMITS",
  "role_note": "Agent mistakes caught; Claude's readings Shriram overruled (A6.8); what headless can't show.",
  "narration_text": "What the agents got wrong, and how each was caught. The Step one agent hit its turn limit and left CLAUDE dot M D at one twenty-four lines, over the limit. The Step two preview drew a reconstructed background, not the real level, with no fixed seed. The state test's at least three scuffs couldn't catch a double fire, so an exact check replaced it. The moth texture was mostly haze. The B wiring plan called ambience a feedback loop and drove amount ratio; Shriram's correction was emitting only. And agents kept trying commands outside their allow list, and were denied. Claude was overruled too: Shriram judged r zero too fast, found the cotton balls, and couldn't see the moths three times before Claude found the texture.",
  "shot": board("What the agents got wrong",
      f"Quoted verbatim from commit messages, TUNING.md and prompts/a6/ · git {REV}",
      "41302d8: \u201cerror_max_turns at 41/40\u201d; \u201cdraft is 124 lines, over the 120 limit\u201d\na17cc65: \u201cdrew a reconstructed background\u201d \u2026 \u201cand had no fixed seed\u201d\nc9a07cd: \u201c'walking fired >= 3' could not catch a double fire\u201d\nTUNING.md:161: \u201cmostly haze\u201d\nsession-6a.jsonl: \u201cfeedback loop drives `amount_ratio` only\u201d\nd5d60fb: \u201c16 permission denials\u201d",
      "REVIEW · each fix came from a reading, a test or Shriram's eyes", "Claude, overruled (A6.8)",
      [{"label": "A r0", "text": "Claude: matches the brief · Shriram: 'way too fast'"},
       {"label": "A r1", "text": "the cotton balls came from Shriram's play"},
       {"label": "B r0–r2", "text": "Claude blamed size, then contrast; the texture was haze"},
       {"label": "Headless", "text": "dummy renderer: never the look"}],
      [0.72, 0.8, 0.88, 0.95],
      [{"at": "0.05", "event": "mistakes list"}, {"at": "0.72", "event": "overruled readings"}])},
 {"beat_id": "B26", "act": "CREDITS",
  "role_note": "Who did what (SOURCES.md 'Assignment 6', brief header); texture sources; game-source revision on screen.",
  "narration_text": f"Who did what. Shriram chose both effects and the retrigger rule, wrote the brief with ChatGPT's help on wording and the price predictions, approved every tuning change, captured every strip, ran the mutations, and gave every verdict and play check. Claude Code, through scoped agent sessions and an interactive session, built the scenes, previews, trigger and controller, the tests and the cost script, read the strips, and proposed the changes. Every texture is procedural: gradients in the scuff scene, and a moth drawn by a script. No outside art. Source revision {REV_SPOKEN}.",
  "shot": board("Who did what",
      f"Quoted verbatim from CHANGE-BRIEF.md and SOURCES.md · game source git {REV}",
      "CHANGE-BRIEF.md:8-9: \u201cShriram chose the two effects and the retrigger rule from options Claude laid out.\u201d\nSOURCES.md:149-150: \u201cChatGPT's help on **the wording and structure** and on **the price predictions**\u201d\nSOURCES.md:154-155: ChatGPT \u201chelped me plan the effect settings and explain the generated process shader\u201d\nCHANGE-BRIEF.md:213: \u201cThe texture should be created procedurally, so I don't need an external image.\u201d",
      f"CREDITS · source revision {REV}", "Who did what in A6",
      [{"label": "Shriram (ChatGPT helped: wording, settings, price predictions)", "text": "effects + retrigger rule; brief; approved every change; captured every strip; mutations; every verdict"},
       {"label": "Claude Code", "text": "scoped claude -p agents + interactive session: scenes, previews, trigger, controller, tests, cost script; strip readings; proposals; this film"},
       {"label": "Narration · revision", "text": f"Kokoro am_onyx (\"Liam\"), local · git {REV}"}],
      [0.05, 0.45, 0.85],
      [{"at": "0.05", "event": "Shriram"}, {"at": "0.45", "event": "Claude Code"}, {"at": "0.85", "event": "revision"}])},
 {"beat_id": "B27", "act": "VERDICT", "lead_silence_s": 0.4,
  "role_note": "Verdict: checked / uncertain / limits / next.",
  "narration_text": "Let's recap with Claude. Checked: both effects match the brief's settings, fire and stop on the right conditions, and freeze on pause, and every tuning round ended with Shriram's verdict. Uncertain: GPU time per effect, which this Mac's profiler never reported, and why stop and play again failed for the moths. Limits: the scuff lands at Hari's centre, behind the front foot. Next: measure GPU time on a machine whose profiler reports it.",
  "shot": remotion("ClaudeVerdictArtifact", {
      "artifactTitle": "Verdict", "artifactHeading": f"Vidiyum Mun A6 particles, git {REV}.", "brandLabel": "@NikBearBrown",
      "artifactLines": ["Checked: settings 128 + 255, states 19 + 63, pause, tuning verdicts.",
                        "Uncertain: GPU time per effect; Stop + Play again (moths).",
                        "Limits: the scuff lands at Hari's centre, behind the front foot.",
                        "Next: GPU time on a machine whose profiler reports it."]},
      [{"at": "0.1", "event": "verdict card"}, {"at": "0.25", "event": "checked"}, {"at": "0.5", "event": "uncertain"},
       {"at": "0.7", "event": "limits"}, {"at": "0.85", "event": "next"}])},
 {"beat_id": "B28", "act": "HANDOFF",
  "role_note": "Your Turn: prompt read aloud; one bounded change + prediction; signs off.",
  "narration_text": "Your turn. Pick one event in your game, and write down what a particle burst should say about it, with its timings, before any node exists. Ask Claude for the scene, and a test that reads every setting back. Then rename one property to its Godot three name, and watch the test fail. Liam, in for Bear.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Your turn.", "topic": TOPIC, "segment": "Your One Effect",
      "command": "I wrote a brief for one particle effect on one event in my game: amount, lifetime, ramps and when it fires. Build the scene, and a headless test that loads it and reads every setting back against my brief. I predict a Godot 3 property name will fail it.",
      "runningText": "paste this into Claude…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["You write the brief and the timings.", "Claude writes the scene + test.", "Rename one property: it must fail."],
      "animateTyping": True},
      [{"at": "0.05", "event": "'Your turn.'"}, {"at": "0.1", "event": "prompt types"}, {"at": "0.75", "event": "result lines"}])},
 {"beat_id": "B29", "act": "OUTRO", "kind": "outro_voice", "tail_hold_s": 1.0,
  "role_note": "OUTRO-LOCK: ClaudeTitleOutro, exact title, @NikBearBrown, slug-seeded mascot; spoken, no jingle.",
  "narration_text": TITLE + ". At Nik Bear Brown.",
  "shot": remotion("ClaudeTitleOutro", {"title": TITLE, "slug": SLUG},
      [{"at": "0.0", "event": "title card"}, {"at": "0.3", "event": "@NikBearBrown + mascot"}])},
]

# Tightened narration (film length 5-7 min); every number checked in FACTCHECK.md.
NARR = {
 "B00": "Vanakkam, this is Liam, in for Bear. The prompt on screen is a reconstruction, not a transcript. Assignment six for Vidiyum Mun: two particle effects, and how they were tuned and tested.",
 "B01": "Two effects. Dust under every step Hari takes, and moths at the string lights until five A M. Then the tuning, the tests, and the prices.",
 "B02": "Vidiyum Mun is a time loop at a beach party in Chennai. Effect A, a sand scuff, fires each time Hari's foot lands, to tie him to the ground. Effect B, moths at the string lights, is ambience: only while it's night, before five A M, minute seventeen forty.",
 "B03": "Every particle system has three parts. Emission: when and where. Ten particles at once, one shot, from a small box at the foot. Process: how each moves and changes. Speed, gravity, damping, a scale curve, a colour ramp. Draw: what each looks like. This quad mesh, twelve centimetres, facing the camera.",
 "B04": "The first strip, r zero: a fixture, a preview over the real level, firing one scuff. A cream puff, gone in under a second. Shriram watched it running: size decent, visible on the dark floor, but way too fast.",
 "B05": "The game has no footstep signal, so the trigger makes one. It reads how far Hari has walked, and counts a landing every point eight four metres. Each landing gets a new scuff instance, freed after one point one five seconds. New, not restarted, so bursts overlap: at most four.",
 "B06": "In the real game, a scripted capture with D held through input events: each footfall leaves its own puff, up to three at once. Shriram, in play: it stays a while, then disappears; natural. The state test, with real keys: no scuff on load, in dialogue, idle or paused, exactly one per contact. Nineteen of nineteen.",
 "B07": "Revision one changed one line, the colour ramp. Alpha at half its life went from zero point one eight to zero point three; at seventy percent, from zero to zero point one five. Claude proposed it; Shriram approved. The lifetime stayed, so the overlap limit holds.",
 "B08": "Claude predicted twice r zero's opacity, twenty frames in. Measured: one point three six times, and the puff now lasts about a second. Ten quads stack their alpha. Shriram: keep it.",
 "B09": "Revision two came from play. The texture is a gradient in the scene, not an image file. Its alpha went from solid out to sixty percent of the radius, to zero point eight five at the centre, fading to zero.",
 "B10": "In the game Shriram saw cotton balls, and the scuff landing behind the front foot, a limitation they kept. Claude predicted a third to a half dimmer; measured, thirteen to fourteen percent. But the lump became soft blobs. Shriram: they look like dust now. Kept.",
 "B11": "Effect B is GPU particles: twelve moths per emitter, three emitters. Preprocess two point four seconds, one full lifetime, simulated before the first frame, so the moths are already there. Beside each emitter, an attractor sphere: radius one metre, strength zero point three.",
 "B12": "The r zero strip. Claude's difference image found moths at all three spans from the first active frame. But Shriram couldn't see them: do you see dots there? Each moth was a one to three pixel speck, in front of the pale villa wall, not the dark sky the brief expected.",
 "B13": "Revision one tripled the quad. Revision two turned the colour ramp from cream to dark umber. Claude proposed both; Shriram approved both.",
 "B14": "Revision one, zoomed: wing dots, but live, still invisible. Revision two: Claude predicted dark shapes standing out clearly. They came out as faint grey smudges. That prediction failed.",
 "B15": "The real cause was the texture. A Step five agent wrote this generator with a squared falloff: sixteen of two thousand five hundred sixty texels above zero point eight alpha. Mostly haze. Revision three uses smoothstep: solid wings and body.",
 "B16": "Seven hundred ninety-four solid texels. In the r three strip, two-winged shapes at every span; changed pixels at file twenty-nine up from thirteen seventy-nine to fifty-one oh eight. Pale grey, not dark as predicted. Shriram: it reads as moths.",
 "B17": "Here's what Effect A doesn't use. Attractor interaction, and turbulence: a noise field, strength zero point four five, whose influence on each moth is drawn between zero point one two and zero point three.",
 "B18": "A fixture capture made for this film, current build, fixed seeds. The moths wander and turn, and stay near their bulbs. At frame seventy the condition ends: emission stops, and they fade out.",
 "B19": "The controller reads the game state, never writes it. Night, before minute seventeen forty, and visible: emitting. Turned on or shown again: restart, so preprocess refills the group. When it ends, emitting stops, and two point four seconds later the group hides.",
 "B20": "The state test, with real keys: sixty-three of sixty-three. Pause freezes the emitters; hiding stops them; holding T to five A M stops emission, then hides the group. In the scripted capture, pause holds everything still. Shriram, in play: they stay exactly where we paused.",
 "B21": "Shriram converted the moth material to shader code in the editor. These notes are the film's, not Shriram's. Line two thirty-two picks each moth's starting speed, between the brief's minimum and maximum. Line four thirty-four bends its velocity toward the turbulence noise, by its influence. And line three ninety-nine starts from gravity, zero here.",
 "B22": "The configuration tests load each scene and read every setting back against the brief. Effect A: one hundred twenty-eight checks. Effect B: two hundred fifty-five. Here are two: spread, and minimum speed.",
 "B23": "Shriram broke Effect A twice. The Godot three name, initial velocity: no load error, the effect still fired, and the speed silently read zero. Exit one. Then spread, eighty to thirty: caught as drift. Exit one.",
 "B24": "The prices. Headless CPU per frame, against an empty-scene control of five point eight microseconds. Effect A adds thirteen point two, inside its budget. Effect B adds three point three, within noise: the dummy renderer runs no GPU particle process. And the Visual Profiler read zero milliseconds of GPU on every row, so GPU time could not be measured here. With vsync off, both effects together cost about point one three to point two eight milliseconds. Per-effect budgets: not confirmed.",
 "B25": "What the agents got wrong. Step one ran out of turns and left a draft over its line limit. Step two's preview drew a reconstructed background, not the real level. A test couldn't catch a double fire. The moth texture was haze. The wiring plan called ambience a feedback loop. And agents tried commands outside their allow list. Claude was overruled too: r zero too fast, the cotton balls, and three rounds of invisible moths.",
 "B26": f"Who did what. Shriram chose both effects, wrote the brief with ChatGPT's help on wording, effect settings and price predictions, approved every change, captured every strip, ran the mutations, and gave every verdict. Claude Code and its scoped agents built the scenes, code and tests, and read the strips. Every texture is procedural. Source revision {REV_SPOKEN}.",
 "B27": "Let's recap with Claude. Checked: settings, start, stop and pause, and every tuning verdict. Uncertain: GPU time per effect. Limit: the scuff lands at Hari's centre. Next: measure GPU time on a machine whose profiler reports it.",
 "B28": "Your turn. Brief one particle effect for one event in your game, with timings, before any node exists. Ask Claude for the scene, and a test that reads every setting back. Then use a Godot three name, and watch it fail. Liam, in for Bear.",
}
for b in beats:
    if b["beat_id"] in NARR:
        b["narration_text"] = NARR[b["beat_id"]]

OWN_QC = {
    "contrast_regions": [{"label": "caption band (film label)", "box": [0.074, 0.905, 0.62, 0.955]}],
    "contrast_reason": "Real captures, Shriram's screenshots and recorded logs reframed inside title-safe; the film's essential text is the caption band. Text inside the evidence is inspected by eye in _qc frame samples."}
for b in beats:
    if b["shot"].get("source") == "own":
        b["qc"] = OWN_QC
    if b["beat_id"] == "B01":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend."}

sheet_path = REEL / "beat_sheet.json"
old = {b["beat_id"]: b for b in json.loads(sheet_path.read_text()).get("beats", [])} if sheet_path.exists() else {}
for b in beats:
    b.setdefault("voice", "am_onyx"); b.setdefault("engine", "kokoro")
    prev = old.get(b["beat_id"])
    if prev and prev.get("narration_text") == b["narration_text"]:
        for k in ("audio_file", "actual_duration_s", "speech_duration_s", "render_duration_s"):
            if k in prev: b[k] = prev[k]
    rem, prem = b["shot"].get("remotion"), (prev or {}).get("shot", {}).get("remotion")
    strip = lambda p: {k: v for k, v in (p or {}).items() if k not in ("durationSeconds", "cues")}
    if rem and prem and "rendered" in prem and strip(rem["props"]) == strip(prem.get("props")) \
            and prev.get("narration_text") == b["narration_text"]:
        rem["rendered"] = prem["rendered"]
        if "durationSeconds" in prem.get("props", {}):
            rem["props"]["durationSeconds"] = prem["props"]["durationSeconds"]
            rem["props"]["cues"] = prem["props"].get("cues", [])

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "mode": "walker",
    "brand": "claude-liam", "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "crop",
    "captions": False, "channel": "@NikBearBrown", "channel_title": "@NikBearBrown", "folderLabel": "@NikBearBrown",
    "greeting": "Vanakkam, Liam", "greeting_note": "hello lexicon: Vanakkam (Tamil), fits the Chennai setting.",
    "persona": "Liam (in for Bear)", "in_for_bear": True,
    "audience": "CSYE 7270 reviewers and makers building their first Godot particle effects",
    "source_revision": REV,
    "game": {"name": "walker-vidiyum-mun-shriram-a", "build_id": BUILD, "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
             "renderer": "Forward+ (Metal)", "git": REV},
    "fps": 30},
  "beats": beats}
sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
words = sum(len(b['narration_text'].split()) for b in beats)
print(f"wrote {sheet_path.name} · {len(beats)} beats · {words} words (~{words / 2.7:.0f} s) · git {REV}")
for k, e in EX.items():
    print(f"  {k}: godot/{e['path']} {e['start_line']}–{e['end_line']}")
