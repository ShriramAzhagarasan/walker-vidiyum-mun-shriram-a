#!/usr/bin/env python3
"""Author beat_sheet.json for the Vidiyum Mun gamedev film (godot-gamedev, walker mode).

Everything that can drift after the code freeze is RESOLVED, not typed:
  * code excerpts are located by an anchor line and copied verbatim from godot/ (line numbers follow);
  * gameplay clip ranges come from capture/<take>-inputs.jsonl events (frame / 30 = capture s);
  * the build id is the source snapshot of godot/ (tools/source_snapshot.py).
Facts that are typed in narration are listed in FACTCHECK.md with their source lines; re-check those
marked RE-VERIFY AT FREEZE before generating audio.

  python3 tools/author_sheet.py [--take run-01]
Re-running keeps measured audio fields for beats whose narration did not change.
"""
import argparse, base64, io, json, sys
from pathlib import Path
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GODOT = REPO / 'godot'
sys.path.insert(0, str(REEL / 'tools'))
from source_snapshot import snapshot  # noqa: E402

TITLE = "Vidiyum Mun: One Pose, From Spec to Engine"
SLUG = "claude-liam-walker-vidiyum-mun-shriram-a-gamedev"
TOPIC = "WALKER · GODOT GAMEDEV"
PROJECT = "Vidiyum Mun"
GAME_LABEL = "SCRIPTED-INPUT CAPTURE · real engine run · keyboard events · not a human playtest"

ap = argparse.ArgumentParser()
ap.add_argument('--take', default='run-01')
args = ap.parse_args()
BUILD, _rows = snapshot(REPO)
B8 = BUILD[:8]

# --- source excerpts (verbatim, anchor-located) ------------------------------------------

def excerpt(rel, anchor, n=None):
    """n lines from the anchor line; n=None = the whole block up to (not including) the next blank line."""
    lines = (GODOT / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    if len(hits) != 1:
        raise SystemExit(f'anchor {anchor!r} matched {len(hits)} lines in {rel}')
    s = hits[0]
    if n is None:
        n = next((k for k in range(1, len(lines) - s) if not lines[s + k].strip()), len(lines) - s)
    return {'path': rel, 'start_line': s + 1, 'end_line': s + n, 'text': '\n'.join(lines[s:s + n])}

def line_of(ex, needle):
    for i, l in enumerate(ex['text'].split('\n')):
        if needle in l:
            return ex['start_line'] + i
    raise SystemExit(f'{needle!r} not in excerpt {ex["path"]}')

EX = {
    'B08': excerpt('scenes/hari.gd', 'func _show_state(state: String) -> void:'),
    'B10': excerpt('autoload/loop_state.gd', 'func _set_clock(minutes: float) -> void:'),
    'B12': excerpt('autoload/sound_bank.gd', 'ls.phone_buzz.connect(_play.bind("phone_buzz"))', 7),
    'B17': excerpt('scenes/slice.gd', '# Clock colour stops:', None),
}

# --- capture events -> clip ranges ---------------------------------------------------------

def load_events(take):
    p = REEL / f'capture/{take}-inputs.jsonl'
    if not p.exists():
        p = REEL / 'capture/validate-720-inputs.jsonl'          # PLANNING ONLY before the final take
        print(f'WARNING: {take} log missing; planning ranges from {p.name}', file=sys.stderr)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()], p.name

EVENTS, EVENT_SRC = load_events(args.take)

def t(event, n=1, **match):
    k = 0
    for e in EVENTS:
        if e['event'] == event and all(e.get(a) == b for a, b in match.items()):
            k += 1
            if k == n:
                return e['t']
    raise SystemExit(f'event {event} {match} #{n} not in {EVENT_SRC}')

T_END = EVENTS[-1]['t']
def _ranges():
  return {
    'B02': (0.0, t('input', key='Enter', pressed=True) + 13.4),
    'B03': (t('loop_started', loop=1), t('dialogue_closed', conversation='amma_call_first') + 0.6),
    'B09': (t('dialogue_closed', conversation='amma_call_first') - 1.6, t('dialogue_closed', conversation='krishna_ambient') + 0.8),
    'B11': (t('walk_start', what='Manikandan', loop=1) + 3.0, t('advay_arrived', loop=1) + 6.5),
    'B14': (t('sfx_event', id='dawn_crash') - 3.0, t('loop_started', loop=2) + 4.5),
    'B15': (t('walk_start', what='Manikandan', loop=2) - 0.2, t('sfx_event', id='clue_saved', clue='KEYS_WITH_MANI') + 2.2),
    'B16': (t('advay_arrived', loop=2) - 1.0, T_END),
}
try:
    R = _ranges()
