# FACTCHECK: "Vidiyum Mun, Built from Boxes" (A3, godot-gamedev walker)

Source revision shown: git `81c1666` (recorded in `evidence/source-revision.txt` at 2026-10-15 21:02 EDT, when the checks were run). godot/ snapshot id in `beat_sheet.json` metadata.

| Beat | Claim (narration / screen) | Source | Status |
|---|---|---|---|
| B00 | Prompt on screen is a reconstruction, not a transcript | labelled in the topic line | by construction |
| B00 | SUV 4.60 × 1.90 × 1.70 m, 456 tris; shrine 1.20 m, 266; fence 2.40 m, 108; 31 checks 0 failed | `evidence/check_a3_assets.out.txt` | verified (headless run, this session) |
| B02 | Chat beside Blender shows the plan ending "reply 'approved'", then "approved" and Claude's reply ("The SUV is saved to blender/suv.blend…") | recording frames at 362 s and 375 s viewed | verified by frame |
| B02 | Clip time 7:52–7:53 PM | macOS menu-bar clock in frame reads 7:52 PM at 352 s and 7:53 PM at 382 s (first cut mislabelled 7:51–7:52; fixed) | verified by frame |
| B03 | Excerpt = `tools/blender/build_suv.py` lines 53–62 (SUV call 1, build 1), verbatim | anchored copy in `tools/author_sheet.py` | verified (copied by script) |
| B04 | Chassis, then cabin, then four wheels appear (build 1) | recording frames 125 s (chassis), 140 s (cabin), 150–160 s (wheels) viewed | verified by frame. NOTE: the brief to this film said "~19:49–19:53"; the frames show the build at 19:48–19:49 (offset 113–173 s); the film uses the frame-verified times |
| B04 | Build 1 = 200 triangles | `build_suv.py` line 243 comment ("shapes: 6 triangles: 200") | verified |
| B04 | Shriram: "looks pretty basic" | `build_suv.py` lines 255–257 (quoted verdict) | verified |
| B04 | Final SUV in Godot | `evidence/a3/godot-suv-front.png` (engine screenshot) | verified (labelled) |
| B05 | Sign duplicated twice, copies deleted, moved to centre/in front, typed X 0, Y −0.03 | recording frames 2710–2770 (three signs), 2800–2830 (copies gone, moving), 2980–3040 (Item tab X 0 m, Y −0.03 m) viewed | verified by frame |
| B05 | ~5 cm off by eye; "front and back depend on the Y axis" | Shriram's own words as supplied for this film | supplied fact (Shriram) |
| B06 | Excerpt `godot/tests/a3_measure.gd` 29–41; floor from vertices, not a collider; earlier floor check fooled itself | file lines 5–6 comment ("Module 3's floor check stopped on the object's own collider") | verified |
| B07 | 31 checks, 0 failed; SUV 4.600 × 1.700 × 1.900, 456 ≤ 480, lowest vertex +0.0000; shrine 266; fence 108 | `evidence/check_a3_assets.out.txt` (real stdout, exit 0) | verified |
| B08 | Excerpt `godot/tests/check_a3_selftest.gd` 64–78; breaks: float 0.5 m, ×0.1, on side, colour white, budget 40 | file | verified |
| B09 | 17/17 | `evidence/check_a3_selftest.out.txt` (exit 0) | verified |
| B09 | Correct stand-in once failed (revision-1 steel colours); stand-in updated, assertion unchanged | check_a3_selftest.gd lines 26–28 comment; supplied facts; commit 81c1666 message | verified |
| B10 | Excerpt `godot/scenes/a3_showcase.gd` 13–16; goddess faced the SUV tail; slot yaw −90; asset transform stays identity | file lines 13–16 | verified |
| B11 | Before/after; lamp flicker is a scene OmniLight3D | `evidence/a3/godot-shrine-front-BEFORE-facing-suv.png`, `godot-shrine-front.png`; a3_showcase.gd lines 46–54, 120 | verified (screenshots viewed in film QC) |
| B11 | Hari's 1.75 m billboard beside the assets; SUV rear/below; fence side | a3_showcase.gd header; `godot-suv-rear.png`, `godot-suv-below.png`, `godot-fence-side.png` | verified |
| B12 | Claude's errors: icosphere 80 vs 20; build-2 underside; wheel silver; rock 1.14 m; sign floated; export failed twice; goddess facing; self-test colours | supplied verified facts; chat frame at 375 s shows the icosphere self-correction | supplied fact |
| B12 | Look check (paraphrased): shrine looks great; SUV fine for six shapes, real design smoother; fence one segment of a long electrified line; red = private property | supplied Shriram's words | supplied fact (paraphrase) |
| B13 | Human vs AI split; revision 81c1666 | supplied facts; `git rev-parse --short HEAD` | verified |
| B14 | Checked / uncertain / limits / next step (slice.tscn) | supplied facts | supplied fact |

Pronouns: Shriram is referred to by name or they/them only.
