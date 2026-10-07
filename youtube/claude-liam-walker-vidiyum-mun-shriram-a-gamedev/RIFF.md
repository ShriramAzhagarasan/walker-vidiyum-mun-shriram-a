# RIFF — observation → interpretation → narration

Observations checked against the final take `run-01` (frozen build e227f23, all SFX). Exact clip ranges: `SHOTLIST.md`. Rows marked with seconds below were first drafted on the pre-freeze `validate-720` take; the events are the same, the times differ (intro adds ~32 s).
Observations are what the footage/log shows; interpretations are marked as such. Scripted input is never called a playtest.

| Beat · artifact + range | Visible / logged observation | Interpretation (source) | Narration (short) | Next experiment |
|---|---|---|---|---|
| B02 · capture 0–16.5 s | Title screen, Enter, intro panels 1–2 (generated stills, captions) | The game's own framing of the concept (intro.gd) | Concept + four pillars | — |
| B03 · capture 32.4–42.5 s | 8:00 PM, loop 1; incoming-call card; Hari in PHONE with the phone at his ear, elbow out; three call lines advance on E (frames 92/188/284) | The spec's F5 rule is visible at deck framing (CHARACTER-SHEET l.21) | "Hari switches to his phone pose: phone at the ear, elbow out." | Check PHONE vs IDLE at gate framing (208 px) |
| B04–B07 · trace boards | Spec PHONE #4; prompt pose clause; s301 vs s302; s302 trim box and the cut file 246×692 | The pose rule travels from spec → prompt text → seed choice → leg-centred file | Steps 1–4 | Resolved before the freeze: Shriram caught s302's second phone in a playtest screenshot; s301 replaced it (`gen/decisions.json`). B06 shows this. |
| B09 · capture ~7.9–18.9 s | `hari_state` PHONE→IDLE at the call close, WALK while D is held, TALK at Krishna (K1) | `_show_state` swaps the image; the height stays 1.75 m (billboard_art.gd l.34) | "phone becomes idle … walk … talk" | If the walk cycle lands, confirm frames step with distance (no foot slide) |
| B11 · capture ~32–57 s | HUD `>> x8` while T is held; 1:21 E → OVERHEAR line; notes card + clue (KNOW_SELVAM); 1:40 at 1× Advay at the SUV, keys move, second notes card | One-shot flags fire once each; fast-forward passes the same checks (loop_state.gd `_set_clock`) | "The driver holds the real T key …" | Hold T through 1:40 to show the same single event at 8× |
| B14 · capture ~67.4–78.9 s | 5:50 AM: headlights, shake, white-out, WHITEOUT pose; 8:00 PM loop 2, STARTLED | The crash is heard, never seen (CONCEPT l.49) | (none: game audio only) | Muted playtest: does the white-out alone read as a crash? (F10) |
| B15 · capture ~88–111 s | Choice "> Ask about Selvam" / "Just getting some air"; cursor S then W; 4 lines; KEYS pose, keys icon travels to Manikandan, third note | The choice is gated on both clues (loop_state.gd `ask_selvam_available`) | "now the choice exists, because both clues are in his notes" | Try "Just getting some air" and confirm the crash repeats |
| B16 · capture ~125–153 s | 1:40 refusal captions, no keys event in the log; T to the railing; safe_dawn; RELIEF; sunrise; end card | Keys didn't move → no `keys_exchanged` (loop_state.gd `_advay_arrives`) | "No jingle this time, because the keys didn't move." | — |
| B18 · R1 boards | Before: lavender sky, bright marble; after: night sky, warm pools under the string lights | Unshaded billboard keeps Hari's colours (billboard_art.gd l.16) | "Only the world around him changed." | Contrast check around Hari in both (F4) |

Human judgement (fun, feel, whether the gaana sounds like Chennai) is Shriram's; the film does not claim it.
