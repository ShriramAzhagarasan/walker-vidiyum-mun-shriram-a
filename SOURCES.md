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

## Assignment 3 (three Blender assets)
| Tool | Version | Use |
|---|---|---|
| Blender | 5.2.2 LTS (Homebrew cask `blender`) | modelling the SUV, rock shrine and fence from basic shapes; glTF export |
| MCP for Blender (community project named in the syllabus) | `mcp-for-blender` 2.1.9 via `uvx`; add-on panel shows "Addon 1.8" | lets Claude Code run Blender Python in Shriram's open session over a localhost socket (127.0.0.1:9876) |
| uv / uvx | 0.12.21 | runs the MCP server |
| GNU coreutils `timeout` | 9.12 | bounds the headless Godot checks |
| Godot | 4.7.2.stable.official | import, the showcase scene, the headless check |

**Switched off and unused:** Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin, Hunyuan3D, Tripo, and the MCP tools `generate_3d`, `search_assets`, `import_asset`. Every mesh is built from Blender's basic shapes; no downloaded or AI-generated mesh is used. Telemetry was disabled with `DISABLE_TELEMETRY=true`. No credentials are committed.
**Colours:** the SUV body `#333738` was sampled from the A2 SUV art (`godot/assets/art/env/suv.png`); the fence's wood and rope match the A2 beach art; every other hex value was chosen in the A3 brief (revisions 1–3 in CHANGE-BRIEF.md). No colour or material comes from an outside source.
**Who did what (A3):**
| Area | Shriram (human) | Claude (AI) |
|---|---|---|
| Assets and brief | Chose the three assets; approved the brief; chose the lore-faithful shrine and the wooden fence; set the SUV's look (modern luxury SUV, doors, windows, lights, tailgate, exhaust) | Drafted the brief's numbers from the game's code; spotted the brief/lore and brief/art conflicts; wrote revisions 2–3 from Shriram's words |
| Blender | "Learn the window" notes and screenshot; enabled and connected the add-on; approved each plan; judged every build (rejected SUV builds 1–3); the hand edit on the fence sign | All Blender Python run through the MCP (`tools/blender/`), measurements after each object, the glTF export code |
| Godot | The look check, orbiting each asset including behind and below | The showcase scene and its two revisions, the headless check and self-test, the screenshot capture script |
| Film | Recorded the Blender session (`blendersession.mov`); watches and uploads the film | Beat sheet, script, narration, edit (Brutalist `godot-gamedev`, walker) |
| Docs | Interface notes, hand-edit paragraph (approved as their own), look-check words, reflection | TEST-REPORT, FRICTIONAL AI-recorded entries, SOURCES, README |

