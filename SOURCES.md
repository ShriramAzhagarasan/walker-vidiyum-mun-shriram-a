# Sources, credits and terms

## Started from
- **An empty Godot 4.7.2 project.** GDScript conventions and the headless test pattern were borrowed from Shriram's Assignment 1 repo [walker-jumpman-shriram-a](https://github.com/ShriramAzhagarasan/walker-jumpman-shriram-a), itself based on [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) by Nik Bear Brown. No A1 art, levels or characters are reused.

## Generative models (all run locally on a MacBook Pro M1 Pro, 16 GB; no paid services)
| Model | Version / revision | Used for | Ran with | License / terms |
|---|---|---|---|---|
| FLUX.2 [klein] 4B (Black Forest Labs) | HF `black-forest-labs/FLUX.2-klein-4B` @ `e7b7dc2` | character reference, poses (reference editing), environments | mflux 0.20.0 (MLX) | Apache 2.0 |
| Z-Image-Turbo (Tongyi-MAI) | HF `Tongyi-MAI/Z-Image-Turbo` @ `f332072` | comparison generations for the reference (2 rejected; none used) | mflux 0.20.0 | Apache 2.0 |
| Stable Audio Open 1.0 (Stability AI) | HF `stabilityai/stable-audio-open-1.0` @ `f21265c` | sound effects | diffusers 0.40.0, PyTorch 2.14.1 (MPS), EDMDPMSolverMultistepScheduler (the default sampler failed; see FRICTIONAL) | Stability AI Community License (free for non-commercial use and for organisations under US$1M annual revenue; attribution required) |
| MusicGen stereo-medium (Meta) | HF `facebook/musicgen-stereo-medium` @ `2747e61` | music loops | transformers 5.18.0, PyTorch 2.14.1 (MPS) | **CC-BY-NC 4.0, non-commercial**: acceptable for coursework; a commercial release of the game would need replacement music |
| rembg 2.0.85 with isnet-anime and BiRefNet-general | — | background removal | onnxruntime (CPU) | MIT (rembg); model weights per their repos (Apache 2.0 / MIT) |

**Prompt rules followed:** no named artists, copyrighted characters, brands, real people's likenesses, or existing songs or recordings in any prompt or reference. Every image prompt asks for a solid flat background, which is removed afterwards.

## Which model made which asset in the slice
| Asset | Model |
|---|---|
| Hari (10 states plus 2 walk frames), all derived from reference B | FLUX.2 [klein] 4B (reference edit) |
| Manikandan (2), Advay, Krishna | FLUX.2 [klein] 4B (Manikandan's phone pose edited from his idle image) |
| Villa, beach view, marble, fire, SUV | FLUX.2 [klein] 4B |
| Intro stills 1, 2, 4 / still 3 | FLUX.2 [klein] 4B / FLUX.2 [klein] 4B reference edit from Hari's reference |
| Phone buzz, clue chime, keys, dawn horn and screech, waves and crows | Stable Audio Open 1.0 |
| Party loop, gaana loop | MusicGen stereo-medium |
| Background removal on every character and SUV cutout | rembg (isnet-anime; BiRefNet-general for the SUV) |
| Code-built geometry (deck, pool walls, plinth, compound wall, railing, lights) | none: written by Claude in GDScript |
| Storyboard thumbnails and character-sheet spec drawings | none: code-drawn by Claude (Pillow) |

## Tools
- Godot 4.7.2.stable.official (macOS)
- Python 3.12 (uv virtual environments), Pillow, librosa, soundfile, ffmpeg
- Claude Code (Claude Opus 5.5): planning, code, prompts, docs, code-drawn design sketches
- Brutalist (course-provided `godot-gamedev` skill, walker modifier): the explainer film

## Who did what
| Area | Shriram (human) | Claude (AI assistant) | Generative models |
|---|---|---|---|
| Game idea, story, characters, setting, tone | Wrote and decided (`design/input/`) | Proposed the twist, loop rules, timeline and secondary characters; Shriram adopted them ("1. yes") | — |
| Design docs | Reviewed and approved | Drafted CONCEPT, STORYBOARD, CHARACTER-SHEET, CHANGE-BRIEF; code-drew the storyboard and spec sheets | — |
| Dialogue | Delegated, reviews | Drafted `DIALOGUE.md` | — |
| Assets | Chose Hari's reference (B) and the style target; caught defects in play (two phones, static motion, flat backdrops) that led to regenerations; reviews Claude's provisional picks (see ASSET-LOG "by" column) | Wrote prompts and scripts, ran generations, cut audio, removed backgrounds | Produced every art, SFX and music asset (see ASSET-LOG) |
| Code | Approved the 2.5D plan; played it 3 times and reported what felt wrong | Wrote the Godot project, tests and capture tools (some through Claude subagents) | — |
| Film | Reviews the final export | Wrote the script, capture driver and beat sheet; Liam narration via local Kokoro TTS (Brutalist) | — |

## Git identity note
The first 7 commits (up to `4e665a4`) were authored as `shrirampolarace <sazhagarasan@polarace.gg>`: Shriram's global git config from work, picked up by this new repo by mistake. They were pushed to his student GitHub account `ShriramAzhagarasan`. Shriram chose to keep them as they are (2026-10-07). From `97b6e7f` onward, the repo-local identity is `Shriram Alagarasan <azhagarasan.s@northeastern.edu>`.

## Asset log
See [ASSET-LOG.md](ASSET-LOG.md): one row per kept or seriously considered generation, with the exact prompt, seed, settings, outcome and edits.
