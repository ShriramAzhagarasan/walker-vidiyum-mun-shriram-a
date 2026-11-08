# Tuning log (Assignment 6)

Every strip under `captures/` is a **fixture capture**: a preview scene (`godot/previews/`) rendered by Godot's Movie
Maker mode at 30 fps on the real renderer (Forward+, Apple M1 Pro), started by Shriram. Claude's reading of a strip is a
claim. Shriram's verdict in the running game, at the project's window size (1280×720), decides.

Each revision records Claude's prediction, the strips before and after, Claude's comparison and Shriram's verdict.

---

## 2026-11-08 — Effect A, revision r1

**Frame numbering.** Movie Maker numbers files from 0, and the preview counts its first `_process` as frame 1, so the
trigger the brief calls "frame 10" is **file `frame00000009.png`**. The strip is read at the trigger and 2, 5, 10, 20
and 40 frames after it: files 9, 11, 14, 19, 29, 49 (said once here, used throughout).

**What I saw** (Shriram, running preview, 1280×720, before reading any frame; screenshots in
`evidence/a6/effect-a-r0-first-look/`): "the size was pretty decent, but i feel the timing was way too fast, and yes i
was able to see it in the dark floor as well, maybe we chould let it be there for a little longer as it was way too
fast"

**Claude's reading of r0** (`captures/footstep_scuff/r0-dark/`, fixture, dark gate, seed 6):
- trig+0 (file 9): a compact cream puff appears at Hari's front foot at full strength on the first frame. It reads
  almost opaque, brighter than "moderate transparency"; the darker FineGrit grains aren't distinguishable from it.
- trig+2, +5: it widens a little (about one foot-length across) and stays at floor level; almost no rise.
- trig+10 (0.33 s): about the same size, starting to break into soft lumps, still dense.
- trig+20 (0.67 s): a faint grey ghost of the puff.
- trig+25 (0.83 s): gone. trig+40: gone.
- Against the intent: the timing matches the brief as written (SoftDust's ramp reaches alpha 0 at 70 % of 1.15 s =
  0.81 s, "mostly disappear by about 0.75 s"), so the strip agrees with the settings. Shriram's "too fast" is a change
  to the intent itself. The rise is lower than A.2's 0.10–0.18 m, as Claude estimated before building (about
  0.06–0.09 m).

**Change:** SoftDust `color_ramp` alpha at 50 % / 70 % of life: 0.18 / 0 → **0.30 / 0.15** (colours, offsets and every
other setting unchanged, so the overlap rule, at most 4 alive, and the 60-particle peak still hold). Proposed by Claude
after Shriram's verdict; **approved by Shriram** ("approve r1"). Claude did not propose `lifetime` 1.15 → 1.6, because
that would change the overlap count to 5, the peak to 75 and the cleanup time.

**Claude's prediction for r1** (same seed, so identical motion; only the fade changes): trig+0, +2, +5 identical to r0;
trig+10 almost identical, a touch denser; trig+20 a clearly visible soft puff, "about twice r0's opacity", where r0 was
a faint ghost; trig+25 still a faint puff where r0 was gone; trig+30 very faint; trig+40 gone. Visible for about 1.1 s
instead of 0.8 s.

**Claude's comparison of r1 with the prediction** (`captures/footstep_scuff/r1-dark/`; mean brightness change in the
scuff patch against the frame before the trigger, 0–255):

| | trig+0 | +2 | +5 | +10 | +15 | +20 | +25 | +30 | +40 |
|---|---|---|---|---|---|---|---|---|---|
| r0 | 70.9 | 73.5 | 76.7 | 74.1 | 64.5 | 47.7 | 2.2 | 1.5 | 1.0 |
| r1 | 70.9 | 73.5 | 76.7 | 75.8 | 71.4 | 64.8 | 52.5 | 36.9 | 1.0 |

- **Matches:** trig+0 to +5 are identical (trig+0 is pixel-identical); +10 is a touch denser; +40 is gone in both; the
  puff now lasts to about +30 (1.0 s) instead of +20 (0.67 s).
- **Doesn't match:** at +20 the puff is 1.36× r0's brightness change, not "about twice"; at +25 and +30 it is clearly
  visible, not "faint" and "very faint". **Explanation:** ten SoftDust quads overlap at the centre, so their alphas stack;
  the predicted per-particle alpha (0.24 at +20, 0.07 at +30) understates the stacked coverage, and the brightness
  change is not linear in alpha. The scuff outlasts the prediction, in the direction Shriram asked for.
- **Under the bulbs** (`r1-lit/`, captured after the change): the cream puff is lighter than the warm deck and reads
  against it from trig+0 to about +30; gone by +40. In both strips the darker FineGrit grains are not distinguishable
  from the puff (Claude's claim; Shriram to judge in play).

**My verdict** (Shriram, running preview, 1280×720): **kept** — "keep it", because "the puff now lingers about a second,
long enough to notice each step, and doesn't build up." *(This wording is the example Claude offered when asking for
a reason; Shriram adopted it as their verdict. "Doesn't build up" can only be judged with repeated steps, so it is
re-checked in normal play once the trigger is wired: TEST-REPORT A6 human checks.)*

**Strips:** `captures/footstep_scuff/r0-dark/`, `r0-retrigger/` (before); `r1-dark/`, `r1-lit/` (after). All fixture
captures.
