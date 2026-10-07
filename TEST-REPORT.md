# Test report: Vidiyum Mun asset slice

- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf · **OS:** macOS 26.6.2 (MacBook Pro M1 Pro, 16 GB) · **Renderer:** Forward+ (Metal)
- **Source revision tested:** *(final SHA filled in at freeze)*. Work-in-progress results below are labelled with the revision they ran on.
- **Labels:** **[AUTO]** = scripted or automated, run by Claude. **[HUMAN]** = played or listened to by Shriram, in his words.

## 1. Startup and controls
| Check | Result |
|---|---|
| [AUTO] Fresh clone → `--import` → tests | *(at freeze)* |
| [HUMAN] Movement, facing, talk, choices, fast-forward, pause, M/N mute, restart work with the intended keys | *(Shriram's playtest)* |

## 2. Automated checks
| Check | Command | Result (rev `443f288`) |
|---|---|---|
| Sound triggers: exact count per event over a scripted two-loop run, including 10 rapid E presses, a held E (40 echo events) and mashing during the crash; the muted run reaches the same outcome | `godot --headless --path godot -s res://tests/test_sound_triggers.gd` | **86 checks, 0 failed.** phone_buzz 2 · clue_saved 3 · keys_exchanged 2 · dawn_crash 1 · safe_dawn 1, identical with both buses muted |
| Loop logic: knowledge persists across the reset, per-loop flags reset, keys-safe prevents the crash, the choice is gated on both clues, all dialogue ids present | `… -s res://tests/test_loop_logic.gd` | **35 checks, 0 failed** |
| 3D scene smoke test: the scene builds with all nodes | `… -s res://tests/test_slice_smoke.gd` | **13 checks, 0 failed** |
| Music loop seams: 3 repetitions, sample step at each seam vs the in-loop 99.9th percentile, RMS change < 6 dB | `python tools/check/loop_seam_check.py` | **PASS.** gaana seam step 0.0094 vs p99.9 0.0926 (0.24 dB); party 0.0401 vs 0.4224 (1.86 dB) |

**What these checks do NOT prove:**
- The sound test counts *requests* to SoundBank, not audible output. It proves logic fires each event once, not that the file sounds right or plays at the right volume.
- The seam check proves there is no sample discontinuity, not that the loop is musically seamless (phrase and groove). That needs human listening.
- The test API jumps the clock (`test_advance_to`). It can't catch timing feel or problems with real-time caption pacing.

## 3. Character against the sheet
- **Evidence:** in-engine scripted captures `evidence/shots/state_<state>_{right,left}.png` (10 states × 2 facings) beside `design/character/poses-spec.png` and the accepted generations.
- *(table filled in after final asset picks)*

## 4. Storyboard against the slice
*(table: panel → in-engine shot → differences. Panel 1 is a design view, not in the slice.)*

## 5. Sound events
*(human: exactly one sound per occurrence, including rapid repeats and a held E)*

## 6. Music
*(human: listened to ≥ 3 repetitions in game; pause muffles; stops at dawn; restarts at 8 PM; stays stopped at the end card)*

## 7. Muted play
*(human: played with M and N both muted; was everything understandable?)*

## 8. Inspect-and-revise cycles
| # | Observation (evidence) | Change | Result |
|---|---|---|---|
| R1 | In-engine screenshots: the night read as lavender dusk, not 1 AM; the white marble washed out (`evidence/revisions/R1-lighting-before.jpg`) | Night ambient `1b1a3c` → `100f26`, moonlight energy 0.25 → 0.08, string lights 1.6 → 2.8 (`scenes/slice.gd`, `scenes/deck_dressing.gd`) | Warm light pools around the string lights; the sky reads as night (`R1-lighting-after.jpg`) |
| R2 | Generated OVERHEAR came back as a hand at the ear: the same silhouette as PHONE (predicted failure F5) | Prompt revised: head turned over the shoulder, hands down, "no phone, hands not near his face" | *(pending)* |
| R3 | Generated WHITEOUT had a sun-flare drawn into the image | Prompt revised: "no light effects, no glow, no lens flare" | *(pending)* |
| R4 | Screenshot p05: Advay hidden behind Manikandan at 1:40 | `ADVAY_AT_CAR` moved beside Manikandan | *(re-capture)* |
| R5 | Capture: the white-out stuck after a fast reset (the crash fade kept running) | `whiteout.gd` kills the running crash tween on reset | Loop-2 shots clean |

## 9. Limitations
*(final list)*
