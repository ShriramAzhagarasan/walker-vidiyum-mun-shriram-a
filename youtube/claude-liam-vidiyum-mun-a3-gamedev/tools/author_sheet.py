#!/usr/bin/env python3
"""Author beat_sheet.json for the A3 film "Vidiyum Mun, Built from Boxes" (godot-gamedev, walker mode).

Code excerpts are located by an anchor line and copied verbatim (line numbers follow). Godot excerpts
(godot/...) are GodotDevWorkbench code beats and are hash-checked by verify_gamedev.py. The one Blender
excerpt (tools/blender/build_suv.py) lives outside godot/, so it is shown verbatim in a GodotDesignBoard
excerpt panel with its path and lines (verify_gamedev.py only certifies sources inside the game folder).
Re-running keeps measured audio fields for beats whose narration did not change.
"""
import json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GODOT = REPO / 'godot'
sys.path.insert(0, str(REEL / 'tools'))
from source_snapshot import snapshot  # noqa: E402

TITLE = "Vidiyum Mun, Built from Boxes"
SLUG = "claude-liam-vidiyum-mun-a3-gamedev"
TOPIC = "WALKER · GODOT GAMEDEV · A3"
PROJECT = "Vidiyum Mun"
BUILD, _rows = snapshot(REPO)
B8 = BUILD[:8]
REV = (REEL / 'evidence/source-revision.txt').read_text().split()[0]
REC = "SHRIRAM'S SCREEN RECORDING"

def excerpt(root, rel, anchor, n, first=False):
    lines = (root / rel).read_text().splitlines()
    hits = [i for i, l in enumerate(lines) if anchor in l]
    if first:
        hits = hits[:1]          # build_suv.py repeats the root lookup in every call; call 1 is the first
    if len(hits) != 1:
        raise SystemExit(f'anchor {anchor!r} matched {len(hits)} lines in {rel}')
    s = hits[0]
    return {'path': rel, 'start_line': s + 1, 'end_line': s + n, 'text': '\n'.join(lines[s:s + n])}

def line_of(ex, needle):
    for i, l in enumerate(ex['text'].split('\n')):
        if needle in l:
            return ex['start_line'] + i
    raise SystemExit(f'{needle!r} not in excerpt {ex["path"]}')

SUV_EX = excerpt(REPO, 'tools/blender/build_suv.py', 'root = bpy.data.objects["suv"]', 10, first=True)
EX = {
    'B06': excerpt(GODOT, 'tests/a3_measure.gd', 'for s in mi.mesh.get_surface_count():', 13),
    'B08': excerpt(GODOT, 'tests/check_a3_selftest.gd', 'var n := _fence(); n.position.y = 0.5', 15),
    'B10': excerpt(GODOT, 'scenes/a3_showcase.gd', "## The shrine's goddess faces the asset's +X", 4),
}

def remotion(pattern, props, show, **kw):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "show": show,
            "remotion": {"pattern": pattern, "props": props}, **kw}

def workbench(bid, title, notes, cues):
    ex = EX[bid]
    return remotion("GodotDevWorkbench", {
        "mode": "code", "title": title, "project": PROJECT, "path": "godot/" + ex['path'],
        "source": f"Godot editor reconstruction · godot/{ex['path']} lines {ex['start_line']}–{ex['end_line']} · git {REV}",
        "code": ex['text'], "startLine": ex['start_line'], "codeFontSize": 27,
        "inspectorLabel": "Source notes — not Inspector values", "notes": notes,
        "cue_fracs": [{"frac": f, "line": line_of(ex, needle), "label": lab} for f, needle, lab in cues],
        "cues": [], "output": [f"Godot editor reconstruction · git {REV}"]},
        [{"at": str(f), "event": f"line highlight: {lab}"} for f, _, lab in cues])

def own(bid, label, show, note, segments):
    """Own media built by tools/make_media.py: recording clips (labelled) and real engine/terminal stills."""
    return {"type": "GAMEPLAY", "class": "SHOW", "source": "own", "treatment": "none", "label": label,
            "segments": segments, "evidence_media": f"media/{bid}.mp4", "show": show, "note": note}

