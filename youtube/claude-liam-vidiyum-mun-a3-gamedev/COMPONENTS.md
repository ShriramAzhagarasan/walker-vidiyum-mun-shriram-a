# COMPONENTS: what this film explains (godot/ at git 81c1666)

| Component | Files (godot/) | Beats | Mechanism shown | Trade-off |
|---|---|---|---|---|
| a3-models | `assets/models/{suv,rock_shrine,fence_segment}.glb` + `.import` | B02–B05, B07, B11 | Built in Blender 5.2.2 by `execute_blender_code` bodies Claude ran through the Blender MCP (`tools/blender/build_*.py`, outside godot/; one body shown verbatim in B03), exported glTF +Y Up | 6 basic shapes and flat colours read as silhouettes; details are faces, not geometry |
| a3-check | `tests/a3_measure.gd`, `tests/check_a3_assets.gd`, `tests/check_a3_selftest.gd`, `tests/data/a3_brief.json`, `tests/capture_a3.gd` | B06–B09 | Every mesh vertex in world space → bounds, floor (lowest vertex), triangles, shapes, scales, colours, compared with the brief; self-test breaks stand-ins on purpose | Proves size/scale/orientation/budget, not that a model looks right or reads at night |
| a3-showcase | `scenes/a3_showcase.gd`, `scenes/a3_showcase.tscn` | B10–B11 | Three slots at game scale beside Hari's 1.75 m billboard; shrine slot yaw −90° (found by a screenshot); lamp flicker as an OmniLight3D; orbit camera | The slot turns, not the asset, so the asset stays identity for the check; showcase only, not yet in slice.tscn |

The rest of godot/ (the A2 slice: runtime, art, audio, UI, A2 tests) is listed in `gamedev-evidence.json` as exclusions with a reason: unchanged by A3 and explained in the A2 film.

Input → state → output trace: Shriram's "approved" (B02) → Claude's call 1 body (B03) → SUV_Chassis in Blender (B04) → exported `suv.glb` → `a3_measure.gd` vertex loop (B06) → "456 triangles, lowest vertex +0.0000" (B07).
