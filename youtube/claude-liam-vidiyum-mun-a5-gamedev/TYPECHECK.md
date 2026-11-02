# TYPECHECK.md — GATE T

Reel: `claude-liam-vidiyum-mun-a5-gamedev`  |  Checked: 2026-11-01T17:57  |  Overall: **FAIL**  |  Beats checked: 23  |  FAILs: 3

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B02 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B04 | ? | dark | contrast-local §8.3b: per-blob contrast 1.70:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B05 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B06 | ? | dark | min-size §8.1: smallest text run 38px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B07 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B08 | ? | dark | min-size §8.1: min text-run height 45px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B09 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B10 | ? | dark | min-size §8.1: min text-run height 143px >= floor 41px | PASS | — |
| B11 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B12 | ? | dark | contrast-local §8.3b: per-blob contrast 2.03:1 < 3.0:1 — text unreadable on actual local b… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B13 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B14 | ? | dark | min-size §8.1: min text-run height 874px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B15 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B17 | ? | dark | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B18 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B19 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B20 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B21 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B22 | ? | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### B04 (?)
- **contrast-local §8.3b**: per-blob contrast 1.70:1 < 3.0:1 — text unreadable on actual local background (blob@(2611,832)–(2671,862) fg≈(227, 70, 103) bg≈(163, 51, 75)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 60% >= 10% — two labels are printing on top of each other: blob@(1652,201)–(2430,593) ∩ blob@(1340,240)–(2115,521) (60% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(385,163)–(1387,456) h=293px (2.0×med), blob@(1652,201)–(2430,593) h=392px (2.7×med), blob@(1340,240)–(2115,521) h=281px (1.9×med)
- **Fix:** Use INK on cream; add backing plate under accent text

### B06 (?)
- **min-size §8.1**: smallest text run 38px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.82:1 < 3.0:1 — text unreadable on actual local background (blob@(1188,751)–(1243,785) fg≈(214, 149, 82) bg≈(173, 97, 58)); move label off its background or change text color
- **Fix:** Increase font_size in scenes.py or Remotion component

### B12 (?)
- **contrast-local §8.3b**: per-blob contrast 2.03:1 < 3.0:1 — text unreadable on actual local background (blob@(1795,933)–(1883,975) fg≈(95, 138, 181) bg≈(54, 89, 118)); move label off its background or change text color
- **bbox-overlap §8.6b**: text-run bbox overlap 79% >= 10% — two labels are printing on top of each other: blob@(1795,933)–(1883,975) ∩ blob@(1470,942)–(2095,1169) (79% of smaller); separate label positions in scenes.py or Remotion component
- **Fix:** Use INK on cream; add backing plate under accent text

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 11 | 0 |
| min-size §8.1 | 23 | 1 |
| overflow §8.2 | 23 | 0 |
| contrast §8.3 | 23 | 0 |
| contrast-local §8.3b | 23 | 3 |
| bbox-overlap §8.6b | 23 | 2 |
| card-clip §8.13 | 23 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 1 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
