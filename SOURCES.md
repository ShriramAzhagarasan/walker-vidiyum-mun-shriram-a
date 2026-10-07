# Sources, credits and terms

## Started from
- **An empty Godot 4.7.2 project.** GDScript conventions and the headless test pattern were borrowed from Shriram's Assignment 1 repo [walker-jumpman-shriram-a](https://github.com/ShriramAzhagarasan/walker-jumpman-shriram-a), itself based on [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) by Nik Bear Brown. No A1 art, levels or characters are reused.

## Generative models (all run locally on a MacBook Pro M1 Pro, 16 GB; no paid services)
| Model | Version / revision | Used for | Ran with | License / terms |
|---|---|---|---|---|
| FLUX.2 [klein] 4B (Black Forest Labs) | HF `black-forest-labs/FLUX.2-klein-4B` @ `e7b7dc2` | character reference, poses (reference editing), environments | mflux 0.20.0 (MLX) | Apache 2.0 |
| Z-Image-Turbo (Tongyi-MAI) | HF `Tongyi-MAI/Z-Image-Turbo` @ `f332072` | comparison generations | mflux 0.20.0 | Apache 2.0 |
| Stable Audio Open 1.0 (Stability AI) | HF `stabilityai/stable-audio-open-1.0` @ `f21265c` | sound effects | diffusers 0.40.0, PyTorch 2.14.1 (MPS) | Stability AI Community License (free for non-commercial use and for organisations under US$1M annual revenue; attribution required) |
| MusicGen stereo-medium (Meta) | HF `facebook/musicgen-stereo-medium` @ `2747e61` | music loops | transformers 5.18.0, PyTorch 2.14.1 (MPS) | **CC-BY-NC 4.0, non-commercial**: acceptable for coursework; a commercial release of the game would need replacement music |
| rembg 2.0.85 with isnet-anime and BiRefNet-general | — | background removal | onnxruntime (CPU) | MIT (rembg); model weights per their repos (Apache 2.0 / MIT) |

**Prompt rules followed:** no named artists, copyrighted characters, brands, real people's likenesses, or existing songs or recordings in any prompt or reference. Every image prompt asks for a solid flat background, which is removed afterwards.

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
| Assets | Accepts or rejects every generation (see ASSET-LOG) | Wrote prompts and scripts, ran generations, cut audio, removed backgrounds | Produced every art, SFX and music asset (see ASSET-LOG) |
| Code | Approved the plan; playtests | Wrote the Godot project and tests | — |

## Asset log
See [ASSET-LOG.md](ASSET-LOG.md): one row per kept or seriously considered generation, with the exact prompt, seed, settings, outcome and edits.