except SystemExit as exc:                      # planning before the take has finished: placeholder ranges
    print('PLANNING ONLY, placeholder gameplay ranges:', exc, file=sys.stderr)
    R = {k: (0.0, 10.0) for k in ('B02', 'B03', 'B09', 'B11', 'B14', 'B15', 'B16')}
R = {k: (round(a * 30) / 30, round(b * 30) / 30) for k, (a, b) in R.items()}

# --- images for the trace beats (embedded so the toolkit's public/ stays untouched) -------

def data_uri(rel, width=2400):
    im = Image.open(REEL / rel).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# --- shot builders ---------------------------------------------------------------------

def remotion(pattern, props, show, **kw):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "show": show,
            "remotion": {"pattern": pattern, "props": props}, **kw}

def gameplay(bid, show, note, label=GAME_LABEL, game_audio_db=-20.0):
    a, b = R[bid]
    return {"type": "GAMEPLAY", "class": "SHOW", "source": "own", "treatment": "none",
            "capture": {"id": args.take, "start_s": a, "end_s": b, "method": "scripted-input"},
            "label": label, "game_audio_db": game_audio_db,
            "hold_policy": "labeled final-frame hold (HELD FRAME) if narration outlasts the action",
            "evidence_media": f"media/{bid}.mp4", "show": show, "note": note}

def workbench(bid, title, notes, cues, source):
    ex = EX[bid]
    return remotion("GodotDevWorkbench", {
        "mode": "code", "title": title, "project": PROJECT, "path": "godot/" + ex['path'],
        "source": source + f" · godot/{ex['path']} lines {ex['start_line']}–{ex['end_line']} · build {B8}",
        "code": ex['text'], "startLine": ex['start_line'], "codeFontSize": 27,
        "inspectorLabel": "Source notes — not Inspector values", "notes": notes,
        "cue_fracs": [{"frac": f, "line": line_of(ex, needle), "label": lab} for f, needle, lab in cues],
        "cues": [], "output": [f"Godot editor reconstruction · build {B8}"]},
        [{"at": str(f), "event": f"line highlight: {lab}"} for f, _, lab in cues])

def figure(title, status, image, cards, source, excerpt_text='', image_label=''):
    return remotion("GodotDesignFigure", {
        "title": title, "status": status, "image": data_uri(image), "imageLabel": image_label,
        "excerpt": excerpt_text, "source": source, "cards": [{"label": a, "text": b} for a, b in cards],
        "cue_fracs": [{"frac": round(0.12 + i * 0.8 / len(cards), 2), "card": i} for i in range(len(cards))], "cues": []},
        [{"at": str(round(0.12 + i * 0.8 / len(cards), 2)), "event": f"card {i + 1}: {a}"} for i, (a, _) in enumerate(cards)],
        image_source=image)

WALK_FRAMES = sorted((GODOT / 'assets/art/hari').glob('walk_[0-9].png'))
if len(WALK_FRAMES) > 1:
    WALK_LINE = (f"Walking is the one exception: {len(WALK_FRAMES)} walk frames, stepped by distance travelled, "
                 "so the feet don't slide.")
else:
    WALK_LINE = "Each state is a single still, so walking is one pose sliding across the deck. That's a trade this slice made on purpose."

_sum = REEL / 'evidence/tests/summary.json'
SUMMARY = {k: v['summary'].split(': ', 1)[1].replace(' -> ', ' · ') for k, v in json.loads(_sum.read_text()).items()} if _sum.exists() else {}

PHONE_ROW = (REPO / 'CHARACTER-SHEET.md').read_text().splitlines()
PHONE_ROW = next(l for l in PHONE_ROW if l.startswith('| 4 | PHONE |'))
CONCEPT = next(l for l in (REPO / 'CONCEPT.md').read_text().splitlines() if l.startswith('You are **Hari**')).replace('**', '')

