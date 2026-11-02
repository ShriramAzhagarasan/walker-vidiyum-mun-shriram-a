#!/usr/bin/env python3
"""Author beat_sheet.json for the A5 film "Vidiyum Mun, the Night Is Slipping" (godot-gamedev, walker mode).

Code excerpts (godot/...) are located by an anchor line and copied verbatim; they are GodotDevWorkbench code beats,
hash-checked by verify_gamedev.py, and each is followed by its result beat (code-then-result-v1). Design-board
excerpts from root docs (CHANGE-BRIEF.md) are also copied verbatim by anchor, with path and line numbers on screen.
Re-running keeps measured audio fields for beats whose narration did not change.
"""
import json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GODOT = REPO / 'godot'
sys.path.insert(0, str(REEL / 'tools'))
from source_snapshot import snapshot  # noqa: E402

TITLE = "Vidiyum Mun, the Night Is Slipping"
SLUG = "claude-liam-vidiyum-mun-a5-gamedev"
TOPIC = "WALKER · GODOT GAMEDEV · A5 SHADERS"
PROJECT = "Vidiyum Mun"
BUILD, _rows = snapshot(REPO)
B8 = BUILD[:8]
import os
REV = os.environ.get('A5_FILM_REV') or (REEL / 'evidence/source-revision.txt').read_text().split()[0]   # the ONE revision variable
# deck_marble + hint_experiment authorship: coordinator's final wording, 2026-11-01 (env overrides kept for reruns)
AUTHOR_PART2 = os.environ.get('A5_AUTHOR_PART2', "written by Shriram with ChatGPT's help (learning shaders for the first time), from Claude's slot outline")
AUTHOR_PART2_SPOKEN = os.environ.get('A5_AUTHOR_PART2_SPOKEN', "Shriram wrote the marble and hint shaders with ChatGPT's help, learning shaders for the first time, from Claude's slot outline.")
SAY = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
       '8': 'eight', '9': 'nine', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F'}
REV_SPOKEN = ' '.join(SAY[c] for c in REV)
SCRIPTED = "SCRIPTED CAPTURE · real renderer · values set from code, not played by hand"
SHRIRAM = "SHRIRAM'S OWN SCREENSHOT"

def excerpt(root, rel, anchor, n):
    lines = (root / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    if len(hits) != 1:
        raise SystemExit(f'anchor {anchor!r} matched {len(hits)} lines in {rel}')
    s = hits[0]
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
    'B03': excerpt(GODOT, 'shaders/night_skip.gdshader', 'shader_type canvas_item;', 9),
    'B05': excerpt(GODOT, 'ui/night_skip_driver.gd', '## The state the glow shows', 9),
    'B07': excerpt(GODOT, 'shaders/hint_experiment.gdshader', 'uniform sampler2D strip_as_colour', 11),
    'B09': excerpt(GODOT, 'shaders/deck_marble.gdshader', 'group_uniforms surface;', 13),
    'B11': excerpt(GODOT, 'materials/marble_wet.tres', '[resource]', 7),
    'B13': excerpt(GODOT, 'shaders/standard_generated.gdshader', 'shader_type spatial;', 5),
    'B16': excerpt(GODOT, 'tests/test_night_skip.gd', 'var shader: Shader = load(SHADER_PATH)', 8),
}
STATE_L, STATE_T = doc_line('CHANGE-BRIEF.md', 'The state, exactly')
COLOUR_L, COLOUR_T = doc_line('CHANGE-BRIEF.md', 'COLOR.rgb = mix(COLOR.rgb, skip_tint.rgb')
GEN7_L, GEN7 = doc_line('godot/shaders/standard_generated.gdshader', 'uniform sampler2D texture_albedo')
GEN19_L, GEN19 = doc_line('godot/shaders/standard_generated.gdshader', 'uniform sampler2D texture_normal')
OWN5_L, OWN5 = doc_line('godot/shaders/deck_marble.gdshader', 'uniform sampler2D albedo_tex')
OWN11_L, OWN11 = doc_line('godot/shaders/deck_marble.gdshader', 'uniform sampler2D normal_tex')

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
    """Own media built by tools/make_media.py from real engine captures, Shriram's screenshots and recorded logs."""
    return {"type": "GAMEPLAY", "class": "SHOW", "source": "own", "treatment": "none", "label": label,
            "segments": segments, "evidence_media": f"media/{bid}.mp4", "show": show, "note": note}

