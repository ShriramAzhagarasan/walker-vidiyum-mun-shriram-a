# Final QC: claude-liam-vidiyum-mun-a3-gamedev ("Vidiyum Mun, Built from Boxes")

- Export: `exports/landscape/claude-liam-vidiyum-mun-a3-gamedev.mp4`, 3840×2160 H.264, 30 fps, AAC 48 kHz, **260.87 s** (4:21), SHA-256 `40e99c7d4e55ecb2b7e004f608e3c55bd43010fd8776b86c66e2f8ed66b3a91e` (matches `.verified.json`, status `ready`). Finished 2026-10-15 21:39 EDT.
- Source revision shown on screen (B07, B09, B10, B13, B14 and code footers): git `81c1666`, recorded at 21:02 EDT when the checks were run.
- `./art godot-gamedev --check`: **PASS** (13 source files, 110 exclusions with reasons, 3 components, 3 exact excerpts, 3 code→result pairs; `_qc/gamedev-check-final.txt`).
- GATE T (typecheck): PASS. Gate V (`_qc/REPORT.md`, written by `./art final`): 34 frames, BLOCKER 0, MAJOR 0.
- Headless (real stdout in `evidence/`): check_a3_assets.gd 31 checks, 0 failed; check_a3_selftest.gd 17 checks, 0 failed.

## Frames read (`_qc/contact-1..3.jpg`, 15/50/85 % of every beat, final export)
- B00 composer labelled ILLUSTRATIVE RECONSTRUCTION; result lines land. B01 "downloaded" → "built" correction lands; lines 2–3 type.
- B02 Shriram's recording, chat crop: "approved" bubble and Claude's reply legible at 4K. The first ~4 s of the clip are still the Blender viewport (cropped) before the chat comes to the front; labelled throughout.
- B03 build_suv.py 53–62 verbatim, cards light in order. B04 empty scene → chassis → cabin/wheels at 4×, then the Godot SUV screenshot with its own label.
- B05 hand edit at 16×: three signs, copies gone, sign centred, Item tab; last 1.8 s labelled HELD FRAME.
- B06/B08/B10 Workbench code readable, line highlights move, "Godot editor reconstruction" labelled. B07/B09 terminal text readable; long rows truncated with "…".
- B11 BEFORE (goddess facing the SUV tail, a dark close-up) → AFTER → SUV rear → SUV below → fence side, each labelled engine screenshot.
- B12/B13 boards legible; B13 shows git 81c1666. B14 verdict, B15 Your Turn, B16 locked outro (exact title, @NikBearBrown, mascot, no subline).

## Audio
Whole film mean −27.3 dB, peak −3.6 dB (narration only; no music, no game audio). Last 1 s of the outro: −91 dB max (silent tail).

## Known issues (not fixed, for a human to judge)
1. `GodotDesignBoard` (B03, B12, B13) prints a fixed "GDD · DOCUMENT EXCERPT" label above its excerpt panel; for B03 the panel is actually Blender code. The component is shared toolkit code outside this reel, so it was not edited; the panel's own heading names the real file and lines.
2. The orbit (B11) is shown as labelled engine screenshots, not Movie Maker motion (no motion capture was made, for time).
3. B03 excerpt (build_suv.py) is outside godot/, so `verify_gamedev.py` does not hash-certify it; it was copied verbatim by `tools/author_sheet.py` (anchor = first `root = bpy.data.objects["suv"]`, lines 53–62).
4. The first cut mislabelled B02 as 7:51–7:52 PM; the in-frame clock reads 7:52–7:53 PM; fixed and re-exported (first cut kept as `_qc/first-cut.mp4`).
5. B04's build timing differs from the brief given to the film (~19:49–19:53): the frames show build 1 appearing at 7:48–7:49 PM; the film uses the frame-verified time.

## Repository incident (disclosed)
Before the headless checks ran, `$R/TEST-REPORT.md` already had uncommitted edits (git status showed ` M TEST-REPORT.md` before Godot started). I briefly restored it to HEAD, believing the edit was a side effect of the check, then re-applied the exact saved diff (`_qc/check-side-effect-TEST-REPORT.diff`) seconds later with `git apply`. `git status` afterwards shows the same ` M TEST-REPORT.md`; content is identical to before. The check itself wrote `evidence/a3/check-a3-1792112569.json` into the repo; it was moved into this reel's `evidence/`. Nothing in `$R/godot` or git history was changed; no commit, no push, no publish.

## Revision note
While the film was being built, a new commit landed: HEAD is now `77cf8b8` ("A3 docs: results, revisions, look check, hand edit, what Claude got wrong"). It changes only BLENDER-NOTES.md, FRICTIONAL.md and SOURCES.md at the repo root; `godot/` and `tools/blender/` are identical to `81c1666`, so the code, checks and evidence shown are unchanged (`./art godot-gamedev --check` re-run at 21:40 against the current godot/ passed). The film shows `81c1666`, the revision the checks were run on. `$R/TEST-REPORT.md` still has its uncommitted edits.
