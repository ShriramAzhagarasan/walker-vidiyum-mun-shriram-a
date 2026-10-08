# GATE T override — documented, not silent

`./art final` ran `type_check.py` (GATE T) first and reported 9 FAIL beats (`TYPECHECK.md`, 2026-10-07 17:12, and again identically at 18:00 on the 13f772c build).
Every flagged blob lies inside **real engine footage or a reproduced asset image**, not in film typography:

| Beat | Flag | Where the blob is (4K px) | What it actually is |
|---|---|---|---|
| B02 | contrast-local 1.91:1 | (937,1279)–(1012,1324) | Intro motion comic still (generated art, game footage) |
| B03 B09 B11 B15 B16 | min-size 35–36 px; contrast-local; bbox-overlap | inside the reframed game frame (x 288–3552, y 116–1952) | The game's own 1280×720 HUD/dialogue text scaled ×3 ×0.85 ("loop 1", "E / Space >", gloss lines) and scene art; the "overlaps" are whole game frames fused into one blob |
| B06 | contrast-local 1.26:1 | (1122,712)–(1187,742) | Skin/hair pixels of the raw s301/s302 generations |
| B07 | contrast-local 2.23:1; bbox-overlap 13 % | (1746,787)–(1804,820); (1789,1443)–(1937,1550) | Shirt check of the cut-out phone.png; the board's own small file caption under the image |
| B18 | contrast-local 1.19–1.29:1; bbox-overlap | inside the two enlarged 1:40 AM screenshot tiles | Pixels of the R1 before/after in-engine screenshots |

The suggested fixes ("Use INK on cream; add backing plate", "Increase font_size") do not apply to game art or the
game's HUD; changing them would change the game for the film. The film's own labels (caption band 50 px Lato Bold on
near-black; Remotion cards) were not flagged. The validator was **not** edited.

Decision (Claude, following the A1 precedent `walker-jumpman-shriram-a/…/_qc/GATE-T-OVERRIDE.md`, under the
coordinator's PHASE 2 GO for `BUILD-PROMPT.md` step 11): compile with `runtime/scripts/compile.py` directly, the
exact command `./art final` runs after GATE T. Every other gate still runs (paperwork, beat lint, shape gate,
approvals, no slates, audio presence/duration, full decode, final-frame QC, receipt). Flag for human review.


**Human approval:** Shriram approved this override on 2026-10-07 at ~21:05 EDT ("OK"; recorded in `design/input/SHRIRAM-DECISIONS.md`).