BAR = [0, 0, 480, 270]          # top-left of a 1280x720 capture: the status bar, zoomed (crop, labelled)

beats = [
 {"beat_id": "B00", "act": "ASK",
  "role_note": "Walker B00. Illustrative reconstruction of the ask (labelled), never a transcript.",
  "narration_text": "Vanakkam, this is Liam, in for Bear. The prompt on screen is a reconstruction, not a transcript. Assignment five for Vidiyum Mun: three hand-written shaders, the materials that use them, and the tests and captures that check them.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Vanakkam, Liam", "topic": "ILLUSTRATIVE RECONSTRUCTION · NOT A TRANSCRIPT", "segment": "Vidiyum Mun · A5",
      "command": "Please use Walker to convert my game design document about Vidiyum Mun, a time-loop mystery at a party on a fenced private beach on ECR, Chennai, into shaders: a glow on Hari's phone status bar while the night is being skipped, a textured marble shader for the pool deck with a dry and a wet material, and a hint experiment. Add headless tests.",
      "runningText": "reading CHANGE-BRIEF.md and godot/…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["night_skip.gdshader · 33/33 at 30, 60, 144 fps.", "deck_marble.gdshader · dry + wet · 156/156.",
                 "Hint quads: 64/128/192 and 137/188/225, as predicted."]},
      [{"at": "0.05", "event": "composer; greeting"}, {"at": "0.15", "event": "topic: ILLUSTRATIVE RECONSTRUCTION"},
       {"at": "0.25", "event": "the Walker ask types"}, {"at": "0.7", "event": "three result lines"}])},
 {"beat_id": "B01", "act": "BLUF", "lead_silence_s": 0.6,
  "role_note": "Hesitant writer; single-word correction 'day' -> 'night'. No authorship claim here (credits beat B19).",
  "narration_text": "Three hand-written shaders. One makes Hari's phone glow while the night slips away. One reads a marble texture as colour and as data. One proves the difference with three grey pixels. Then tests, mutations and captures check every claim they can.",
  "shot": remotion("BrutalistHesitantWriter", {
      "contextTitle": "What this film shows",
      "text": "Three hand-written shaders.\nOne glows while the day slips.\nOne reads marble as colour and as data.",
      "triggerWords": "day", "replacementWords": "night",
      "fontSize": 84, "lineSpacing": 2.6, "align": "center", "seed": "vidiyum-a5",
      "mistakeRate": 2, "hesitateWithin": 0, "hesitateBetween": 1, "charMs": 8,
      "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
      [{"at": "0.08", "event": "line one types"}, {"at": "0.3", "event": "'day' struck; 'night' typed"},
       {"at": "0.55", "event": "lines two and three"}])},
 {"beat_id": "B02", "act": "SETUP",
  "role_note": "Game, the state the effect communicates, the objects (incl. the textured one); the colour line in the spec (CHANGE-BRIEF.md §1.1, §1.4).",
  "narration_text": "The game is Vidiyum Mun, a time loop at a beach party in Chennai. Holding T at night runs the clock eight times faster, and whatever happens meanwhile goes unheard. The spec names that state exactly, and the colour line from the brief: mix the bar's colour toward sodium orange, by skip amount times tint strength. The textured shader goes on the four pool-deck floors: three dry, one wet.",
  "shot": board("The game, the state, the object",
      f"CHANGE-BRIEF.md lines {STATE_L} and {COLOUR_L} (verbatim) · git {REV}",
      f"{STATE_T.strip()}\n\nThe colour line, §1.4:\n{COLOUR_T}",
      "SPEC · written before either shader existed", "What it's for",
      [{"label": "Game", "text": "Vidiyum Mun: a time loop at an ECR beach party"},
       {"label": "State", "text": "T held at night: clock ×8, events go unheard"},
       {"label": "Shader 1", "text": "Hari's phone status bar (canvas_item)"},
       {"label": "Shader 2", "text": "4 deck floors: 3 dry marble, 1 wet (spatial)"}],
      [0.08, 0.22, 0.55, 0.85],
      [{"at": "0.05", "event": "spec excerpt"}, {"at": "0.55", "event": "colour line + objects"}])},
 {"beat_id": "B03", "act": "CODE",
  "role_note": "Q1 what a shader does: night_skip.gdshader, typed by Shriram. Paired result B04.",
  "narration_text": "Here's the shader Shriram typed in. Shader type canvas item: it runs on 2D drawing. Three uniforms, values the game can set from outside. And line eight, the colour line from the spec, word for word. A shader is a small program the graphics card runs for every pixel the bar draws. This one takes the colour the bar arrived with, and mixes it toward orange.",
  "shot": workbench("B03", "What a shader does: the colour line",
                    [{"label": "shader_type", "value": "canvas_item: 2D drawing"},
                     {"label": "uniforms", "value": "set from outside"},
                     {"label": "line 8", "value": "COLOR → toward orange"}],
                    [(0.18, 'shader_type canvas_item;', 'shader type'),
                     (0.35, 'uniform float skip_amount', 'set from outside'),
                     (0.6, 'COLOR.rgb = mix(', 'the colour line')], font=30)},
 {"beat_id": "B04", "act": "RESULT",
  "role_note": "Result of B03: controlled-value captures (real renderer) at 0 / 0.5 / 1 / 2, then the P1/P2 rows of TEST-REPORT A5.4.",
  "narration_text": "Its result, with the real renderer. Skip amount set from code to zero, a half, one, then two. Shriram predicted the battery pixel at one: two forty-nine, one ninety-seven, one forty-seven, once blended over the scene. Captured: exactly that, and every prediction held within one step per channel. At two, the bar went past the slider's end, to pure orange. Hint range does not clamp a value set from code.",
  "shot": own("B04", f"{SCRIPTED} · status bar zoomed",
              [{"at": "0.0", "event": "skip_amount 0"}, {"at": "0.16", "event": "0.5"}, {"at": "0.32", "event": "1.0"},
               {"at": "0.48", "event": "2.0 (beyond the range)"}, {"at": "0.64", "event": "TEST-REPORT A5.4 rows"}],
              "Engine captures at fixed values; then the recorded table.",
              [{"kind": "still", "src": "evidence/a5/glow_skip_0_0.png", "crop": BAR, "w": 1, "label": f"{SCRIPTED} · skip_amount = 0.0"},
               {"kind": "still", "src": "evidence/a5/glow_skip_0_5.png", "crop": BAR, "w": 1, "label": f"{SCRIPTED} · skip_amount = 0.5"},
               {"kind": "still", "src": "evidence/a5/glow_skip_1_0.png", "crop": BAR, "w": 1, "label": f"{SCRIPTED} · skip_amount = 1.0"},
               {"kind": "still", "src": "evidence/a5/glow_skip_2_0.png", "crop": BAR, "w": 1, "label": f"{SCRIPTED} · skip_amount = 2.0, set from code"},
               {"kind": "still", "src": "evidence/table_glow.png", "w": 2.2, "label": "TEST-REPORT.md A5.4 · captured vs predicted on screen (verbatim rows)"}])},
 {"beat_id": "B05", "act": "CODE",
  "role_note": "How game state reaches the shader: the driver (night_skip_driver.gd). Paired result B06 (motion + playtest + test timings).",
  "narration_text": "So who sets skip amount during play? This driver. Each frame it reads the game state, and never writes it: fast forward, during the night phase. Move toward steps the value by delta, over a quarter second in, and half a second out. Then it hands the number to the material. Delta, not a frame count, so the fade takes the same time at thirty or a hundred forty-four frames a second.",
  "shot": workbench("B05", "How game state reaches the shader",
                    [{"label": "state_holds()", "value": "reads, never writes"},
                     {"label": "FADE_IN / OUT", "value": "0.25 s / 0.5 s"},
                     {"label": "_apply()", "value": "set_shader_parameter"}],
                    [(0.15, 'return LoopState.fast_forward', 'reads the state'),
                     (0.45, 'move_toward(skip_amount, target, delta / duration)', 'steps by delta'),
                     (0.75, '_apply()', 'to the material')], font=30)},
 {"beat_id": "B06", "act": "RESULT",
  "role_note": "Result of B05: scripted movie-maker capture (real input events), Shriram's playtest screenshot, recorded test timings.",
  "narration_text": "In motion: a scripted capture, with T held and released through real input events, recorded frame by frame by Godot's movie maker. Eight frames to full glow, fifteen to fade, at thirty frames a second. Then Shriram's own screenshot from playing it, T held, times eight. And the recorded test at thirty, sixty, and a hundred forty-four: fade in a quarter second, within one frame; fade out half a second.",
  "shot": own("B06", "SCRIPTED CAPTURE · Godot movie maker · T held via Input.parse_input_event · real driver + shader",
              [{"at": "0.0", "event": "glow fades in and out (real time)"}, {"at": "0.3", "event": "same at half speed"},
               {"at": "0.6", "event": "Shriram's playtest screenshot"}, {"at": "0.8", "event": "test timings at 30/60/144"}],
              "Motion capture, then Shriram's screenshot, then recorded test output.",
              [{"kind": "clip", "src": "capture/glow_motion.avi", "start_frame": 29, "end_frame": 196, "speed": 1.0, "crop": BAR,
                "label": "SCRIPTED CAPTURE · movie maker, 30 fps · real time · zoomed on the status bar"},
               {"kind": "clip", "src": "capture/glow_motion.avi", "start_frame": 48, "end_frame": 115, "speed": 0.5, "crop": BAR,
                "label": "SCRIPTED CAPTURE · the same frames at HALF SPEED"},
               {"kind": "still", "src": "evidence/a5/human/checkC_playtest_T_held_x8.png", "w": 1, "label": f"{SHRIRAM} · F5 playtest, T held (>> x8)"},
               {"kind": "still", "src": "evidence/terminal_timings.png", "w": 1.2, "label": "HEADLESS · test_night_skip.gd at 30 / 60 / 144 fps · lines verbatim from logs/"}])},
 {"beat_id": "B07", "act": "CODE",
  "role_note": "Q3 why a texture is information: hint_experiment.gdshader. Paired result B08.",
  "narration_text": "Why is a texture information? This experiment binds one file, three grey texels, sixty-four, one twenty-eight and one ninety-two, to two samplers. One says source colour: these bytes are s R G B colour, so decode them. The other says nothing: these bytes are data. A bool picks which one writes albedo.",
  "shot": workbench("B07", "Same bytes, two meanings",
                    [{"label": "texture", "value": "greys 64 · 128 · 192"},
                     {"label": "strip_as_colour", "value": "decode as sRGB"},
                     {"label": "strip_as_data", "value": "raw numbers"}],
                    [(0.25, 'source_color, filter_nearest', 'read as colour'),
                     (0.5, 'strip_as_data : filter_nearest', 'read as data'),
                     (0.8, 'if (use_source_color)', 'the bool picks')], font=30)},
 {"beat_id": "B08", "act": "RESULT",
  "role_note": "Result of B07: hint quads captured, with Shriram's prediction (CHANGE-BRIEF §2.5) and the measurement (TEST-REPORT A5.6).",
  "narration_text": "Shriram predicted both quads before the shader existed. With the hint: sixty-four, one twenty-eight, one ninety-two, because the decode and the screen's encode cancel out. Without it: one thirty-seven, one eighty-eight, two twenty-five, encoded for the screen without ever being decoded. Captured: exactly those six numbers. Same bytes, different meaning.",
  "shot": own("B08", f"{SCRIPTED} · hint_experiment.tscn, Linear tonemap, exposure 1.0",
              [{"at": "0.0", "event": "the two quads"}, {"at": "0.5", "event": "predicted vs measured"}],
              "Engine capture, then the two recorded tables.",
              [{"kind": "still", "src": "evidence/a5/hint_quads.png", "w": 1, "label": f"{SCRIPTED} · top: source_color · bottom: no hint"},
               {"kind": "still", "src": "evidence/table_hint.png", "w": 1.3, "label": "CHANGE-BRIEF.md §2.5 (predicted) · TEST-REPORT.md A5.6 (captured) · verbatim rows"}])},
 {"beat_id": "B09", "act": "CODE",
  "role_note": "deck_marble.gdshader uniforms: colour vs data samplers, ranges, groups. Paired result B10.",
  "narration_text": "The marble shader uses that difference. Albedo, the colour of the stone, gets source colour. Roughness and the normal map are data: no source colour, and the normal map says hint normal. Then five number uniforms, each with a range and a default, in two Inspector groups, surface and finish. Its UVs come from world X Z, so all four floors tile at the same scale.",
  "shot": workbench("B09", "Colour and data in one material",
                    [{"label": "albedo_tex", "value": "colour"},
                     {"label": "rough / normal", "value": "data"},
                     {"label": "groups", "value": "surface · finish"}],
                    [(0.12, 'uniform sampler2D albedo_tex', 'colour: source_color'),
                     (0.3, 'uniform sampler2D roughness_tex', 'data, no hint'),
                     (0.4, 'uniform sampler2D normal_tex', 'data: hint_normal'),
                     (0.62, 'uniform float tile_size_m', 'range + default'),
                     (0.78, 'group_uniforms finish;', 'Inspector groups')], font=28)},
 {"beat_id": "B10", "act": "RESULT",
  "role_note": "Result of B09: marble at a held 10 PM (real renderer) and the interface sweep sheet.",
  "narration_text": "Here it is under the string lights, at a held ten P M. Then the interface sweep, each slider at both ends of its range. Tile size takes the slabs from busy to broad. Specular grows the pool of light. Roughness changes it less. And normal depth barely shows, because this polished marble's normal map is very flat.",
  "shot": own("B10", f"{SCRIPTED} · slice.tscn, clock held at 10:00 PM",
              [{"at": "0.0", "event": "marble at 10 PM"}, {"at": "0.4", "event": "sweep sheet"}],
              "Engine captures, labelled.",
              [{"kind": "still", "src": "evidence/a5/marble_10pm_glow_on.png", "w": 1, "label": f"{SCRIPTED} · deck at 10:00 PM, glow on"},
               {"kind": "still", "src": "evidence/a5/sweep_sheet.png", "w": 1.6, "label": f"{SCRIPTED} · interface sweep: each marble_dry uniform at both range ends (glow off)"}])},
 {"beat_id": "B11", "act": "CODE",
  "role_note": "Q2 material vs shader: marble_wet.tres. Paired result B12 (Shriram's editor checks A and B).",
  "narration_text": "A shader is the program. A material is one set of values for it. Here's the wet material: the same shader file, the same three textures, and just two values changed, roughness zero point three, and specular zero point eight. The dry material sets none of them, so the shader's defaults apply.",
  "shot": workbench("B11", "A material is values for a shader",
                    [{"label": "shader", "value": "one, shared"},
                     {"label": "wet overrides", "value": "0.3 · 0.8"},
                     {"label": "marble_dry", "value": "shader defaults"}],
                    [(0.25, 'shader = ExtResource', 'one shader'),
                     (0.45, 'shader_parameter/albedo_tex', 'same textures'),
                     (0.7, 'shader_parameter/roughness_scale', 'wet: glossier')], font=32)},
 {"beat_id": "B12", "act": "RESULT",
  "role_note": "Result of B11: Shriram's own editor screenshots (TEST-REPORT A5.8 checks A and B).",
  "narration_text": "Shriram checked it in the editor. One edit to the shader, albedo times zero point three, and all four floors went dark, dry and wet together. One edit to the wet material, a red tint, and only the strip behind the pool changed. Both edits were undone, and git confirmed it.",
  "shot": own("B12", f"{SHRIRAM} · Godot editor, slice.tscn",
              [{"at": "0.0", "event": "shader edit: all floors dark"}, {"at": "0.5", "event": "material edit: only the back strip red"}],
              "Shriram's screenshots, labelled.",
              [{"kind": "still", "src": "evidence/a5/human/checkA_shader_edit_x0.3_all_floors_dark.png", "w": 1,
                "label": f"{SHRIRAM} · shader line 27 × 0.3: all four floors darken"},
               {"kind": "still", "src": "evidence/a5/human/checkB_wet_tint_red_only_back_strip.png", "w": 1,
                "label": f"{SHRIRAM} · marble_wet albedo_tint red: only the back strip"}])},
 {"beat_id": "B13", "act": "CODE",
  "role_note": "Q4 the Godot shading language: standard_generated.gdshader (editor conversion). Paired result B14.",
  "narration_text": "What is the Godot shading language? Shriram converted a standard material to code in the editor, and this is what Godot wrote. A shader type and a render mode up top. Then uniforms with hints, which build the Inspector: a colour for the albedo, and source colour on the albedo texture. It reads like G L S L, but Godot decides the stages and the built-ins.",
  "shot": workbench("B13", "What Godot wrote for a StandardMaterial3D",
                    [{"label": "lines 3–4", "value": "type · render mode"},
                     {"label": "line 6", "value": "albedo colour"},
                     {"label": "line 7", "value": "albedo: source_color"}],
                    [(0.2, 'shader_type spatial;', 'shader type'), (0.32, 'render_mode', 'render mode'),
                     (0.55, 'uniform vec4 albedo', 'Inspector albedo colour'),
                     (0.72, 'uniform sampler2D texture_albedo', 'source_color')], font=28)},
 {"beat_id": "B14", "act": "RESULT",
  "role_note": "Result of B13: the generated shader rendering Shriram's scratch sphere (scripted capture, camera/light added at runtime).",
  "narration_text": "And that generated code, rendering Shriram's scratch sphere with the same three marble textures. The capture script added the camera and the light. The material is exactly what the editor generated.",
  "shot": own("B14", "SCRIPTED CAPTURE · scenes/scratch_standard.tscn · camera + light added at runtime, nothing saved",
              [{"at": "0.0", "event": "the sphere"}],
              "Engine capture, labelled.",
              [{"kind": "still", "src": "evidence/standard_generated_sphere.png", "w": 1, "crop": [253, 218, 1035, 658],
                "label": "SCRIPTED CAPTURE · scenes/scratch_standard.tscn · camera + light added at runtime, nothing saved · cropped to the sphere"}])},
 {"beat_id": "B15", "act": "COMPARE",
  "role_note": "Two generated lines beside their equivalents in Shriram's shader (verbatim), annotated.",
  "narration_text": "Line seven of the generated shader, beside line five of the marble shader: both put source colour on the albedo sampler. Line nineteen beside line eleven: Godot's normal map uses hint roughness normal, Shriram's uses hint normal, and neither decodes it as colour. That's what Godot's language adds over plain G L S L: shader types with their built-ins, and hints that wire each uniform to the Inspector and to colour decoding.",
  "shot": board("Generated vs deck_marble, line by line",
      f"verbatim lines · git {REV}",
      f"standard_generated.gdshader:{GEN7_L}\n{GEN7}\ndeck_marble.gdshader:{OWN5_L}\n{OWN5}\nstandard_generated.gdshader:{GEN19_L}\n{GEN19}\ndeck_marble.gdshader:{OWN11_L}\n{OWN11}",
      "LANGUAGE-NOTES.md Q6 · both read albedo as colour, the normal map as data", "What the hints say",
      [{"label": f"gen :{GEN7_L} ≈ own :{OWN5_L}", "text": "source_color: decode sRGB, it's colour"},
       {"label": f"gen :{GEN19_L} ≈ own :{OWN11_L}", "text": "hint_roughness_normal / hint_normal: data"},
       {"label": "Godot adds", "text": "shader_type + built-ins (no hand-written entry points)"},
       {"label": "Godot adds", "text": "hints → Inspector sliders, groups, colour decoding"}],
      [0.08, 0.35, 0.68, 0.84],
      [{"at": "0.05", "event": "two line pairs"}, {"at": "0.68", "event": "what Godot adds"}])},
 {"beat_id": "B16", "act": "CODE",
  "role_note": "The uniform-list assertion (test_night_skip.gd). Paired result B17 (mutations).",
  "narration_text": "Now the tests. Setting a uniform and reading it back proves nothing, because Godot accepts any name without an error. So this test asks the compiled shader for its uniform list. An empty list means it failed to parse. A missing name means somebody renamed it.",
  "shot": workbench("B16", "Ask the shader, not a round trip",
                    [{"label": "uniform list", "value": "what it declares"},
                     {"label": "size == 3", "value": "empty = no parse"},
                     {"label": "name + type", "value": "catches a rename"}],
                    [(0.3, 'get_shader_uniform_list()', 'the compiled list'),
                     (0.6, 'listed.size() == 3', 'parse check'),
                     (0.85, 'listed.get(uname, -1)', 'name contract')], font=28)},
 {"beat_id": "B17", "act": "RESULT",
  "role_note": "Result of B16: the three mutations' recorded output (logs/mutations/*.log), verbatim.",
  "narration_text": "Shriram broke the shaders on purpose, three times. Delete one semicolon: a shader error, and four checks fail. Rename skip amount: two fail, while all twenty-two timing checks still passed, because the driver kept writing a name that no longer existed, silently. Remove source colour from the marble: the material test fails. Each run exited with one, and each file was restored.",
  "shot": own("B17", "HEADLESS · logs/mutations/*.log · recorded output, verbatim lines",
              [{"at": "0.0", "event": "m1 semicolon"}, {"at": "0.35", "event": "m2 rename"}, {"at": "0.7", "event": "m3 source_color"}],
              "Recorded output, not reconstructed.",
              [{"kind": "still", "src": "evidence/terminal_mutations.png", "w": 1}])},
 {"beat_id": "B18", "act": "LIMITS",
  "role_note": "Agent mistakes caught; what no headless run can show; what remains uncertain.",
  "narration_text": "What Claude and its agents got wrong, and how each was caught. The CLAUDE dot M D draft cited the wrong floor lines and missed two tests. The audit invented a colour temperature, misstated which floors share a material, and its hint check matched substrings, so source colour on a data sampler would have passed. An explicit assertion fixed that. The audit agent tried to reset project dot godot three times, and its scope denied it. And Claude first wrote its own curl formula, then replaced it with the course's. No headless run shows how anything looks. That's what the captures and Shriram's eyes are for.",
  "shot": board("What the agents got wrong",
      f"FRICTIONAL.md · MATERIALS.md review · git {REV}",
      "CLAUDE.md draft: wrong floor lines; 2 tests missing.\nAudit: invented '~2700 K'; wrong on which floors share a material.\nAudit test: substring hint check passed source_color on data → assertion added.\nAudit agent: git checkout ×2 + git restore ×1 on project.godot → denied.\nClaude: own curl formula → the course's.",
      "REVIEW · every fix came from a reading, a measurement or a mutation", "What headless can't show",
      [{"label": "The look", "text": "dummy renderer draws nothing"},
       {"label": "Glow reads as skipping?", "text": "Shriram's playtest"},
       {"label": "Marble reads as stone?", "text": "captures + Shriram's eyes"},
       {"label": "Seams line up?", "text": "Shriram, walking the deck"}],
      [0.8, 0.86, 0.91, 0.95],
      [{"at": "0.05", "event": "mistakes list"}, {"at": "0.8", "event": "headless limits"}])},
 {"beat_id": "B19", "act": "CREDITS",
  "role_note": "Who did what (SOURCES.md 'Who did what in A5'); texture sources; game-source revision on screen.",
  "narration_text": f"Who did what. Shriram chose the state, the object, the colour, the fades and the marble, and made every prediction, with ChatGPT's help on the maths. Shriram typed in the night-skip shader; its colour line comes from the brief. {AUTHOR_PART2_SPOKEN} Shriram ran the mutations and the human checks, and wrote the language notes in their own words; ChatGPT had paraphrased an earlier draft. Claude proposed options, organised the brief's prose, gave a slot outline for the Part 2 shaders, and wrote the driver, the tests, the wiring, the capture tools, the audit review, the docs and this film. Textures: Poly Haven's Marble zero one and Floor Tiles zero six, by Rob Tuytel, C C zero. Source revision, {REV_SPOKEN}.",
  "shot": board("Who did what",
      f"SOURCES.md · game source git {REV}",
      f"night_skip.gdshader: typed by Shriram (its colour line comes from the brief, worked out with ChatGPT's help).\ndeck_marble.gdshader and hint_experiment.gdshader: {AUTHOR_PART2}.\nLANGUAGE-NOTES (Shriram's own words; an earlier draft was paraphrased by ChatGPT).",
      f"CREDITS · source revision {REV}", "Who did what in A5",
      [{"label": "Shriram", "text": "state, object, colour, fades, marble; predictions (maths with ChatGPT); mutations; human checks"},
       {"label": "Claude · audit agent", "text": "Claude: proposed options, organised the brief's prose, slot outline for the Part 2 shaders; driver, tests, wiring, capture tools, audit review, docs, this film. Audit agent: MATERIALS.md, test_materials.gd (reviewed)."},
       {"label": "Textures · narration · revision", "text": f"Marble 01, Floor Tiles 06 (curl calibration): Rob Tuytel, Poly Haven, CC0 · Kokoro am_onyx (\"Liam\"), local · git {REV}"}],
      [0.05, 0.58, 0.8],
      [{"at": "0.05", "event": "authorship + Shriram"}, {"at": "0.58", "event": "Claude + audit agent"}, {"at": "0.8", "event": "textures + revision"}])},
 {"beat_id": "B20", "act": "VERDICT", "lead_silence_s": 0.4,
  "role_note": "Verdict: checked / uncertain / limits / next.",
  "narration_text": "Let's recap with Claude. Checked: both shaders parse, the glow follows its rules at three frame rates, every predicted pixel held, and three mutations each failed their test. Uncertain: the marble's normal map is too flat for a decisive curl verdict, zero point six three seven. And the glow's on-screen contrast, three point four six to one, depends on the scene behind the bar. Next: Shriram's idea, a battery that drains from orange to red as dawn approaches.",
  "shot": remotion("ClaudeVerdictArtifact", {
      "artifactTitle": "Verdict", "artifactHeading": f"Vidiyum Mun A5 shaders, git {REV}.", "brandLabel": "@NikBearBrown",
      "artifactLines": ["Checked: parse, rules at 30/60/144 fps, every predicted pixel, 3 mutations fail.",
                        "Uncertain: Marble 01 too flat for a curl verdict (0.637).",
                        "Limits: on-screen contrast 3.46:1 depends on the scene behind the bar.",
                        "Next: the battery drains from orange to red as dawn nears."]},
      [{"at": "0.1", "event": "verdict card"}, {"at": "0.25", "event": "checked"}, {"at": "0.45", "event": "uncertain"},
       {"at": "0.65", "event": "limits"}, {"at": "0.85", "event": "next"}])},
 {"beat_id": "B21", "act": "HANDOFF",
  "role_note": "Your Turn: prompt read aloud; one bounded change + prediction; signs off.",
  "narration_text": "Your turn. Pick one state in your game, and one object that should show it. Write the colour line yourself, and predict one pixel at three values. Then ask Claude for the driver, and a test that checks the uniform list, not a round trip. Delete a semicolon, and watch it fail. Liam, in for Bear.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Your turn.", "topic": TOPIC, "segment": "Your One Shader",
      "command": "I wrote a canvas_item shader with one uniform for a state in my game. Write a driver that sets it from that state by delta, and a headless test that asserts the shader's uniform list, not a set-then-get round trip. I've predicted one pixel at 0, 0.5 and 1.",
      "runningText": "paste this into Claude…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["You write the colour line.", "Claude writes the driver + test.", "Delete a semicolon: it must fail."],
      "animateTyping": True},
      [{"at": "0.05", "event": "'Your turn.'"}, {"at": "0.1", "event": "prompt types"}, {"at": "0.75", "event": "result lines"}])},
 {"beat_id": "B22", "act": "OUTRO", "kind": "outro_voice", "tail_hold_s": 1.0,
  "role_note": "OUTRO-LOCK: ClaudeTitleOutro, exact title, @NikBearBrown, slug-seeded mascot; spoken, no jingle.",
  "narration_text": TITLE + ". At Nik Bear Brown.",
  "shot": remotion("ClaudeTitleOutro", {"title": TITLE, "slug": SLUG},
      [{"at": "0.0", "event": "title card"}, {"at": "0.3", "event": "@NikBearBrown + mascot"}])},
]

