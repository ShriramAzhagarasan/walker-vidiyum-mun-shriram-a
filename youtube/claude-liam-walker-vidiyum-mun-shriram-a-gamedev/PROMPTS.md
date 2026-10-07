# PROMPTS — every prompt shown or spoken in the film

## B00 — Walker ask (illustrative reconstruction, labelled on screen; not a transcript)
> Please use Walker to convert my game design document about Vidiyum Mun, a time-loop mystery at the last party on a fenced beach villa on ECR, Chennai, into a playable 2.5D Godot slice: a 3D marble deck, my hero Hari as generated cel-shaded art in ten states, and generated sound effects and music wired to real game events.

Why: names the actual game, the 2.5D decision (SHRIRAM-DECISIONS 2026-10-06) and the assignment's asset scope. The real session was many smaller requests (`design/input/SHRIRAM-DECISIONS.md`).

## B05 — the traced generation prompt (real, verbatim)
Source: `gen/log.jsonl`, asset `CHAR-HARI-PHONE`, model `flux2-klein-4b`, `edit_refs: design/character/gen/hari-ref.png`, 768×1344, quantize 8, seeds 301 and 302 (identical prompt). Copied to `evidence/asset-trace/phone-s302-log-row.json`.
> The same young man from the reference image: identical face, hair, skin tone, maroon and cream checked half-sleeve collared shirt untucked, dark indigo jeans and blue-strap rubber flip-flop slippers, same proportions and the same flat cel-shaded style with clean dark outlines. Whole body visible from hair to slippers, three-quarter front view facing right. Holding a dark smartphone to his ear with his elbow clearly raised out to the side, other hand in his jeans pocket, eyes looking slightly away and guilty, as if telling a small lie. Flat cel-shaded 2D game illustration, clean uniform dark outlines, two-tone shading, flat colours, no texture, no gradients. Solid flat light grey background, no shadow on the background, no text, no logos.

## B22 — Your Turn (read aloud verbatim, then discussed)
> I have a character sheet and one generated reference. For one pose: (1) write an edit prompt that changes only the pose clause; (2) name the silhouette risk at my in-game pixel height; (3) list the cleanup steps, and a check that the feet stay put when the sprite flips.

Why: it generalises exactly the chain the film traced (spec → prompt → raw → edits → engine) and forces a check the viewer can verify in their own engine, instead of trusting the answer.

## Film-production prompts
The film is built from `BUILD-PROMPT.md` (paste-ready). No paid API, no image/video generation was used to make the film itself; all visuals are Remotion scenes, real engine capture and the game's own committed images.
