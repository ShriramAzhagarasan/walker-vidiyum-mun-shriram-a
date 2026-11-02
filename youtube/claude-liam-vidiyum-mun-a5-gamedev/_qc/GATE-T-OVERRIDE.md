# GATE T override: APPLIED

**Approved by Shriram 2026-11-01 (~18:15) ("approve override") and the coordinator; compiled with compile.py directly, which is what ./art final runs after GATE T.** The coordinator checked `_qc/gate-t/gt_B04.png`, `gt_B06.png` and `gt_B12.png`: every box is on captured game or editor pixels, not film captions.

`./art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape` (2026-11-01 ~17:57) ran `type_check.py`
first and stopped: `TYPECHECK.md` reports 3 FAIL beats. No export was written. The validator was **not** edited.

Every flagged blob lies **inside a real engine capture or Shriram's own screenshot**, not in the film's typography
(boxes drawn on the mid-beat frame, which is the frame type_check samples: `_qc/gate-t/gt_B04.png`, `gt_B06.png`, `gt_B12.png`):

| Beat | Flag | Blob (4K px) | What it actually is |
|---|---|---|---|
| B04 | contrast-local 1.70:1; bbox-overlap 60 % | (2611,832)–(2671,862); (1652,201)–(2430,593) ∩ (1340,240)–(2115,521) | bougainvillea petals in the scripted capture `glow_skip_2_0.png`; the orange status bar at skip_amount 2.0 (the hint_range evidence itself) |
| B06 | min-size 38 px; contrast-local 1.82:1 | (1188,751)–(1243,785) | chairs behind the villa window in Shriram's playtest screenshot `checkC_playtest_T_held_x8.png` |
| B12 | contrast-local 2.03:1; bbox-overlap 79 % | (1795,933)–(1883,975) ∩ (1470,942)–(2095,1169) | the editor's light gizmo over the pool in Shriram's screenshot `checkB_wet_tint_red_only_back_strip.png` |

The suggested fixes ("Use INK on cream; add backing plate", "Increase font_size") cannot apply to captured pixels
without altering the evidence. The film's own labels (caption band, Remotion cards) were not flagged; all 20 other beats PASS.
These failures predate this session's changes: B04, B06 and B12 have the same inputs and labels as before, and
`./art final` had not been run on this reel before (no `exports/` existed).

Precedent: `youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/_qc/GATE-T-OVERRIDE.md` (A2): compile with
`runtime/scripts/compile.py` directly, the exact command `./art final` runs after GATE T; every other gate still runs.
That override had the coordinator's GO and Shriram's approval; so does this one (above).

Command run (from $B):
`python3 runtime/scripts/compile.py $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`

## Re-render 2026-11-01 ~20:30 (authorship wording fix: B00/B01 "hand-written" removed; B15 excerpt layout)
`type_check.py` was run again before compiling: FAILs only on the same three evidence beats (B04, B06, B12). Nothing new
was flagged, so this re-render reused the override approved above (Shriram + coordinator) and compiled with `compile.py`
directly. The previous export is kept in `exports/landscape/superseded/` (sha256 613d4ed5…).