beats = [
 {"beat_id": "B00", "act": "ASK",
  "role_note": "Walker B00. Illustrative reconstruction of the ask (labelled), never a transcript.",
  "narration_text": "Vanakkam, this is Liam, in for Bear. The prompt on screen is a reconstruction, not a transcript. Assignment three: three Blender models for Vidiyum Mun, built by Claude through the Blender M C P, judged by Shriram, and checked in Godot.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Vanakkam, Liam", "topic": "ILLUSTRATIVE RECONSTRUCTION · NOT A TRANSCRIPT", "segment": "Vidiyum Mun · A3",
      "command": "Please use Walker to convert my game design document about Vidiyum Mun, a time-loop mystery on a fenced private beach on ECR, Chennai, into three game assets built in Blender through the MCP: the SUV whose keys decide the dawn crash, Manimekala's rock shrine, and one segment of the illegal fence. Six basic shapes each, flat colours, exported to Godot.",
      "runningText": "reading godot/ and CHANGE-BRIEF.md…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["SUV 4.60 × 1.90 × 1.70 m · 456 triangles.", "Rock shrine 1.20 m · 266 · fence 2.40 m · 108.", "Godot headless: 31 checks, 0 failed."]},
      [{"at": "0.05", "event": "composer; greeting"}, {"at": "0.15", "event": "topic: ILLUSTRATIVE RECONSTRUCTION"},
       {"at": "0.25", "event": "the Walker ask types"}, {"at": "0.7", "event": "three result lines"}])},
 {"beat_id": "B01", "act": "BLUF", "lead_silence_s": 0.6,
  "role_note": "Hesitant writer; single-word correction 'downloaded' -> 'built'.",
  "narration_text": "Three models, built for the game, not downloaded. Each one is six basic shapes, placed by code Claude ran inside Blender. Then measured in Godot, and judged by Shriram's eye.",
  "shot": remotion("BrutalistHesitantWriter", {
      "contextTitle": "What this film shows",
      "text": "Three models, downloaded for the game.\nSix shapes each, placed by code in Blender.\nMeasured in Godot. Judged by Shriram.",
      "triggerWords": "downloaded", "replacementWords": "built",
      "fontSize": 84, "lineSpacing": 2.6, "align": "center", "seed": "vidiyum-a3",
      "mistakeRate": 2, "hesitateWithin": 0, "hesitateBetween": 1, "charMs": 8,
      "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
      [{"at": "0.08", "event": "line one types"}, {"at": "0.3", "event": "'downloaded' struck; 'built' typed"},
       {"at": "0.55", "event": "lines two and three"}])},
 {"beat_id": "B02", "act": "FOOTAGE",
  "role_note": "Shriram's own recording: the Claude chat beside Blender, the SUV plan and Shriram's 'approved'.",
  "narration_text": "This is Shriram's own screen recording, cropped to the Claude chat beside Blender. Claude laid out the SUV plan, six shapes with sizes and colours, and asked for one word before building anything. Shriram typed it: approved. Then Claude answers, already building.",
  "shot": own("B02", f"{REC} · chat beside Blender, 7:52–7:53 PM · 2× speed · cropped",
              [{"at": "0.0", "event": "chat: the plan ends 'reply \"approved\"'"}, {"at": "0.5", "event": "'approved' (7:48 PM) and Claude's reply"}],
              "The prompt and Claude's reply, from Shriram's recording.",
              [{"kind": "clip", "src": "rec", "start": 352.0, "end": 382.0, "speed": 2.0, "crop": [600, 0, 1900, 2234]}])},
 {"beat_id": "B03", "act": "CODE-BLENDER",
  "role_note": "One execute_blender_code body, verbatim (tools/blender/build_suv.py, outside godot/; GodotDesignBoard excerpt).",
  "narration_text": "Here's one of the calls Claude ran, saved word for word in build S U V dot p y. Add a one metre cube. Name it S U V chassis. Scale it to four point six, by one point eight, by zero point seven five. Apply the scale, so the node stays at one. Then a flat body colour.",
  "shot": remotion("GodotDesignBoard", {
      "title": "One call Claude ran in Blender", "section": f"tools/blender/build_suv.py · lines {SUV_EX['start_line']}–{SUV_EX['end_line']} · SUV call 1 (build 1), verbatim",
      "excerpt": SUV_EX['text'],
      "source": "",
      "status": f"CODE · execute_blender_code · mcp-for-blender 2.1.9 · Blender 5.2.2 LTS · git {REV}", "visualLabel": "What it does", "layout": "cards",
      "cards": [{"label": "Shape", "text": "one cube, 1 m"}, {"label": "Size", "text": "4.60 × 1.80 × 0.75 m"},
                {"label": "Scale", "text": "applied → node stays 1, 1, 1"}, {"label": "Colour", "text": "flat #2e2d38"}],
      "cue_fracs": [{"frac": 0.25, "card": 0}, {"frac": 0.45, "card": 1}, {"frac": 0.65, "card": 2}, {"frac": 0.82, "card": 3}], "cues": []},
      [{"at": "0.05", "event": "verbatim excerpt"}, {"at": "0.25", "event": "cards light in order"}])},
 {"beat_id": "B04", "act": "RESULT-BLENDER",
  "role_note": "Result of B03: Shriram's recording, the SUV appearing part by part (4x), then the final SUV in Godot (engine screenshot).",
  "narration_text": "And here it lands, in Shriram's recording, four times faster. The chassis appears, then the cabin, then four wheels. That was build one: two hundred triangles. Shriram's verdict: it looks pretty basic. Three more builds followed, each from what Shriram saw, to this one in Godot.",
  "shot": own("B04", f"{REC} · Blender, 7:48–7:49 PM · 4× speed",
              [{"at": "0.0", "event": "chassis, cabin, wheels appear (build 1)"}, {"at": "0.75", "event": "final SUV, Godot engine screenshot"}],
              "Build 1 appearing; final build 4 in Godot.",
              [{"kind": "clip", "src": "rec", "start": 113.0, "end": 173.0, "speed": 4.0},
               {"kind": "still", "src": "evidence/a3/godot-suv-front.png", "min": 4.0,
                "label": "GODOT ENGINE SCREENSHOT · a3_showcase.tscn · final SUV (build 4) · git " + REV}])},
 {"beat_id": "B05", "act": "HAND-EDIT",
  "role_note": "Shriram's own hand edit by mouse (recording 20:31–20:36, 16x).",
  "narration_text": "Now Shriram's own hand edit, by mouse, sixteen times faster. The fence sign floated between the ropes. Shriram duplicated it twice, then deleted the copies to stay at six shapes, and moved it to the centre, in front. By eye, it sat about five centimetres off the rope. Typing X zero and Y minus zero point zero three put it flush. The lesson, in Shriram's words: front and back depend on the Y axis.",
  "shot": own("B05", f"{REC} · Shriram's hand edit in Blender, 8:31–8:36 PM · 16× speed",
              [{"at": "0.1", "event": "sign duplicated twice"}, {"at": "0.4", "event": "copies deleted; sign dragged to centre"},
               {"at": "0.85", "event": "Item tab: X 0, Y −0.03"}],
              "Hand edit: duplicate, delete, move, exact values.",
              [{"kind": "clip", "src": "rec", "start": 2696.0, "end": 3016.0, "speed": 16.0}])},
 {"beat_id": "B06", "act": "CODE",
  "role_note": "Measurement from mesh vertices (a3_measure.gd). Paired result B07 (headless output).",
  "narration_text": "Then Godot checks the exported files. This loop walks every mesh vertex in world space. The lowest one is the floor height, measured from the mesh, not from a collider, which is how an earlier floor check fooled itself. The same loop counts triangles.",
  "shot": workbench("B06", "Measure from vertices, not a collider",
                    [{"label": "lo / hi", "value": "world-space bounds of every vertex"},
                     {"label": "tris", "value": "index count / 3, per surface"},
                     {"label": "floor rule", "value": "lowest vertex y = 0 ± 0.01 m"}],
                    [(0.2, 'var w := mi.global_transform * v', 'every vertex, in world space'),
                     (0.45, 'lo = lo.min(w)', 'lowest point = the floor height'),
                     (0.8, 'tris +=', 'triangle count')])},
 {"beat_id": "B07", "act": "RESULT",
  "role_note": "Result of B06: actual headless stdout of check_a3_assets.gd, rendered (labelled headless).",
  "narration_text": "The headless run, on this revision. Thirty-one checks, zero failed. The S U V measures four point six, by one point seven up, by one point nine metres, four hundred fifty-six triangles under a budget of four eighty, lowest vertex at zero. The shrine, two sixty-six. The fence, one hundred eight.",
  "shot": own("B07", f"HEADLESS · check_a3_assets.gd stdout · Godot 4.7.2 · git {REV}",
              [{"at": "0.0", "event": "SUV block"}, {"at": "0.8", "event": "31 checks, 0 failed -> PASS"}],
              "Recorded output, not reconstructed.",
              [{"kind": "still", "src": "evidence/check_a3_assets.png", "min": 1.0}])},
 {"beat_id": "B08", "act": "CODE",
  "role_note": "Self-test: deliberately broken stand-ins. Paired result B09.",
  "narration_text": "A check that always passes proves nothing. So the self-test breaks things on purpose: a box stand-in floated half a metre, shrunk to a tenth, laid on its side, a sign colour turned white, a budget squeezed below the triangle count.",
  "shot": workbench("B08", "The check must be able to fail",
                    [{"label": "stand-in", "value": "BoxMesh fence: posts, sign, rope"},
                     {"label": "A3-F1…F7", "value": "predicted failures, each expected to be caught"},
                     {"label": "expect(…, false)", "value": "a pass here would be a test failure"}],
                    [(0.15, 'n.position.y = 0.5', 'floats by 0.5 m'), (0.35, 'n.scale = Vector3(0.1', 'scaled ×0.1'),
                     (0.55, 'n.rotation_degrees = Vector3(90', 'lying on its side'), (0.75, 'Color.WHITE', 'colour lost'),
                     (0.9, 'tight.max_tris = 40', 'over budget')])},
 {"beat_id": "B09", "act": "RESULT",
  "role_note": "Result of B08: actual headless stdout of check_a3_selftest.gd, rendered.",
  "narration_text": "Every break is caught. Seventeen of seventeen. One honest scar: the correct stand-in once failed, because it still wore the first brief's steel colours. The stand-in was updated, the assertion was not. And a pass proves size, scale and orientation, not that a model looks right.",
  "shot": own("B09", f"HEADLESS · check_a3_selftest.gd stdout · Godot 4.7.2 · git {REV}",
              [{"at": "0.0", "event": "correct stand-in passes"}, {"at": "0.5", "event": "each break caught"}, {"at": "0.85", "event": "17 checks, 0 failed"}],
              "Recorded output, not reconstructed.",
              [{"kind": "still", "src": "evidence/check_a3_selftest.png", "min": 1.0}])},
 {"beat_id": "B10", "act": "CODE",
  "role_note": "The slot fix found by a screenshot (a3_showcase.gd). Paired result B11 (engine screenshots, before/after + orbit).",
  "narration_text": "One problem only a picture found. In the showcase row, the goddess faced the asset's plus X: straight at the S U V's tail. The fix turns the shrine's slot by ninety degrees. The slot turns, not the asset, so the check still sees an unrotated model.",
  "shot": workbench("B10", "A screenshot found it; the slot turns",
                    [{"label": "found in", "value": "godot-shrine-front.png (before)"},
                     {"label": "rock_shrine slot", "value": "yaw −90°"},
                     {"label": "asset transform", "value": "stays identity (checked)"}],
                    [(0.2, "goddess faces the asset's +X", 'she faced the SUV tail'),
                     (0.55, 'Turn her slot', 'turn the slot to face the camera'),
                     (0.8, 'SLOT_YAW_DEG', 'rock_shrine: −90°')])},
 {"beat_id": "B11", "act": "RESULT",
  "role_note": "Result of B10 + the running scene: real engine screenshots (before / after; orbit incl. behind and below).",
  "narration_text": "Before: she faces the tail light. After: she faces the camera, lit by a flickering lamp light that lives in the scene, because the model itself can't animate. Then around the running showcase, beside Hari's one point seven five metre billboard: the S U V from behind and from below, wheels on the floor, and the fence from the side.",
  "shot": own("B11", "GODOT ENGINE SCREENSHOTS · a3_showcase.tscn · real renders",
              [{"at": "0.0", "event": "BEFORE: goddess faces the SUV"}, {"at": "0.2", "event": "AFTER: faces the camera"},
               {"at": "0.45", "event": "SUV rear"}, {"at": "0.65", "event": "SUV below"}, {"at": "0.85", "event": "fence side"}],
              "Engine screenshots, labelled; not a recording of motion.",
              [{"kind": "still", "src": "evidence/a3/godot-shrine-front-BEFORE-facing-suv.png", "w": 0.2, "label": "BEFORE THE FIX · goddess faces the SUV's tail · engine screenshot"},
               {"kind": "still", "src": "evidence/a3/godot-shrine-front.png", "w": 0.2, "label": "AFTER · slot yaw −90° · engine screenshot · git " + REV},
               {"kind": "still", "src": "evidence/a3/godot-suv-rear.png", "w": 0.2, "label": "ORBIT · SUV from behind · engine screenshot"},
               {"kind": "still", "src": "evidence/a3/godot-suv-below.png", "w": 0.2, "label": "ORBIT · SUV from below · engine screenshot"},
               {"kind": "still", "src": "evidence/a3/godot-fence-side.png", "w": 0.2, "label": "ORBIT · fence from the side · engine screenshot"}])},
 {"beat_id": "B12", "act": "REVISION",
  "role_note": "What Claude got wrong + Shriram's look check (TEST-REPORT / FACTS).",
  "narration_text": "What Claude got wrong. It priced an icosphere at eighty triangles; it's twenty. It raised the S U V's whole underside when only the nose was meant. It measured the rock at one point one four metres, not one point two. It floated the fence sign, and the export failed twice. Shriram's look check: the shrine looks great. The S U V is fine for six shapes; a real one would be smoother.",
  "shot": remotion("GodotDesignBoard", {
      "title": "What Claude got wrong", "section": f"TEST-REPORT.md + tools/blender/build_*.py comments · git {REV} · look check paraphrased",
      "excerpt": "Icosphere 'subdivisions 1' priced at 80 tris (it is 20).\nSUV build 2 raised the whole underside, not just the nose.\nWheel silver faces didn't apply at first (caught with look).\nRock measured 1.14 m, not 1.20 (stretched).\nFence sign floated between the ropes.\nExport failed twice; in Godot the goddess faced the SUV.\nSelf-test stand-in kept revision-1 colours (1/17 failed).",
      "source": "",
      "status": "REVISION · every fix came from a measurement, a look, a screenshot or Shriram", "visualLabel": "Shriram's look check", "layout": "cards",
      "cards": [{"label": "Shrine", "text": "looks great; goddess and side flame work"}, {"label": "SUV", "text": "fine for 6 shapes; real design smoother"},
                {"label": "Fence", "text": "one segment of a long electrified line"}, {"label": "Sign", "text": "red = 'private property' (no text allowed)"}],
      "cue_fracs": [{"frac": 0.72, "card": 0}, {"frac": 0.84, "card": 1}, {"frac": 0.9, "card": 2}, {"frac": 0.95, "card": 3}], "cues": []},
      [{"at": "0.05", "event": "the wrong list"}, {"at": "0.72", "event": "look-check cards"}])},
 {"beat_id": "B13", "act": "CREDITS",
  "role_note": "Human vs AI; source revision shown on screen.",
  "narration_text": "Who did what. Shriram chose the assets, judged every build, drove every revision, and did the hand edit and the look check. Claude wrote the brief's numbers, all the Blender code, the export, the Godot checks, the showcase scene, and this film. Source revision, eight one c one six six six.",
  "shot": remotion("GodotDesignBoard", {
      "title": "Who did what", "section": f"SOURCES.md · source revision git {REV}",
      "excerpt": "Shriram: chose the three assets; judged every build; asked for every revision (SUV builds 2–4, the goddess relief, the wooden fence); did the hand edit and the look check; recorded the session.\nClaude: brief numbers, every execute_blender_code body, the .glb export, check_a3_assets.gd, the self-test, a3_showcase.tscn, this film.",
      "source": f"git {REV} · godot/ snapshot {B8} · Blender 5.2.2 LTS · mcp-for-blender 2.1.9 · Godot 4.7.2",
      "status": f"CREDITS · source revision {REV}", "visualLabel": "The assets", "layout": "cards",
      "cards": [{"label": "SUV", "text": "the car whose keys decide the dawn"}, {"label": "Rock shrine", "text": "Manimekala's rock, fenced off"},
                {"label": "Fence", "text": "the illegal fence on a public beach"}, {"label": "Revision", "text": f"git {REV}"}],
      "cue_fracs": [{"frac": 0.55, "card": 0}, {"frac": 0.65, "card": 1}, {"frac": 0.75, "card": 2}, {"frac": 0.88, "card": 3}], "cues": []},
      [{"at": "0.05", "event": "Shriram / Claude"}, {"at": "0.88", "event": f"revision {REV}"}])},
 {"beat_id": "B14", "act": "VERDICT", "lead_silence_s": 0.4,
  "role_note": "Verdict: checked / uncertain / limits / next.",
  "narration_text": "Let's recap with Claude. Checked: three models at the briefed size, on the floor, under budget, thirty-one of thirty-one. Uncertain: whether they read at night, under the game's own lighting. A pass can't say. Limits: six-shape silhouettes, and no text on the sign. Next: place all three in the actual night slice.",
  "shot": remotion("ClaudeVerdictArtifact", {
      "artifactTitle": "Verdict", "artifactHeading": f"Vidiyum Mun A3 assets, git {REV}.", "brandLabel": "@NikBearBrown",
      "artifactLines": ["Checked: size, floor, scale, budget, colours, facing · 31/31 headless.",
                        "Uncertain: do they read at night, under the slice's lighting?",
                        "Limits: 6-shape silhouettes; no text on the sign; flame flicker is a Godot light.",
                        "Next: place SUV, shrine and fence in slice.tscn."]},
      [{"at": "0.1", "event": "verdict card"}, {"at": "0.25", "event": "checked"}, {"at": "0.45", "event": "uncertain"},
       {"at": "0.65", "event": "limits"}, {"at": "0.85", "event": "next"}])},
 {"beat_id": "B15", "act": "HANDOFF",
  "role_note": "Your Turn: prompt read aloud; one bounded change + prediction; signs off.",
  "narration_text": "Your turn. Ask Claude for a headless check on one model you exported: size and floor from the mesh vertices, not a collider, triangles against your budget, and one broken stand-in it must catch. Predict which row fails before you run it. Liam, in for Bear.",
  "shot": remotion("ClaudeComposerAsk", {
      "greeting": "Your turn.", "topic": TOPIC, "segment": "Your One Model",
      "command": "Write a Godot headless check for one model I exported from Blender: measure its size and lowest vertex from the mesh vertices (not a collider), count triangles against my budget, and add one deliberately broken stand-in the check must catch.",
      "runningText": "paste this into Claude…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "High",
      "output": ["Size + floor from vertices.", "Triangles vs your budget.", "One broken stand-in: predict, then run."],
      "animateTyping": True},
      [{"at": "0.05", "event": "'Your turn.'"}, {"at": "0.1", "event": "prompt types"}, {"at": "0.75", "event": "result lines"}])},
 {"beat_id": "B16", "act": "OUTRO", "kind": "outro_voice", "tail_hold_s": 1.0,
  "role_note": "OUTRO-LOCK: ClaudeTitleOutro, exact title, @NikBearBrown, slug-seeded mascot; spoken, no jingle.",
  "narration_text": TITLE + ". At Nik Bear Brown.",
  "shot": remotion("ClaudeTitleOutro", {"title": TITLE, "slug": SLUG},
      [{"at": "0.0", "event": "title card"}, {"at": "0.3", "event": "@NikBearBrown + mascot"}])},
]

