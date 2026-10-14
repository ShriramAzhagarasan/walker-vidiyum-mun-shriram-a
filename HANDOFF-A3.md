# HANDOFF — Assignment 3 build session (read this first)

You are a new Claude Code session opened in `walker-vidiyum-mun-shriram-a` so that the **Blender MCP**
(`mcp-for-blender 2.1.9`, registered for this project with `DISABLE_TELEMETRY=true`) is loaded.
Due: **Thu 2026-10-15 23:59**. Shriram approves every build step and judges the looks.

## Already done (previous session)
- Blender 5.2.2 LTS, GNU coreutils `timeout`, `uv 0.12.21` installed. MCP registered; add-on installed to
  `~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py`. Exact setup log, including two
  real failures and their fixes: `evidence/a3/mcp-setup-log.txt`.
- **A3 brief:** `CHANGE-BRIEF.md` (section "Change brief: Assignment 3"), plus its data copy
  `godot/tests/data/a3_brief.json`. It must be **committed before anything is built** (check `git log`).
- Assets: `suv` (4.60 × 1.90 × 1.85 m, ≤250 tris), `rock_shrine` (1.20 × 1.00 × 1.50 m, ≤200),
  `fence_segment` (2.40 × 0.12 × 2.10 m, ≤100). Blender axes X × Y × Z (Z up). Front faces +X.
  Base on the floor at the world origin; origin at the centre of the underside.

## Rules (from the assignment; do not bend them)
- **One asset per request.** First call `get_scene_info`, report, and propose steps; **do not build until Shriram approves.**
- One `execute_blender_code` call per object. After each, call `get_scene_info` (location, size, rotation, scale) and report.
  Apply rotation and scale. Show the result with `look`.
- **Never** use Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D or Tripo, and never call `generate_3d`,
  `search_assets` or `import_asset`. Downloaded or AI-generated meshes do not count.
- Low segment counts (12-segment cylinders, an icosphere at subdivisions 1, an 8-segment cone). ≤ 6 shapes per asset.
- **Save every `execute_blender_code` body verbatim** to `tools/blender/build_<asset>.py` (append in order, with a comment per call).
- Save each asset's `.blend` to `blender/<asset>.blend` (never commit `.blend1`).
- Export with Blender's glTF exporter (binary `.glb`, **+Y Up on**, apply modifiers) to `godot/assets/models/<asset>.glb`.
  Save the export code into the same build script.
- Say what you could not verify. Claude cannot judge whether it looks right; Shriram does.

## Prompt to use per asset (adapt the name)
> We are using Walker's Game brief → Build → Playtest → Inspect → Revise → Export workflow. Use the Blender MCP
> tools in my open Blender session. Read CHANGE-BRIEF.md (A3 section) and HANDOFF-A3.md first.
> Task: build only this asset: **suv**, exactly as the brief specifies (size in metres, origin, materials,
> triangle budget). Start from an empty scene with metric units; Blender is Z-up.
> First call get_scene_info and tell me what is in the scene, then propose the steps. Do not build yet.
> After I approve: one execute_blender_code call per object… (rest as in the assignment). Do not export yet.

## Order of work
1. Commit the brief, `BLENDER-NOTES.md` and the screenshot (if not already), then push.
2. Build `suv` → `rock_shrine` → `fence_segment` (approve, build, look, Shriram's viewport check).
3. **Shriram's hand edit** (by mouse, in Blender) on at least one asset. Record what changed and what Shriram says it taught them.
4. Export the three `.glb` files, then `godot --headless --path godot --import`.
5. `godot/scenes/a3_showcase.tscn`: floor, one light, a camera, the three assets side by side, and a 1.70 m Hari-size
   reference capsule (label it a reference).
6. `godot/tests/check_a3_assets.gd`: for each asset, the mesh AABB size vs `a3_brief.json` (±5 %), node scale (1,1,1),
   tallest axis = Y, **lowest mesh point y = 0 ± 0.01 m measured from mesh vertices (not a collider)**, triangle and
   surface counts vs budget, albedo vs hex, SUV cabin centre x < 0. Print a table, exit nonzero on failure.
   Run: `timeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/check_a3_assets.gd --fixed-fps 60`
7. TEST-REPORT (A3 section), SOURCES, README, FRICTIONAL (AI-recorded entries labelled; Shriram writes their own).
8. Film: Brutalist `godot-gamedev` **walker** mode (`../brutalist.art/skills/make/godot-gamedev/SKILL.md`), reusing
   Shriram's own Blender screen recording. Then tag `a3`, push the tag, fresh clone of the tag, ZIP, Canvas note.
