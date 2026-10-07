# TYPECHECK.md — GATE T

Reel: `claude-liam-walker-vidiyum-mun-shriram-a-gamedev`  |  Checked: 2026-10-07T18:03  |  Overall: **FAIL**  |  Beats checked: 24  |  FAILs: 9

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B02 | ? | dark | contrast-local §8.3b: per-blob contrast 1.91:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B03 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B04 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | ? | light | contrast-local §8.3b: per-blob contrast 1.26:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B07 | ? | light | contrast-local §8.3b: per-blob contrast 2.23:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B08 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B09 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B10 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B11 | ? | dark | min-size §8.1: smallest text run 36px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B12 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B13 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B14 | ? | dark | min-size §8.1: min text-run height 80px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B15 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B16 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B17 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B18 | ? | light | contrast-local §8.3b: per-blob contrast 1.29:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B19 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B20 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B22 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B23 | ? | dark | min-size §8.1: min text-run height 44px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### B02 (?)
- **contrast-local §8.3b**: per-blob contrast 1.91:1 < 3.0:1 — text unreadable on actual local background (blob@(937,1279)–(1012,1324) fg≈(210, 153, 65) bg≈(155, 103, 52)); move label off its background or change text color
- **Fix:** Use INK on cream; add backing plate under accent text

### B03 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.70:1 < 3.0:1 — text unreadable on actual local background (blob@(1917,1524)–(1987,1554) fg≈(195, 141, 98) bg≈(133, 107, 102)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(1326,116)–(1462,171) ∩ blob@(943,116)–(3551,1020) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(943,116)–(3551,1020) h=904px (19.9×med), blob@(438,973)–(3551,1951) h=978px (21.5×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B06 (?)
- **contrast-local §8.3b**: per-blob contrast 1.26:1 < 3.0:1 — text unreadable on actual local background (blob@(1122,712)–(1187,742) fg≈(116, 84, 65) bg≈(135, 98, 77)); move label off its background or change text color
- **Fix:** Use INK on cream; add backing plate under accent text

### B07 (?)
- **contrast-local §8.3b**: per-blob contrast 2.23:1 < 3.0:1 — text unreadable on actual local background (blob@(1746,787)–(1804,820) fg≈(85, 52, 53) bg≈(142, 104, 96)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 13% >= 10% — two labels are printing on top of each other: blob@(1793,1443)–(1854,1482) ∩ blob@(1789,1477)–(1937,1550) (13% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(211,292)–(911,401) h=109px (1.8×med)
- **Fix:** Use INK on cream; add backing plate under accent text

### B09 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.14:1 < 3.0:1 — text unreadable on actual local background (blob@(3413,1721)–(3534,1796) fg≈(149, 113, 139) bg≈(139, 104, 130)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(288,116)–(2822,938) ∩ blob@(769,174)–(856,217) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(288,116)–(2822,938) h=822px (19.6×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B11 (?)
- **min-size §8.1**: smallest text run 36px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.84:1 < 3.0:1 — text unreadable on actual local background (blob@(2439,731)–(2500,768) fg≈(228, 147, 67) bg≈(187, 91, 42)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(1947,116)–(2065,174) ∩ blob@(1611,116)–(3551,963) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(1611,116)–(3551,963) h=847px (18.4×med), blob@(3403,869)–(3551,966) h=97px (2.1×med), blob@(1306,1177)–(3551,1951) h=774px (16.8×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B15 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.79:1 < 3.0:1 — text unreadable on actual local background (blob@(2458,732)–(2518,769) fg≈(227, 147, 74) bg≈(188, 93, 54)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(1953,116)–(2090,177) ∩ blob@(1634,116)–(3551,1260) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(1634,116)–(3551,1260) h=1144px (26.0×med), blob@(439,1172)–(3551,1951) h=779px (17.7×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B16 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.00:1 < 3.0:1 — text unreadable on actual local background (blob@(394,1839)–(614,1924) fg≈(168, 121, 110) bg≈(167, 121, 111)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(288,116)–(3062,944) ∩ blob@(769,174)–(856,217) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(288,116)–(3062,944) h=828px (8.1×med), blob@(288,1110)–(2119,1800) h=690px (6.8×med), blob@(2076,1159)–(3551,1747) h=588px (5.8×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B18 (?)
- **contrast-local §8.3b**: per-blob contrast 1.29:1 < 3.0:1 — text unreadable on actual local background (blob@(1131,930)–(1232,960) fg≈(50, 65, 87) bg≈(57, 82, 113)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(498,628)–(1901,1509) ∩ blob@(1528,637)–(1675,716) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(498,628)–(1901,1509) h=881px (11.2×med), blob@(2166,628)–(3569,1543) h=915px (11.6×med)
- **Fix:** Use INK on cream; add backing plate under accent text

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 12 | 0 |
| min-size §8.1 | 24 | 5 |
| overflow §8.2 | 24 | 0 |
| contrast §8.3 | 24 | 0 |
| contrast-local §8.3b | 24 | 9 |
| bbox-overlap §8.6b | 24 | 7 |
| card-clip §8.13 | 24 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 1 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
