# Final QC — claude-liam-walker-vidiyum-mun-shriram-a-gamedev

- Export: `exports/landscape/claude-liam-walker-vidiyum-mun-shriram-a-gamedev.mp4` — 3840×2160 H.264, 30 fps, AAC 48 kHz, **378.20 s**, SHA-256 `e948a875752d4e1f3745054ad4fc0921d9d2dfd81313ed0e5b832db8b06502fe` (matches `.verified.json`, status `ready`).
- Source: git `13f772c` (godot/ snapshot `4e3bf647…`). Capture `capture/run-01` = `CAPTURE OK frames=5798`, counts 2/3/2/1/1, 10/10 states, 0 foreign inputs.
- `./art godot-gamedev --check`: PASS (110 files, 7 components, 4 exact excerpts, 4 code→result pairs).
- Gate V (compile.py final-frame check): 48 frames, BLOCKER 0, MAJOR 0.
- GATE T: 9 beats flagged, all inside game footage / reproduced asset images — see `GATE-T-OVERRIDE.md` (compiled with compile.py directly, A1 precedent). **Needs human sign-off.**

## Frames read (`_qc/contact-1..4.jpg`, 15/50/85 % of every beat)
- Bookends: B00 ask types and lands answered; B01 "prompt" → "pipeline" correction lands; B21 verdict; B22 Your Turn; B23 locked outro (title, @NikBearBrown, mascot, no subline).
- B02 real title screen + intro panels 1–2; B03 PHONE pose with Amma call card; B09 PHONE→IDLE→WALK→TALK at Krishna; B11 FF ">> x8", overhear, notes card, 1:40 Advay; B14 white-out (fully white frame mid-beat, intended) then 8 PM loop 2, labelled GAME AUDIO · NO NARRATION; B15 choice cursor, keys kept; B16 refusal caption, end card "…but someone is missing".
- Trace boards B04–B07 legible; B06 circles s302's second phone; B18 shows the matching 1:40 AM tiles of the R1 grids, enlarged (upscaled thumbnails: soft but readable).
- Minor: B19 "Assets + smoke" card reads "70 checks · 13 checks" (the "0 failed" was trimmed by the card format); B13 terminal text is small but legible at 4K.

## Audio (`_qc/levels.json`, export; `capture/run-01-sfx-levels.json`, capture)
- Narrated beats: mean −26.8 … −29.5 dB, peaks ≤ −3.3 dB. B14 (game audio only): mean −24.0 dB, audible. Outro tail (last 1 s): −91 dB max (silence; no game audio on the card).
- SFX vs the 1 s before, in the captured WAV (mean dB): phone_buzz loop 1 +12.5; clue (Selvam) +5.6; keys + clue (1:40) +7.1; dawn_crash +14.3; phone_buzz loop 2 +0.4 vs the 1 s before (that second is the crash's own tail) but **+11.6** vs the music-only second at 110.5 s; keys + clue (kept) +7.4; safe_dawn +9.2. Under narration the game audio sits at −20 dB.
