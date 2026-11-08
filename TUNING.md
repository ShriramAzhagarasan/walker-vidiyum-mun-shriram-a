# Tuning log (Assignment 6)

Every strip under `captures/` is a **fixture capture**: a preview scene (`godot/previews/`) rendered by Godot's Movie
Maker mode at 30 fps on the real renderer (Forward+, Apple M1 Pro), started by Shriram. Claude's reading of a strip is a
claim. Shriram's verdict in the running game, at the project's window size (1280×720), decides.

Each revision records Claude's prediction, the strips before and after, Claude's comparison and Shriram's verdict.

---

## 2026-11-08 — Effect A, revision r1 (in progress)

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
