# SOURCES

Source revision shown on screen: **git `81c1666`** (`git -C $R rev-parse --short HEAD` at 2026-10-15 21:02 EDT, when the headless checks were run; `evidence/source-revision.txt`). godot/ content snapshot (tools/source_snapshot.py): `86c31cd9…` (full id in beat_sheet.json metadata). Tools: Godot 4.7.2.stable.official.ed1daf0bf (headless), Blender 5.2.2 LTS, mcp-for-blender 2.1.9, macOS.

## Shriram's screen recording (real Blender session; never reconstructed)
`~/Desktop/blendersession.mov` (52:50, 3456×2234 h264, 2,776,980,562 bytes; Shriram's own Cmd+Shift+5 recording; **not copied into git**). Recording start ≈ 19:46 EDT (given as 19:46:13; the in-frame clock reads 7:52 PM at offset 352 s and 7:53 PM at 382 s, so the times below are read from the macOS menu-bar clock in the frames, not computed). Only short clips were cut into `clips/` (gitignored):

| Clip | Beat | Recording offset | Wall clock (EDT, read from the frames) | Speed | Crop | SHA-256 |
|---|---|---|---|---|---|---|
| `clips/B02-0.mp4` | B02 the chat: plan, "approved", Claude's reply | 352–382 s | 7:52–7:53 PM (menu-bar clock) | 2× (labelled) | x 600–1900 (chat) | `cf02b1d6…` |
| `clips/B04-0.mp4` | B04 SUV build 1 appearing part by part | 113–173 s | 7:48–7:49 PM (menu-bar clock) | 4× (labelled) | none | `5e80ebb4…` |
| `clips/B05-0.mp4` | B05 Shriram's hand edit (duplicate ×2, delete, move, X 0 / Y −0.03) | 2696–3016 s | 8:31–8:36 PM (menu-bar clock) | 16× (labelled) | none | `8f2d22a6…` |

Every clip is labelled on screen "SHRIRAM'S SCREEN RECORDING" with its time and speed. Frames were extracted and viewed before use (see FACTCHECK.md). The wall-clock column is the macOS menu-bar clock read in the frames.

## Godot engine evidence (real)
- Headless stdout, run this session on `$R/godot` at git 81c1666: `evidence/check_a3_assets.out.txt` (`eaf67212…`, 31 checks, 0 failed, exit 0), `evidence/check_a3_selftest.out.txt` (`f8bc43ae…`, 17 checks, 0 failed, exit 0); the check's JSON receipt `evidence/check-a3-1792112569.json`. Rendered verbatim (excerpt rows, long lines truncated with "…") to `evidence/check_a3_assets.png` (`5f848ad4…`) and `evidence/check_a3_selftest.png` (`6837f989…`) by `tools/make_media.py`, labelled HEADLESS.
- Engine screenshots of `scenes/a3_showcase.tscn` (taken by `godot/tests/capture_a3.gd` before this film; used as-is, labelled): `$R/evidence/a3/godot-suv-front.png` (`e20819e0…`), `godot-suv-rear.png` (`fb6019ca…`), `godot-suv-below.png` (`1b3a3844…`), `godot-fence-side.png` (`97ae71cf…`), `godot-shrine-front.png` (`cc18b3ff…`), `godot-shrine-front-BEFORE-facing-suv.png` (`9f79e183…`). No Movie Maker motion capture was made (time); the orbit is shown as labelled screenshots, not motion.

## Code shown (verbatim, path + lines)
- `tools/blender/build_suv.py` 53–62 (B03; outside godot/, so shown in a GodotDesignBoard excerpt panel, not a hash-certified excerpt).
- `godot/tests/a3_measure.gd` 29–41 (B06), `godot/tests/check_a3_selftest.gd` 64–78 (B08), `godot/scenes/a3_showcase.gd` 13–16 (B10): certified by `./art godot-gamedev --check` (gamedev-evidence.json).

## Who did what
Shriram: chose the three assets; judged every build; drove all revisions (SUV builds 2–4, the goddess relief and front lamp, the wooden fence); did the hand edit and the look check; recorded the session. Claude: the brief's numbers, all Blender code (execute_blender_code bodies), the .glb export, the Godot check, self-test and showcase scene, and this film. Narration: local Kokoro `am_onyx` (Liam, in for Bear). No paid calls, no imported or generated 3D assets, no licences involved.
