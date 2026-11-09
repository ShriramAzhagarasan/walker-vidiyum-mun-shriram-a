# TYPECHECK.md — GATE T

Reel: `claude-liam-vidiyum-mun-a6-gamedev`  |  Checked: 2026-11-08T21:12  |  Overall: **FAIL**  |  Beats checked: 30  |  FAILs: 7

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B02 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B04 | ? | dark | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B05 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B06 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B07 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B08 | ? | dark | min-size §8.1: smallest text run 39px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B09 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B10 | ? | dark | min-size §8.1: smallest text run 36px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B11 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B12 | ? | dark | min-size §8.1: smallest text run 36px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B13 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B14 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B15 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B16 | ? | dark | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B17 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B18 | ? | dark | min-size §8.1: smallest text run 39px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B19 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B20 | ? | dark | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B21 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B22 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B23 | ? | dark | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B24 | ? | dark | contrast-local §8.3b: per-blob contrast 2.90:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B25 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B26 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B27 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B28 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B29 | ? | dark | min-size §8.1: min text-run height 44px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### B06 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.02:1 < 3.0:1 — text unreadable on actual local background (blob@(1742,1242)–(1835,1275) fg≈(155, 126, 115) bg≈(155, 124, 112)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(1146,116)–(2135,477) ∩ blob@(2026,131)–(2095,167) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(1146,116)–(2135,477) h=361px (7.8×med), blob@(2297,348)–(2691,477) h=129px (2.8×med), blob@(1146,772)–(2119,1275) h=503px (10.9×med), blob@(1354,1596)–(1528,1711) h=115px (2.5×med), blob@(1998,1615)–(2184,1708) h=93px (2.0×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B08 (?)
- **min-size §8.1**: smallest text run 39px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B10 (?)
- **min-size §8.1**: smallest text run 36px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B12 (?)
- **min-size §8.1**: smallest text run 36px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.88:1 < 3.0:1 — text unreadable on actual local background (blob@(1097,1156)–(1157,1192) fg≈(215, 149, 82) bg≈(173, 94, 54)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(391,646)–(3460,1372) ∩ blob@(1425,1155)–(1509,1192) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(391,646)–(3460,1372) h=726px (11.5×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B14 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.03:1 < 3.0:1 — text unreadable on actual local background (blob@(789,1500)–(895,1529) fg≈(187, 128, 78) bg≈(184, 126, 76)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(1915,1050)–(3432,1675) ∩ blob@(3048,1500)–(3137,1535) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(1944,924)–(2386,1010) h=86px (2.1×med), blob@(1915,1050)–(3432,1675) h=625px (15.2×med), blob@(359,1195)–(1838,1564) h=369px (9.0×med)
- **Fix:** Increase font_size in scenes.py or Remotion component

### B18 (?)
- **min-size §8.1**: smallest text run 39px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.64:1 < 3.0:1 — text unreadable on actual local background (blob@(1220,1098)–(1272,1127) fg≈(212, 119, 73) bg≈(166, 86, 43)); move label off its background or change text color
- **Fix:** Increase font_size in scenes.py or Remotion component

### B24 (?)
- **contrast-local §8.3b**: per-blob contrast 2.90:1 < 3.0:1 — text unreadable on actual local background (blob@(2024,1138)–(2613,1456) fg≈(171, 176, 150) bg≈(114, 89, 73)); move label off its background or change text color
- **Fix:** Use INK on cream; add backing plate under accent text

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 14 | 0 |
| min-size §8.1 | 30 | 6 |
| overflow §8.2 | 30 | 0 |
| contrast §8.3 | 30 | 0 |
| contrast-local §8.3b | 30 | 5 |
| bbox-overlap §8.6b | 30 | 3 |
| card-clip §8.13 | 30 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 1 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