beats = [
 {"beat_id": "B00", "act": "ASK",
  "role_note": "COLD OPEN + walker B00. Illustrative reconstruction of the ask (labelled in the topic line), never a transcript. Output lines = the actual built result.",
  "narration_text": "Vanakkam, this is Liam, in for Bear. The prompt on screen is a reconstruction, not a transcript. The shape of it: a time-loop mystery on a Chennai beach, built as a Godot slice where every picture and every sound came from a local model.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Vanakkam, Liam", "topic": "ILLUSTRATIVE RECONSTRUCTION · NOT A TRANSCRIPT", "segment": "Vidiyum Mun",
      "command": "Please use Walker to convert my game design document about Vidiyum Mun, a time-loop mystery at the last party on a fenced beach villa on ECR, Chennai, into a playable 2.5D Godot slice: a 3D marble deck, my hero Hari as generated cel-shaded art in ten states, and generated sound effects and music wired to real game events.",
      "runningText": "reading godot/ and CHANGE-BRIEF.md…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["Hari: 10 generated states on a 3D deck.", "5 SFX events + 2 music loops.", "Loop 1 earns the clues. Loop 2 keeps the keys."]},
      [{"at": "0.05", "event": "composer; greeting 'Vanakkam, Liam' (Tamil hello)"}, {"at": "0.15", "event": "topic: ILLUSTRATIVE RECONSTRUCTION"},
       {"at": "0.25", "event": "the Walker ask types"}, {"at": "0.7", "event": "three result lines"}])},
 {"beat_id": "B01", "act": "BLUF", "lead_silence_s": 0.8,
  "role_note": "EXECUTIVE-SUMMARY LAW. Misconception 'prompt' corrected to 'pipeline': the body shows the asset is a chain (spec, model, pick, edits, code), not one prompt.",
  "narration_text": "One pipeline made Hari, not one prompt. A spec, a model, a pick, three edits, and one function of engine code. Then the night he lives in, played twice, with five sounds that each fire once per event.",
  "shot": remotion("BrutalistHesitantWriter", {
      "contextTitle": "What this film shows",
      "text": "One prompt made Hari.\nA spec, a model, a pick, three edits, one function.\nThen one night, looped, scored by five sounds.",
      "triggerWords": "prompt", "replacementWords": "pipeline",
      "fontSize": 84, "lineSpacing": 2.6, "align": "center", "seed": "vidiyum-7270",
      "mistakeRate": 2, "hesitateWithin": 0, "hesitateBetween": 1, "charMs": 8,
      "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
      [{"at": "0.08", "event": "'One prompt made Hari.' types"}, {"at": "0.3", "event": "'prompt' struck; 'pipeline' typed"},
       {"at": "0.55", "event": "lines two and three"}])},
 {"beat_id": "B02", "act": "CONCEPT",
  "role_note": "Concept + pillars in plain terms over the game's own title screen and intro motion comic (real capture; Enter pressed once, panels run on their timers). CONCEPT.md l.6, 19-22.",
  "narration_text": "Here's the game, from its own title screen. You're Hari, a broke engineering student at a rich family's beach party. Every dawn ends in tragedy, and he wakes at eight PM again, keeping only what he learned. Four pillars: see the people nobody sees, every loop you see more, dawn is always coming, and the night belongs to Chennai.",
  "shot": gameplay("B02", [{"at": "0.0", "event": "title screen: Vidiyum Mun, Press Enter"}, {"at": "0.2", "event": "Enter; intro panel 1 (ECR) and panel 2 (the fence), generated stills"}],
                   "Title + intro motion comic (storyboard panel 1).",
                   label="SCRIPTED-INPUT CAPTURE · title screen + intro motion comic (generated stills) · real engine run")},
 {"beat_id": "B03", "act": "PLAY",
  "role_note": "Gameplay: loop 1 opens. PHONE state in real play; phone_buzz + music under narration at the stated gain.",
  "narration_text": "Real engine, scripted keyboard input. Eight PM, loop one. That buzz is Amma calling, and Hari switches to his phone pose: phone at the ear, elbow out. He tells her he's studying at Krishna's place. That pose is the asset we'll trace, from the spec to this frame.",
  "shot": gameplay("B03", [{"at": "0.0", "event": "8:00 PM, loop 1; incoming-call card; PHONE pose"},
                           {"at": "0.3", "event": "Amma / Hari / Amma lines advance on E"}],
                   "PHONE state + phone_buzz in real play.")},
 {"beat_id": "B04", "act": "TRACE-SPEC",
  "role_note": "Asset trace 1/5: the spec (code-drawn, committed before generation).",
  "narration_text": "Step one, the spec, committed before anything was generated. Ten states, and phone is number four: phone to ear, elbow out, eyes slightly away, because he's lying to his mother. The silhouette test found a risk. From the gate, idle, phone and overhear look alike. So the rule is written down: elbow clearly out.",
  "shot": figure("Step 1 · The spec, before any generation", "SPEC · code-drawn sketch, not model output",
                 'evidence/asset-trace/B-spec-board.png',
                 [("Committed", "revision 1, pre-generation"), ("Risk F5", "3 poses alike at 208 px"),
                  ("Rule", "PHONE: elbow clearly out"), ("Facing", "drawn right; left = flip")],
                 f"design/character/poses-spec.png (code-drawn by Claude) · CHARACTER-SHEET.md row 4 · highlight added for the film",
                 excerpt_text=PHONE_ROW)},
 {"beat_id": "B05", "act": "TRACE-PROMPT",
  "role_note": "Asset trace 2/5: the exact prompt from gen/log.jsonl (seed 302 row), with the edit reference.",
  "narration_text": "Step two, the exact prompt from the generation log: an edit of the reference Shriram picked, run locally on FLUX two klein. Most of the words pin identity: the face, the check, the chappals. One clause changes per state, and here it carries the spec's rule.",
  "shot": figure("Step 2 · The exact prompt", "PROMPT · gen/log.jsonl, verbatim",
                 'evidence/asset-trace/B-prompt-board.png',
                 [("Model", "FLUX.2 [klein] 4B, local"), ("Mode", "edit from hari-ref.png"),
                  ("Seeds", "301 and 302"), ("Size", "768 × 1344, 8-bit")],
                 "gen/log.jsonl rows for CHAR-HARI-PHONE · prompts/image_prompts.json · reference = Shriram's pick B (SHRIRAM-DECISIONS.md)")},
 {"beat_id": "B06", "act": "TRACE-RAW",
  "role_note": "Asset trace 3/5: raw outputs (copied from gen/raw with hashes; also in the committed contact sheet). Labelled NOT in-engine.",
  "narration_text": "Step three, raw output. None of this is in the game yet. Same prompt, two seeds. Seed three-oh-two was the first one wired in, until Shriram spotted it in a playtest screenshot: a second phone at the other ear. It's rejected. Seed three-oh-one, one phone, is in the build now: proposed by Claude, approved by Shriram.",
  "shot": figure("Step 3 · Raw output", "RAW GENERATION · not in-engine footage",
                 'evidence/asset-trace/B-raw-board.png',
                 [("Seed 301", "one phone · in the build"), ("Seed 302", "two phones · rejected"),
                  ("Caught by", "Shriram, playtest screenshot"), ("Pick", "Claude proposed, Shriram approved")],
                 "gen/raw/CHAR-HARI-PHONE_klein_s301.png, _s302.png (hashes in SOURCES.md) · gen/decisions.json · circle added for the film")},
 {"beat_id": "B07", "act": "TRACE-EDIT",
  "role_note": "Asset trace 4/5: logged edits (gen/edit_log.jsonl row for s302). Trim box drawn from the logged numbers.",
  "narration_text": "Step four, three logged edits. Rembg cuts out the figure, and the floor shadow goes too. A trim to the figure's box. A resize to six hundred eighty pixels, centred on the legs. My reading: the sprite mirrors around its centre, so his feet stay put when he turns.",
  "shot": figure("Step 4 · Three edits to a game file", "EDITS · gen/edit_log.jsonl",
                 'evidence/asset-trace/B-edit-board.png',
                 [("Cutout", "rembg, isnet-anime"), ("Trim", "to the figure's bbox"),
                  ("Scale", "680 px tall, Lanczos"), ("Centre", "on the legs")],
                 "gen/edit_log.jsonl (src gen/raw/CHAR-HARI-PHONE_klein_s301.png → godot/assets/art/hari/phone.png) · trim box overlay drawn from the logged bbox")},
 {"beat_id": "B08", "act": "CODE",
  "role_note": "Asset trace 5/5 (code): state name → art file. Paired result B09.",
  "narration_text": "Step five, one function in Hari's script. When the story changes his state, it lowercases the name, so phone becomes phone dot p n g. The billboard then scales any image to exactly one point seven five metres tall. The text label only shows if the art is missing.",
  "shot": workbench("B08", "Step 5 · State name → art file",
                    [{"label": "PHONE →", "value": "art/hari/phone.png"},
                     {"label": "billboard_art.gd", "value": "pixel_size = height_m / texture height"},
                     {"label": "hari_spec.gd", "value": "HEIGHT_M = 1.75"}],
                    [(0.12, 'var key', 'state name → lowercase file key'), (0.35, 'ART_DIR + key', 'ART_DIR + key + .png'),
                     (0.8, 'label.visible', 'label only on placeholders')],
                    "Godot editor reconstruction")},
 {"beat_id": "B09", "act": "RESULT",
  "role_note": "Result of B08 in real play: PHONE → IDLE at call end → WALK → TALK at Krishna.",
  "narration_text": "Here's that function at work. The call ends, and phone becomes idle. He walks, and the walk image takes over, flipped or not by direction. At Krishna, talk. One height, feet on the marble. " + WALK_LINE,
  "shot": gameplay("B09", [{"at": "0.1", "event": "call closes: PHONE → IDLE"}, {"at": "0.25", "event": "D held: WALK along the deck"},
                           {"at": "0.75", "event": "E at Krishna: TALK"}],
                   "Paired result for hari.gd _show_state.")},
 {"beat_id": "B10", "act": "CODE",
  "role_note": "Timeline one-shots. Paired result B11 (real T fast-forward, overhear, 1:40 keys).",
  "narration_text": "Now the night. Every timeline event sits behind a flag that resets each loop. Past one-forty, Advay arrives once. At five-fifty, dawn runs once. Holding T makes the clock eight times faster, through the same checks, so fast-forward can't skip an event.",
  "shot": workbench("B10", "The night: one flag per event",
                    [{"label": "ADVAY_TIME", "value": "1:40 AM (loop_state.gd)"},
                     {"label": "DAWN_TIME", "value": "5:50 AM"},
                     {"label": "FAST_FORWARD", "value": "8.0 while T is held"}],
                    [(0.15, 'flags.ADVAY_DONE', 'Advay: once per loop'), (0.45, 'flags.DAWN_DONE', 'dawn: once per loop'),
                     (0.75, 'clock_minutes = minf', 'every tick passes the same checks')],
                    "Godot editor reconstruction")},
 {"beat_id": "B11", "act": "RESULT",
  "role_note": "Result of B10: driver holds the real T key; 1:21 overhear → clue chime; 1:40 at 1x Advay takes keys → keys SFX + clue 2.",
  "narration_text": "Here it is, played. The driver holds the real T key, and the clock races. At one twenty-one, Manikandan is on the phone to Selvam, and Hari leans in to overhear. Clue saved: a notes card and a chime. Then one-forty, at normal speed. Advay takes the keys. A jingle, and the second clue.",
  "shot": gameplay("B11", [{"at": "0.05", "event": "T held: HUD shows >> x8; walk back to the SUV"},
                           {"at": "0.4", "event": "E: OVERHEAR line; clue_saved KNOW_SELVAM"},
                           {"at": "0.75", "event": "1:40: Advay takes keys; keys_exchanged; clue_saved KNOW_KEYS"}],
                   "Fast-forward is the game's own T key, disclosed.")},
 {"beat_id": "B12", "act": "CODE",
  "role_note": "SoundBank listens only. Paired result B13 (recorded test output + this take's counts).",
  "narration_text": "Sound only listens. The sound bank hangs off the logic's signals and never changes game state. One sound per event is guaranteed upstream, by those flags, so it can be tested without listening.",
  "shot": workbench("B12", "Sound only listens",
                    [{"label": "SFX bus", "value": "phone_buzz · clue_saved · keys_exchanged · dawn_crash · safe_dawn"},
                     {"label": "Music bus", "value": "party_loop + gaana_loop"},
                     {"label": "trigger_counts", "value": "counts every request (tests read it)"}],
                    [(0.12, 'phone_buzz', 'loop start → buzz'), (0.35, 'keys_exchanged', 'keys change hands → jingle'),
                     (0.6, 'dawn_crash', 'dawn → crash or safe dawn')],
                    "Godot editor reconstruction")},
 {"beat_id": "B13", "act": "RESULT",
  "role_note": "Result of B12: recorded output of tests/test_sound_triggers.gd on the frozen build + this capture's driver counts. Image is the actual stdout, rendered.",
  "narration_text": "The test plays both loops through the logic, mashes E, holds it down, and counts every request. Buzz twice, clue three times, keys twice, crash once, safe dawn once, even with both buses muted. This capture's driver counted the same. What it can't tell you is whether they sound right.",
  "shot": figure("Exactly one sound per event", "RECORDED OUTPUT · frozen build",
                 'evidence/tests/B13-test-output.png',
                 [("phone_buzz", "2"), ("clue_saved", "3"), ("keys_exchanged", "2"), ("dawn · safe", "1 · 1")],
                 f"tests/test_sound_triggers.gd stdout, run on the isolated copy at build {B8} · capture driver summary row")
  | {"evidence_media": "media/B13.mp4"}},
 {"beat_id": "B14", "act": "GAME-AUDIO", "kind": "game_audio",
  "role_note": "REQUIRED no-narration segment: the slice's own audio (music fade, dawn_crash horn/screech, white-out, 8 PM phone_buzz). narration_text empty; audio_file = mp3/game/B14.wav cut from the same frames. Not in any component, not a result beat, not between a code beat and its result.",
  "narration_text": "",
  "shot": gameplay("B14", [{"at": "0.0", "event": "5:49 AM, party music thinned"}, {"at": "0.25", "event": "dawn_crash: headlights, shake, horn + screech"},
                           {"at": "0.6", "event": "white-out; WHITEOUT pose"}, {"at": "0.85", "event": "8:00 PM loop 2: buzz, STARTLED"}],
                   "Game audio only, no narration.",
                   label="GAME AUDIO · NO NARRATION · scripted-input capture · real engine run", game_audio_db=-8.0)},
 {"beat_id": "B15", "act": "PLAY",
  "role_note": "Loop 2: STARTLED wake already seen; the choice gated on both clues; KEYS state; keys SFX + clue 3.",
  "narration_text": "That was the slice's own sound: the music fading, a horn and a screech you never see, then eight PM again. Loop two. Hari is in shock, and the call that repeats word for word proves it. Now the choice exists, because both clues are in his notes. Ask about Selvam. Manikandan keeps the keys: keys pose, a jingle, and a third note.",
  "shot": gameplay("B15", [{"at": "0.05", "event": "walk to the SUV"}, {"at": "0.2", "event": "choice: > Ask about Selvam; cursor down and back"},
                           {"at": "0.85", "event": "KEYS pose; keys travel to Manikandan; clue KEYS_WITH_MANI"}],
                   "Loop 2 choice and the keys kept.")},
 {"beat_id": "B16", "act": "PLAY",
  "role_note": "Loop 2: 1:40 refusal (no keys SFX: keys don't move); T to dawn at the railing; safe_dawn; RELIEF; end card.",
  "narration_text": "One-forty. Advay asks and gets refused. No jingle this time, because the keys didn't move. Fast-forward to dawn at the railing: waves and crows instead of a horn, Hari's relief pose, a sunrise, then the end card. But someone is missing.",
  "shot": gameplay("B16", [{"at": "0.05", "event": "1:40: Advay refused caption"}, {"at": "0.45", "event": "T held; walk to the railing"},
                           {"at": "0.75", "event": "safe_dawn; RELIEF; sunrise"}, {"at": "0.9", "event": "end card"}],
                   "Safe dawn and the end of the slice.")},
 {"beat_id": "B17", "act": "CODE",
  "role_note": "Cause → effect: revision R1 (TEST-REPORT §8). Paired result B18 (before/after screenshots).",
  "narration_text": "One cause and effect from the revision log. Early screenshots read as lavender dusk, not one AM. The fix is these colour stops: night ambient down to one-zero-zero-f-two-six, moonlight down to zero point zero eight, and brighter string lights.",
  "shot": workbench("B17", "Revision R1 · the night, in numbers",
                    [{"label": "Before (TEST-REPORT R1)", "value": "ambient 1b1a3c · moonlight 0.25 · lights 1.6"},
                     {"label": "After", "value": "ambient 100f26 · moonlight 0.08"},
                     {"label": "deck_dressing.gd", "value": "light_energy = 2.8"}],
                    [(0.2, '1290.0', '9:30 PM stop: deep night'), (0.5, '1680.0', 'held until 4 AM')],
                    "Godot editor reconstruction")},
 {"beat_id": "B18", "act": "RESULT",
  "role_note": "Result of B17: evidence/revisions/R1-lighting-before/after.jpg (scripted screenshots, labelled).",
  "narration_text": "Before and after, the same moment at one-forty, in scripted screenshots. Before, the deck glows lavender, like dusk. After, the shadows go dark and the warm light sits on the marble. Same scene, three values changed.",
  "shot": figure("R1 · before and after", "SCRIPTED SCREENSHOTS · test API, not played footage",
                 'evidence/asset-trace/B-r1-board.png',
                 [("Deck", "lavender dusk → night"), ("Light", "warm pools on marble"),
                  ("Values", "ambient · moon · lights"), ("Source", "TEST-REPORT §8, R1")],
                 "evidence/revisions/R1-lighting-before.jpg, R1-lighting-after.jpg · TEST-REPORT.md R1")
  | {"evidence_media": "media/B18.mp4"}},
 {"beat_id": "B19", "act": "TESTS",
  "role_note": "What was tested and what it doesn't prove (TEST-REPORT §2). RE-VERIFY numbers at freeze.",
  "narration_text": "Tested by script: sound counts, the audio mix, loop logic, a scene smoke test, every generated asset, and the music seams. All pass. Shriram played it four times. His notes, motion too static, loop two repeating itself, backgrounds slapped on, effects he couldn't hear, drove the revisions.",
  "shot": remotion("GodotDesignBoard", {
      "title": "What was tested", "section": "TEST-REPORT.md · what these checks do NOT prove",
      "excerpt": "The sound test counts requests to SoundBank, not audible output.\nThe seam check proves there is no sample discontinuity, not that the loop is musically seamless.\nThe test API jumps the clock (test_advance_to).",
      "source": f"evidence/tests/*.txt (re-run on the isolated copy) · TEST-REPORT.md §2 (excerpt shortened) · seam check: tools/check/loop_seam_check.py PASS · build {B8}",
      "status": "AUTOMATED · re-run on the frozen build; plus 4 human playtests", "visualLabel": "Results", "layout": "cards",
      "cards": [{"label": "Sound triggers", "text": SUMMARY['test_sound_triggers.gd']}, {"label": "Loop logic", "text": SUMMARY['test_loop_logic.gd']},
                {"label": "Audio mix", "text": SUMMARY['test_audio_mix.gd']}, {"label": "Assets + smoke", "text": SUMMARY['test_assets_present.gd'].split(',')[0] + ' · ' + SUMMARY['test_slice_smoke.gd'].split(',')[0]}],
      "cue_fracs": [{"frac": 0.1, "card": 0}, {"frac": 0.2, "card": 1}, {"frac": 0.3, "card": 2}, {"frac": 0.4, "card": 3}], "cues": []},
      [{"at": "0.1", "event": "four result cards"}, {"at": "0.5", "event": "the NOT-proven excerpt"}])},
 {"beat_id": "B20", "act": "CREDITS",
  "role_note": "Human vs AI, model per asset, source revision (SOURCES.md, SHRIRAM-DECISIONS.md).",
  "narration_text": f"Who did what. Shriram wrote the story, cast and setting, chose two-and-a-half D, picked the reference style, playtested four times, and approved every other asset pick, which Claude proposed. Claude wrote the code, prompts and docs. Every asset came from a local model. Build snapshot {' '.join(B8[:4])}.",
  "shot": remotion("GodotDesignBoard", {
      "title": "Who did what", "section": "SOURCES.md · who did what",
      "excerpt": "Shriram: story, characters, setting, tone; 2.5D Telltale style; reference pick B (\"that kind of style, which matches life is strange kind of game like telltale style\"); 4 playtests; approved Claude's other asset picks and the dialogue.\nClaude: code, prompts, docs, code-drawn sketches; ran the generations; proposed the other asset picks.\nModels: every art, SFX and music asset.",
      "source": f"SOURCES.md, design/input/SHRIRAM-DECISIONS.md · Z-Image-Turbo used only for comparison · build {B8} (SHA-256 in SOURCES.md)",
      "status": "CREDITS · git 13f772c · snapshot " + B8, "visualLabel": "Which model made which asset", "layout": "cards",
      "cards": [{"label": "FLUX.2 [klein] 4B", "text": "Hari ×10, NPCs, environments"}, {"label": "Stable Audio Open 1.0", "text": "the 5 sound effects"},
                {"label": "MusicGen stereo-medium", "text": "party + gaana loops"}, {"label": "rembg", "text": "background removal"}],
      "cue_fracs": [{"frac": 0.55, "card": 0}, {"frac": 0.68, "card": 1}, {"frac": 0.78, "card": 2}], "cues": []},
      [{"at": "0.05", "event": "Shriram / Claude / models excerpt"}, {"at": "0.55", "event": "model cards light"}])},
 {"beat_id": "B21", "act": "VERDICT", "lead_silence_s": 0.5,
  "role_note": "Verdict: working / uncertain / known limits / next.",
  "narration_text": "Let's recap with Claude. Working: ten Hari states in a real 3D night, five sounds tied to logic, and one full turn of the loop. Uncertain: whether a first-time player reads the dawn with the sound off. Known limit: Hari, the cast and the SUV are flat billboards, and they read as 2D when the camera turns. Next, in A3: replace the SUV, the rock and the fence with Blender models.",
  "shot": remotion("ClaudeVerdictArtifact", {
      "artifactTitle": "Verdict", "artifactHeading": f"Vidiyum Mun slice, build {B8}.", "brandLabel": "@NikBearBrown",
      "artifactLines": ["Works: 10 Hari states in a 3D night, 5 sounds on logic events, one full loop turn.",
                        "Uncertain: does a first-time player read the dawn with the sound off?",
                        "Known limit: billboard characters and the SUV read as 2D when the camera turns.",
                        "Next (A3): replace the SUV, the rock and the fence with Blender models."]},
      [{"at": "0.1", "event": "verdict card"}, {"at": "0.25", "event": "works"}, {"at": "0.45", "event": "uncertain"},
       {"at": "0.65", "event": "limits"}, {"at": "0.85", "event": "next"}])},
 {"beat_id": "B22", "act": "HANDOFF",
  "role_note": "HANDOFF LAW: prompt read verbatim, discussed; signs off 'Liam, in for Bear.'",
  "narration_text": "Your turn. I have a character sheet and one generated reference. For one pose: one, write an edit prompt that changes only the pose clause. Two, name the silhouette risk at my in-game pixel height. Three, list the cleanup steps, and a check that the feet stay put when the sprite flips. Then check its pixel math against your own screenshot. Liam, in for Bear.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Your turn.", "topic": TOPIC, "segment": "Your One Pose",
      "command": "I have a character sheet and one generated reference. For one pose: (1) write an edit prompt that changes only the pose clause; (2) name the silhouette risk at my in-game pixel height; (3) list the cleanup steps, and a check that the feet stay put when the sprite flips.",
      "runningText": "paste this into Claude…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["Pose clause drafted.", "Silhouette risk at your pixel height.", "Cleanup + feet-planted check: verify in your engine."],
      "animateTyping": True},
      [{"at": "0.05", "event": "'Your turn.'"}, {"at": "0.1", "event": "prompt types"}, {"at": "0.75", "event": "result lines"}])},
 {"beat_id": "B23", "act": "OUTRO", "kind": "outro_voice", "tail_hold_s": 1.0,
  "role_note": "OUTRO-LOCK: ClaudeTitleOutro, exact title, @NikBearBrown, slug-seeded mascot, spoken never scored; no game audio.",
  "narration_text": TITLE + ". At Nik Bear Brown.",
  "shot": remotion("ClaudeTitleOutro", {"title": TITLE, "slug": SLUG},
      [{"at": "0.0", "event": "title card"}, {"at": "0.3", "event": "@NikBearBrown + mascot"}])},
]

