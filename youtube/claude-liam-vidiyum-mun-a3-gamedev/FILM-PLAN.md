# Film plan: A3, "Vidiyum Mun, Built from Boxes" (godot-gamedev, walker mode)

Skill: `../../../brutalist.art/skills/make/godot-gamedev/SKILL.md` (read in full). Teaching unit: **code → visible result**,
with every excerpt beat followed immediately by its result beat (`teaching_contract: code-then-result-v1`).
Liam (Kokoro `am_onyx`), in for Bear. Native 4K, 30 fps. Reel folder: this one. The A2 film is left untouched.

| Beat | Kind | Shows | Source of the visual | Required by the assignment |
|---|---|---|---|---|
| B00 | Walker ask (composer) | "Please use Walker to convert my game design document about Vidiyum Mun…", **labelled an illustrative reconstruction** | Remotion | Walker opening |
| B01 | Hesitant writer | what A3 added; single-word correction ("downloaded" → "hand-built") | Remotion | summary |
| B02 | Result | the A2 slice: the flat SUV card and the painted shrine and fence (why the game needs real models) | real engine capture of `slice.tscn` | game + why each asset |
| B03 | Code | `godot/tests/data/a3_brief.json` (sizes, budgets, colours) | verbatim excerpt | brief in numbers |
| B04 | Result | showcase with the brief-sized placeholders beside Hari's 1.75 m billboard | real engine render | |
| B05 | **Shriram's footage** | the prompt to Claude and the MCP building the SUV in Blender, **labelled "Shriram's screen recording"** | Shriram's own recording | real Blender session + a prompt and what it built |
| B06 | Code | `tools/blender/build_suv.py` (one `execute_blender_code` body) | verbatim excerpt | code Claude ran |
| B07 | Result | the SUV in Blender, then in Godot | Shriram's recording / engine render | |
| B08 | **Shriram's footage** | the hand edit by mouse | Shriram's own recording | hand edit |
| B09 | Code | `tests/a3_measure.gd`: floor height from mesh vertices, not a collider | verbatim excerpt | what the check does |
| B10 | Result | headless check output beside the brief, **labelled "headless"** | recorded terminal output | numbers vs brief |
| B11 | Code | `tests/check_a3_selftest.gd`: the broken stand-ins | verbatim excerpt | what a check can and cannot prove |
| B12 | Result | self-test 17/17, each failure caught | recorded terminal output | |
| B13 | Result | the three assets in the running scene, orbit including behind and below | Movie Maker capture of `a3_showcase.tscn` | assets in the running Godot scene |
| B14 | Revision | what Claude got wrong, and the inspect-and-revise cycle | evidence from the build | revision + limitation |
| B15 | Credits | human vs AI; source revision shown | Remotion | contributions + revision |
| B16–B18 | Verdict → Your Turn → regular outro | checked / uncertain / one next step | Remotion | required ending |

**Still needed from Shriram:** one screen recording of the build session (Cmd+Shift+5, whole screen), covering at least one prompt with its result and the hand edit. The skill cannot take footage itself; nothing is reconstructed in its place.
