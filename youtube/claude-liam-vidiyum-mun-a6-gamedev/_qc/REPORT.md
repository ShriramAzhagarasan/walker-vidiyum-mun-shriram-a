# Gate V — visual QC report

Frames sampled: 60  ·  BLOCKER: 0  ·  MAJOR: 0

Regional text-contrast checks (all declared regions required): B04, B06, B08, B10, B12, B14, B16, B18, B20, B23, B24. Whole-frame dimming/scene color is not text contrast; empty-frame, fill and declared safe-area checks remain active. Visual content review remains required.

Clean — no BLOCKER/MAJOR defects. ✓

---

# Final export (2026-11-08 21:19)

`exports/landscape/claude-liam-vidiyum-mun-a6-gamedev.mp4`: 3840×2160, 30 fps, 430.9 s,
sha256 `5a5e381bd69906e0cff87e26bf8307952287c4e26931d38d01446b4ba0a29f85`; integrated −24.4 LUFS, LRA 5.3 LU, true peak
−3.0 dBFS. It was compiled with `compile.py` directly under the GATE T override Shriram approved (`_qc/GATE-T-OVERRIDE.md`). Gate V
(the section above, written by the final compile) found 60 frames, BLOCKER 0, MAJOR 0. `./art godot-gamedev --check`: PASS.

# Manual QC (Claude)

Frames sampled at 30 % and 80 % of every beat of the review cut (60 frames: `_qc/contact_0.png` … `contact_2.png`),
mid-beat frames of every code beat (`_qc/frames/`), and spot frames of the final (`_qc/frames/final_check.png`).
- Code beats: excerpts fit the panel at 24–30 px after two corrections (the first excerpts were 23–28 lines and clipped).
  Highlights land on the narrated lines. Path, line range and git `52fa183` are on screen, labelled "Godot editor reconstruction".
- Result beats: every segment is labelled FIXTURE / SCRIPTED CAPTURE / SHRIRAM'S OWN SCREENSHOT / CLAUDE'S ZOOM / HEADLESS.
  No held frames (B18 uses labelled half-speed segments).
- B12 narration revised at Shriram's request (~21:05). Its first claim is now attributed to Claude's difference image
  (TUNING.md:122). The beat was re-voiced (Kokoro am_onyx) and rebuilt. No other beat changed.
- B25/B26 board excerpts are verbatim quotes with their sources.
- Outro: ClaudeTitleOutro with exact title, @NikBearBrown and mascot. Spoken title plus "At Nik Bear Brown", no jingle.
- I did not listen end to end. Audio is the measured Kokoro narration, conformed without retiming.

# Known flaws (not fixed)

1. **B21 header.** The board's built-in header reads "GDD · DOCUMENT EXCERPT" above shader and scene lines. The header
   is hard-coded in the shared `GodotDesignBoard.tsx`. The edit to add an optional label was denied by the permission
   check, and I did not work around it. The excerpt itself is verbatim with line numbers, and the panel is labelled
   "ANNOTATION BY THIS FILM (CLAUDE) · not Shriram's notes".
2. **B03** narrates gravity, damping, the scale curve and the colour ramp. These settings are at `footstep_scuff.tscn:91-97`,
   outside the excerpt on screen (lines 74–86).
3. **B11** narrates the attractor sphere (radius 1.0, strength 0.3). It is at `string_light_moths.tscn:83-89`, outside the
   excerpt on screen (lines 69–81); only the notes panel shows it.
4. GATE T flags seven beats for blobs in captured pixels. That was overridden with Shriram's approval; see `GATE-T-OVERRIDE.md`.
