# GATE T override: REQUESTED, NOT APPLIED (needs Shriram's approval)

`type_check.py` (GATE T, run by `./art final` before `compile.py`) reports **7 FAIL beats**: B06, B08, B10, B12, B14,
B18, B24 (`TYPECHECK.md`, `_qc/typecheck.log`). No final export was written; the validator was not edited; no override was
applied by this session.

Every flagged blob is inside a **real engine capture or a screenshot**, on the mid-beat frame that type_check samples
(boxes drawn in magenta: `_qc/gate-t/gt_<beat>.png`, overview `_qc/gate-t/overview.png`):

| Beat | Flag(s) | What the flagged pixels are |
|---|---|---|
| B06 | min-size 35 px; contrast-local 1.02:1; bbox-overlap | pool, window chairs and the two scuff puffs in Shriram's play screenshot `evidence/a6/effect-a-play/r1-walking-by-pool.png` |
| B08 | min-size 39 px (no location given) | fixture strip r0/r1 (`evidence/strip_a_r0_r1.png`): toes / flip-flops / dust in the real frames; the film's captions were enlarged to 80 px mono and the result did not change, so the small run is in the frames |
| B10 | min-size 36 px (no location given) | fixture strip r1/r2, same as B08 |
| B12 | min-size 36 px; contrast-local 1.88:1; bbox-overlap | window chairs and wall in Shriram's preview screenshot `effect-b-r0-first-look/1-preview-live.png` |
| B14 | min-size 35 px; contrast-local 1.03:1; bbox-overlap | pool and deck in Shriram's live screenshot `effect-b-r0-first-look/3-r1-live-shriram.png` |
| B18 | min-size 39 px; contrast-local 1.64:1 | window chairs in the fixture Movie Maker capture `capture/moths_r3_preview.avi` |
| B24 | contrast-local 2.90:1 | the game view inside Shriram's Visual Profiler screenshot `use-it/visual-profiler-B-heaviest.png` |

The fixes the checker suggests (larger font, INK on cream, backing plate) cannot apply to captured pixels without
altering the evidence. All 23 other beats PASS, including every film-made label, strip caption and log still.

Precedent: the A5 film (`../claude-liam-vidiyum-mun-a5-gamedev/_qc/GATE-T-OVERRIDE.md`), same kind of flags on captured
pixels, approved by Shriram, compiled with the exact command `./art final` runs after GATE T.

**If Shriram approves**, the command (from `$B`, every other gate in compile.py still runs, including Gate V):
```
python3 runtime/scripts/compile.py $REEL --height 2160 --fps 30 --out $REEL/exports/landscape
```