OWN_QC = {
    "contrast_regions": [{"label": "caption band (film label)", "box": [0.074, 0.905, 0.62, 0.955]}],
    "contrast_reason": "Real footage/screenshots reframed at 85 % inside title-safe; the film's essential text is the caption band. Text inside Shriram's recording, engine screenshots and recorded terminal output belongs to the evidence and is inspected by eye in _qc frame samples."}
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

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "mode": "walker",
    "brand": "claude-liam", "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "crop",
    "captions": False, "channel": "@NikBearBrown", "channel_title": "@NikBearBrown", "folderLabel": "@NikBearBrown",
    "greeting": "Vanakkam, Liam", "greeting_note": "hello lexicon: Vanakkam (Tamil), fits the Chennai setting.",
    "persona": "Liam (in for Bear)", "in_for_bear": True,
    "audience": "CSYE 7270 reviewers and makers building Blender assets for a Godot game",
    "source_revision": REV, "recording": "Shriram's screen recording blendersession.mov (not in git; clips in clips/)",
    "game": {"name": "walker-vidiyum-mun-shriram-a", "build_id": BUILD, "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
             "renderer": "Forward+ (Metal)", "git": REV},
    "fps": 30},
  "beats": beats}
sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
words = sum(len(b['narration_text'].split()) for b in beats)
print(f"wrote {sheet_path.name} · {len(beats)} beats · {words} words (~{words / 2.9:.0f} s) · git {REV} · build {B8}")
print('  build_suv.py', SUV_EX['start_line'], SUV_EX['end_line'])
for k, e in EX.items():
    print(f"  {k}: godot/{e['path']} {e['start_line']}–{e['end_line']}")