OWN_QC = {
    "contrast_regions": [{"label": "caption band (film label)", "box": [0.074, 0.905, 0.62, 0.955]}],
    "contrast_reason": "Real engine captures, Shriram's screenshots and recorded logs reframed at 85 % inside title-safe; the film's essential text is the caption band. Text inside the evidence is inspected by eye in _qc frame samples."}
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
    # keep a Remotion render stamp only when the beat's props are unchanged (cues/duration are re-derived by make_media)
    rem, prem = b["shot"].get("remotion"), (prev or {}).get("shot", {}).get("remotion")
    strip = lambda p: {k: v for k, v in (p or {}).items() if k not in ("durationSeconds", "cues")}
    if rem and prem and "rendered" in prem and strip(rem["props"]) == strip(prem.get("props")) \
            and prev.get("narration_text") == b["narration_text"]:
        rem["rendered"] = prem["rendered"]

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "mode": "walker",
    "brand": "claude-liam", "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "crop",
    "captions": False, "channel": "@NikBearBrown", "channel_title": "@NikBearBrown", "folderLabel": "@NikBearBrown",
    "greeting": "Vanakkam, Liam", "greeting_note": "hello lexicon: Vanakkam (Tamil), fits the Chennai setting.",
    "persona": "Liam (in for Bear)", "in_for_bear": True,
    "audience": "CSYE 7270 reviewers and makers writing their first Godot shaders",
    "source_revision": REV,
    "game": {"name": "walker-vidiyum-mun-shriram-a", "build_id": BUILD, "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
             "renderer": "Forward+ (Metal)", "git": REV},
    "fps": 30},
  "beats": beats}
sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
words = sum(len(b['narration_text'].split()) for b in beats)
print(f"wrote {sheet_path.name} · {len(beats)} beats · {words} words (~{words / 2.9:.0f} s) · git {REV} · build {B8}")
for k, e in EX.items():
    print(f"  {k}: godot/{e['path']} {e['start_line']}–{e['end_line']}")
