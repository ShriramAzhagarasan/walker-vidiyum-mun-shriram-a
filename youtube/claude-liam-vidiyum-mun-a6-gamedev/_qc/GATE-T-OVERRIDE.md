# GATE T override: APPLIED (GATE T only)

**Approval.** Shriram, 2026-11-08 ~21:05, relayed verbatim by the coordinator (this session did not see the message
directly): "i approve the text check override, and yes fix one line in beat 12"

**Scope.** GATE T (`type_check.py`) only. `./art final` runs `type_check.py` and then `compile.py`. This override skips
only the GATE T stop and runs the same `compile.py` command directly. Every gate inside compile.py (beat_lint, gate_shape,
approvals, Gate V / final_frame_check) still runs. If any of them fails, nothing is overridden.

**Re-check after the B12 narration fix (~21:10).** `type_check.py` was run again: the same 7 FAIL beats (B06, B08, B10,
B12, B14, B18, B24). The flagged blobs are in the same captured pixels (`_qc/gate-t/gt_*.png`; B12 is the window chairs and
wall in Shriram's preview screenshot). Nothing new was flagged. The validator was not edited.

| Beat | Flag(s) | What the flagged pixels are |
|---|---|---|
| B06 | min-size 35 px; contrast-local 1.02:1; bbox-overlap | pool, window chairs and the two scuff puffs in Shriram's play screenshot `evidence/a6/effect-a-play/r1-walking-by-pool.png` |
| B08 | min-size 39 px (no location given) | fixture strip r0/r1 (`evidence/strip_a_r0_r1.png`): toes / flip-flops / dust in the real frames; the film's captions were enlarged to 80 px mono and the result did not change, so the small run is in the frames |
| B10 | min-size 36 px (no location given) | fixture strip r1/r2, same as B08 |
| B12 | min-size 36 px; contrast-local 1.88:1; bbox-overlap | window chairs and wall in Shriram's preview screenshot `effect-b-r0-first-look/1-preview-live.png` |
| B14 | min-size 35 px; contrast-local 1.03:1; bbox-overlap | pool and deck in Shriram's live screenshot `effect-b-r0-first-look/3-r1-live-shriram.png` |
| B18 | min-size 39 px; contrast-local 1.64:1 | window chairs in the fixture Movie Maker capture `capture/moths_r3_preview.avi` |
| B24 | contrast-local 2.90:1 | the game view inside Shriram's Visual Profiler screenshot `use-it/visual-profiler-B-heaviest.png` |

The suggested fixes (larger font, INK on cream, backing plate) cannot apply to captured pixels without altering the evidence.
All 23 other beats PASS. Precedent: A5 (`../claude-liam-vidiyum-mun-a5-gamedev/_qc/GATE-T-OVERRIDE.md`).

**Command run** (from `$B`):
`python3 runtime/scripts/compile.py $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`