## Assignment 5 (shaders and materials)
### AI assistance outside Claude Code (Shriram's disclosure, 2026-10-28)
- **Tool:** OpenAI ChatGPT, the latest model offered in the ChatGPT app at the time (Shriram, 2026-11-01: "whatever is
  the latest chatgpt model"). The exact version wasn't noted.
- **Purpose (Shriram's words):** "I provided the shader requirements, initial pixel values, blending formula, uniform
  parameters, and colour-space experiment setup. I used ChatGPT to help calculate and verify the expected RGB values, explain
  sRGB decoding and encoding, and organize the mathematical working. I reviewed the outputs against the assignment
  requirements."
- **Used for:** the predictions in CHANGE-BRIEF.md §1.8 (pixel values, transparency, contrast ratios) and §2.5 (hint
  experiment). Claude recomputed every value independently on 2026-10-28 and they match.
- **Also used for (2026-10-29):** writing `godot/shaders/deck_marble.gdshader` and `godot/shaders/hint_experiment.gdshader`.
  Shriram's words: "i used chatgpt's help as i'm learning all of this for the first time." Claude Code gave a slot-by-slot
  outline (names, hints and built-ins from CHANGE-BRIEF.md §2.3 and §2.5) and reviewed both files in prose. It did not
  write or edit either file. `night_skip.gdshader` (commit `51e18aa`) is separate from this note: Shriram typed that
  file themself. Its colour line is the one from CHANGE-BRIEF.md §1.4, which Shriram worked out with ChatGPT's help
  on the maths and wording (Shriram, 2026-11-01: answer "a" to "did ChatGPT help write the shader file?").
- **LANGUAGE-NOTES.md (2026-11-01):** rewritten by Shriram in their own words on 2026-11-01; an earlier draft was
  paraphrased by ChatGPT. That earlier draft (commit `bd1c458`) had Shriram's answers and reasoning, with ChatGPT used
  only to paraphrase the wording ("i had to be sure so i used it for just paraphrasing but the thought and everything
  was done by me"). For the final version, which adds the annotation of the generated shader, Shriram said: "i wrote it".
  Claude Code checked every line reference in both versions (four were wrong in the first draft and Shriram corrected
  them). In the final version it pointed out two accuracy slips without supplying wording. It did not write or change
  any answer.
- **FRICTIONAL.md A5 reflection (2026-11-01):** written by Shriram, with ChatGPT paraphrasing the wording (Shriram: "i
  used chatgpt for paraphrasing from everything that i wrote"). Claude placed it unchanged and labelled it so.

### Textures (A5)
| Asset | Author | Licence | Source | Used for |
|---|---|---|---|---|
| Marble 01 (`marble_01`), 2K PNG: diff, rough, nor_gl, nor_dx | Rob Tuytel | CC0 1.0 | <https://polyhaven.com/a/marble_01> | the deck floors (`marble_dry`, `marble_wet`); nor_dx only for the curl check |
| Floor Tiles 06 (`floor_tiles_06`), 2K PNG: nor_gl, nor_dx | Rob Tuytel | CC0 1.0 | <https://polyhaven.com/a/floor_tiles_06> | curl-check calibration only (`godot/tests/data/curl/`) |
| `hint_strip_3x1.png` | written by `godot/tools/write_hint_strip.gd` | project file | this repo | the hint experiment |

Downloaded 2026-10-29 through the Poly Haven API, unmodified. Credits also in `godot/assets/textures/marble_01/ATTRIBUTION.md`.

### Who did what in A5
- **Shriram:**
  - chose the state (night skip on T), the object (the phone status bar), the colour (sodium orange), both fade
    times, the re-press and pause rules, the time scale, the marble, where it goes, and wet vs dry;
  - wrote the colour line, the pixel and hint predictions and the Part 3 answers (maths with ChatGPT, above);
  - hand-wrote `night_skip.gdshader`; wrote `deck_marble.gdshader` and `hint_experiment.gdshader` with ChatGPT's help;
    converted the StandardMaterial3D for Step 4 in the editor; wrote LANGUAGE-NOTES.md in their own words (an earlier draft was paraphrased by ChatGPT);
  - ran all three shader mutations by hand;
  - did the human checks (shader edit, material edit, playtest, seams, sweep check);
  - approved the driver plan and the docs.
- **Claude Code.** Models, read from the transcripts: the CLAUDE.md draft (`prompts/a5/session-1.jsonl`) and the
  audit (`session-3.jsonl`) ran as `claude -p` on `claude-opus-4-7`; the interactive session that did everything else
  ran on Claude Opus 5.5 (`claude-opus-5-5`). Claude Code drafted CLAUDE.md (reviewed and corrected) and wrote:
  - the status-bar split, the driver and `test_night_skip.gd`;
  - the texture downloads and import settings, the materials and floor wiring, the hint strip script, scene and
    materials;
  - `normal_map_check.gd` (around the course's `curl_ratio`) and the capture tool;
  - the audit review and corrections, the TEST-REPORT, README and FRICTIONAL drafts, and the film (beat sheet, script,
    Kokoro "Liam" narration, render).

  It reviewed Shriram's shaders in prose only, and never edited a `.gdshader`.
- **Audit agent** (a scoped `claude -p` run of the course prompt, `prompts/a5/session-3.jsonl`): wrote `godot/MATERIALS.md`
  and `godot/tests/test_materials.gd`. Committed unedited, then reviewed by Claude: one invented number removed, one
  finding corrected, one test gap closed.

### Starting point, tools and further AI contributions (A5)
- **Starting point:** this repository at tag `a3` (Assignment 3). A5 is the commits after it (`git log a3..a5`).
- **Narration model:** Kokoro-82M v1.0 (ONNX, via `kokoro-onnx`), Apache-2.0, run locally by the course-provided
  Brutalist pipeline; voice `am_onyx` ("Liam"). No paid or cloud voice service.
- **Film tooling:** the course-provided Brutalist `godot-gamedev` skill with the walker modifier (`../brutalist.art`),
  Remotion for the scene renders. Details are in the film's own records under `youtube/claude-liam-vidiyum-mun-a5-gamedev/`.
- **Claude's part in the brief and in Shriram's learning** (in addition to the list above):
  - Claude offered the options for each decision in the chat. Shriram chose from them, then accepted Claude's six
    recommendations for the rest (FRICTIONAL.md, 2026-10-28).
  - Claude organized Shriram's decisions into CHANGE-BRIEF.md and filled in the project facts (brief header).
  - Claude explained `mix()` with worked examples before Shriram wrote the colour line.
  - Claude gave the slot outline for the two Part 2 shaders.
  - Claude reviewed CLAUDE.md (`1ccf2ff`) and the audit (`b8179c3`). Shriram approved the CLAUDE.md review. Their own
    checks are the human checks in TEST-REPORT A5.8.

## Assignment 6 (particle effects)

- **ChatGPT (same app model as A5; the exact version wasn't noted):** Shriram wrote CHANGE-BRIEF.md Parts A–H with
  ChatGPT's help on **the wording and structure** and on **the price predictions** in Part G (Shriram, 2026-11-08:
  "chatgpt helped me with the wordings and structuring of thing and also helped with price predictions"). Shriram named
  only those two areas; Shriram chose the effects and the retrigger rule from options Claude laid out. Claude
  placed the text unchanged apart from edits Shriram dictated (see the brief's header).
- **ChatGPT, later uses (Shriram, 2026-11-08, in the FRICTIONAL.md A6 reflection):** ChatGPT "helped me plan the
  effect settings and explain the generated process shader", and the A6 reflection "was drafted with ChatGPT
  assistance using the available screenshots and reported debugging observations". The process-shader notes in
  TEST-REPORT.md are Shriram's, written after ChatGPT's explanation of the shader. Claude checked only their line numbers.
- **Claude Code (Claude Opus 5.5, Northeastern access):** wrote §0 of the brief (project facts), ran the scoped
  `claude -p` build sessions (`prompts/a6/`), and wrote the CLAUDE.md revision, effect scenes, previews, trigger code,
  tests and cost script, as recorded per step in TEST-REPORT.md and TUNING.md.
- **A6 film:** made by Claude Code through the course-provided Brutalist `godot-gamedev` skill (walker modifier).
  Narration is Kokoro-82M v1.0 `am_onyx` ("Liam"), Apache-2.0, run locally. Records are in
  `youtube/claude-liam-vidiyum-mun-a6-gamedev/`. Shriram approved the GATE T override and the B12 wording, and watched
  the final.
- **A6 textures: procedural, no external images.** The scuff's soft dots are `GradientTexture2D` resources in
  `godot/effects/footstep_scuff.tscn`. The moth silhouette `godot/effects/moth.png` is generated by `godot/tools/moth_texture.gd`
  (agent-written in Step 5, revised by Claude at B r3; regenerate with `write_moth_texture.gd`). No licence applies.