GAMEPLAY_QC = {
    "contrast_regions": [{"label": "capture caption band (film label)", "box": [0.074, 0.905, 0.62, 0.955]}],
    "contrast_reason": "Real engine footage reframed at 85 % inside title-safe. The film's essential text is the caption band under the footage; the game's own HUD/dialogue text belongs to the footage (it is absent in the intro and whited out at the crash) and is inspected by eye in _qc frame samples, not by the contrast heuristic."}
for b in beats:
    if b["shot"].get("type") == "GAMEPLAY":
        b["qc"] = GAMEPLAY_QC
    if b["beat_id"] == "B01":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: types token by token (EXECUTIVE-SUMMARY LAW)."}

sheet_path = REEL / "beat_sheet.json"
old = {b["beat_id"]: b for b in json.loads(sheet_path.read_text()).get("beats", [])} if sheet_path.exists() else {}
for b in beats:
    b.setdefault("voice", "am_onyx"); b.setdefault("engine", "kokoro")
    prev = old.get(b["beat_id"])
    if prev and prev.get("narration_text") == b["narration_text"]:
        for k in ("audio_file", "actual_duration_s", "speech_duration_s", "render_duration_s", "action_duration_s", "hold_s"):
            if k in prev: b[k] = prev[k]

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "mode": "walker",
    "brand": "claude-liam", "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "crop",
    "captions": False, "channel": "@NikBearBrown", "channel_title": "@NikBearBrown", "folderLabel": "@NikBearBrown",
    "greeting": "Vanakkam, Liam", "greeting_note": "hello lexicon: Vanakkam (Tamil), fits the Chennai setting. Wagwan is Bear-only.",
    "persona": "Liam (in for Bear)", "in_for_bear": True,
    "audience": "CSYE 7270 reviewers and makers generating assets for a Godot slice",
    "game": {"name": "walker-vidiyum-mun-shriram-a", "build_id": BUILD, "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
             "renderer": "Forward+ (Metal)"},
    "capture_log": f"capture/{EVENT_SRC}", "fps": 30},
  "beats": beats}
sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
words = sum(len(b['narration_text'].split()) for b in beats)
game = sum(R[k][1] - R[k][0] for k in R)
print(f"wrote {sheet_path.name} · {len(beats)} beats · {words} narration words (~{words / 2.55:.0f} s) · gameplay action {game:.1f} s · log {EVENT_SRC}")
for k, (a, b) in R.items():
    print(f"  {k}: {a:.2f}–{b:.2f} s ({b - a:.1f} s)")
for k, e in EX.items():
    print(f"  {k}: godot/{e['path']} {e['start_line']}–{e['end_line']}")
