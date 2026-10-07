# Frictional log: Vidiyum Mun (A2)

Dated log of the design as it happened. Each entry separates **Shriram** (the human: decisions, taste, edits), **Claude** (AI assistant: plans, code, prompts, drafts) and the **models** (generated outputs).
Entries for 2026-10-01 and 2026-10-02 are **retrospective**, written on 2026-10-06 from the Claude Code session transcript and Shriram's verbatim messages in `design/input/SHRIRAM-DECISIONS.md`.

## 2026-10-01: choosing the game (retrospective)
- **Wanted:** the game I actually want to build this semester, a story-driven open-world feel inside one location, as an homage to Chennai.
- **Asked / decided (Shriram):** picked "The Last Party: a time loop on ECR" and made it about a middle-class Chennai boy taken to a rich kid's beach-house party.
- **What Claude gave:** a refined pitch with generic local colour (an auto driver waiting outside, a woman selling sundal on the sand at midnight).
- **Decided (Shriram):** rejected those details as generic and stereotyped. There'd be a family driver, not an auto driver, and nobody sells sundal at that hour. Gave the real geography instead: an empty private beach, a fence, and a public beach where local guys drink and look like trouble. Tone from Tamil films with this kind of plot.
- **Next:** named the cast (Hari, Aadhav, Vastav, Manikandan) and the title *Vidiyum Mun*.
- **Human / Claude / model:** Shriram's idea and corrections; Claude's drafts. No models yet.
- **Still unresolved then:** what actually happens at dawn.

## 2026-10-01 to 02: toolchain (retrospective)
- **Wanted:** free, local models that run on a 16 GB M1 Pro, with licences that suit a personal project later.
- **Tried (Claude):** FLUX.1-schnell and Kontext. Both turned out to be gated behind a Hugging Face login. Found FLUX.2 [klein] 4B and Z-Image-Turbo (Apache 2.0, ungated) instead, plus MusicGen and Stable Audio Open (gated: Shriram logged in and accepted the licence).
- **Friction:** the first download commands passed exclude patterns wrongly and fetched incomplete weights; this was caught by checking file sizes and re-run. Pillow here has no Tamil shaping (no raqm), so the Tamil script was dropped from the code-drawn sketches (it renders correctly in Godot).
- **Decided:** use Klein 4B as the main image model, because it can edit from a reference image, and the course says consistency comes from the reference.

## 2026-10-02: the story (retrospective)
- **Shriram** wrote the full plot and design reference (`design/input/STORY-BIBLE-v1.md`): the Manimekala Theivam rock, the illegal fence, the officials sealing the beach at 7 AM, Advay the cousin, Manikandan as Selvam's uncle. He tagged each item (Shriram) or (Claude).
- **Claude** proposed the "Hari already died once" twist, Muthu, the old woman at the rock, the hour-by-hour chain (fence → bottles → rockets → fire → drowning and crash), and the loop-2 slice script.
- **Decided:** keep the crash off-screen (sound only).

## 2026-10-06: approvals and the 3D decision
- **Decided (Shriram, verbatim in SHRIRAM-DECISIONS):**
  - adopted all of Claude's story-bible items, the cel-shaded style and the four pillars;
  - renamed Aadhav to **Krishna**, so he isn't confused with Advay;
  - the villa is "a white villa with glass … italian marble … warm lights";
  - **the game should be 3D, like Life is Strange or a Telltale game.**
- **Claude** laid out the trade-off with 24 hours left and free local models only. Full 3D character models (image-to-3D) would be rough and might not finish. 2D now and 3D later is the safest. 2.5D means a real 3D deck with generated cel-shaded characters as billboards.
- **Decided (Shriram):** 2.5D, Telltale-style.
- **Consequence (Claude):**
  - The character sheet switched from profile to a three-quarter front view.
  - On-screen size became about 300 px (deck) and 208 px (gate), from the camera distance and field of view.
  - The background-removal and billboard risks were added to the predictions (F3, F9).
- **Silhouette test finding** (from the code-drawn spec, before any generation): IDLE, PHONE and OVERHEAR are nearly identical at 208 px. That became predicted failure F5 and a generation rule (PHONE: elbow out; OVERHEAR: lean back, head turned).
- **Palette finding:** a light-blue shirt (the first idea) would vanish against the white villa (contrast ~1.2:1). Switched to a maroon and cream check, which gives ≥ 3:1 against every background for at least one large shirt value (table in CHARACTER-SHEET).
- **Human / Claude / model:** Shriram decided the direction. Claude drafted all design docs, code-drew the storyboard and spec sheets, and drafted the dialogue at Shriram's request. No generations before this commit.
- **Still unresolved:** whether MusicGen can produce a gaana loop that sounds like Chennai (F8); the citation for Manimekala in the epic.
