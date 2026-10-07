# COMPONENTS — what the film explains

Generated from `gamedev-evidence.json` (every file under `godot/` except `.godot/` and `*.uid`).

## hari-asset  (beats B03, B04, B05, B06, B07, B08, B09)

Hari's generated art as a game asset: ten state PNGs (FLUX.2 klein edits, rembg cutout, trim, 680 px leg-centred) shown on a fixed-Y, unshaded billboard Sprite3D sized to 1.75 m; hari.gd maps Story.hari_state to <state>.png, walks camera-relative and flips the sprite to face left.

Files: `assets/art/hari/.gitkeep`, `assets/art/hari/idle.png`, `assets/art/hari/idle.png.import`, `assets/art/hari/keys.png`, `assets/art/hari/keys.png.import`, `assets/art/hari/notes.png`, `assets/art/hari/notes.png.import`, `assets/art/hari/overhear.png`, `assets/art/hari/overhear.png.import`, `assets/art/hari/phone.png`, `assets/art/hari/phone.png.import`, `assets/art/hari/relief.png`, `assets/art/hari/relief.png.import`, `assets/art/hari/startled.png`, `assets/art/hari/startled.png.import`, `assets/art/hari/talk.png`, `assets/art/hari/talk.png.import`, `assets/art/hari/walk.png`, `assets/art/hari/walk.png.import`, `assets/art/hari/walk_1.png`, `assets/art/hari/walk_1.png.import`, `assets/art/hari/walk_2.png`, `assets/art/hari/walk_2.png.import`, `assets/art/hari/walk_3.png`, `assets/art/hari/walk_3.png.import`, `assets/art/hari/walk_4.png`, `assets/art/hari/walk_4.png.import`, `assets/art/hari/whiteout.png`, `assets/art/hari/whiteout.png.import`, `logic/hari_spec.gd`, `scenes/billboard_art.gd`, `scenes/blob_shadow.gd`, `scenes/hari.gd`

## night-logic  (beats B10, B11, B15, B16)

The loop: LoopState owns the clock (8 PM to 5:55 AM in 180 s, x8 while T is held), knowledge that persists, per-loop flags and one-shot timeline events; Story runs dialogue and Hari's state; Controls turns keys into logic calls; dialogue.json holds every line.

Files: `autoload/controls.gd`, `autoload/loop_state.gd`, `autoload/story.gd`, `data/dialogue.json`, `logic/input_setup.gd`, `logic/story_data.gd`, `project.godot`

## sound  (beats B03, B12, B13, B15)

SoundBank listens to five LoopState signals (phone_buzz, clue_saved, keys_exchanged, dawn_crash, safe_dawn) and two music loops on separate buses; it never changes game state and counts every request for tests.

Files: `assets/audio/music/.gitkeep`, `assets/audio/music/gaana_loop.ogg`, `assets/audio/music/gaana_loop.ogg.import`, `assets/audio/music/party_loop.ogg`, `assets/audio/music/party_loop.ogg.import`, `assets/audio/sfx/.gitkeep`, `assets/audio/sfx/clue_saved.ogg`, `assets/audio/sfx/clue_saved.ogg.import`, `assets/audio/sfx/dawn_crash.ogg`, `assets/audio/sfx/dawn_crash.ogg.import`, `assets/audio/sfx/keys_exchanged.ogg`, `assets/audio/sfx/keys_exchanged.ogg.import`, `assets/audio/sfx/phone_buzz.ogg`, `assets/audio/sfx/phone_buzz.ogg.import`, `assets/audio/sfx/safe_dawn.ogg`, `assets/audio/sfx/safe_dawn.ogg.import`, `autoload/sound_bank.gd`, `default_bus_layout.tres`

## world  (beats B02, B11, B16, B17, B18)

The 3D deck: slice.tscn/slice.gd build the marble deck, backdrops, NPC billboards, SUV, lights and a sky driven by the clock (revision R1 retuned the night values); a Telltale-style follow camera blends zone presets.

Files: `assets/art/env/.gitkeep`, `assets/art/env/beach_backdrop.png`, `assets/art/env/beach_backdrop.png.import`, `assets/art/env/fire_glow.png`, `assets/art/env/fire_glow.png.import`, `assets/art/env/marble.png`, `assets/art/env/marble.png.import`, `assets/art/env/suv.png`, `assets/art/env/suv.png.import`, `assets/art/env/villa.png`, `assets/art/env/villa.png.import`, `assets/art/npc/.gitkeep`, `assets/art/npc/advay.png`, `assets/art/npc/advay.png.import`, `assets/art/npc/krishna.png`, `assets/art/npc/krishna.png.import`, `assets/art/npc/manikandan.png`, `assets/art/npc/manikandan.png.import`, `assets/art/npc/manikandan_phone.png`, `assets/art/npc/manikandan_phone.png.import`, `assets/art/ui/.gitkeep`, `scenes/art3d.gd`, `scenes/camera_rig.gd`, `scenes/deck_dressing.gd`, `scenes/environment_fill.gd`, `scenes/fallback_prop.gd`, `scenes/slice.gd`, `scenes/slice.tscn`, `scenes/textured_surface.gd`

## ui  (beats B11, B15, B16)

Screen-space twins of every sound: phone card, notes card, captions, white-out, pause overlay and end card, plus the phone-style HUD clock and mute indicators.

Files: `ui/dialogue_panel.gd`, `ui/hud.gd`, `ui/notes_toast.gd`, `ui/screen_cards.gd`, `ui/whiteout.gd`

## intro  (beats B02)

The main scene: a title screen and a four-panel intro motion comic (generated stills, captions, gaana music, the dawn horn on panel 4); Enter advances, Esc skips, then it changes to slice.tscn, where loop 1 starts itself.

Files: `assets/art/intro/intro_1.png`, `assets/art/intro/intro_1.png.import`, `assets/art/intro/intro_2.png`, `assets/art/intro/intro_2.png.import`, `assets/art/intro/intro_3.png`, `assets/art/intro/intro_3.png.import`, `assets/art/intro/intro_4.png`, `assets/art/intro/intro_4.png.import`, `scenes/intro.gd`, `scenes/intro.tscn`

## tests  (beats B13, B19, B18)

Headless tests (exact sound counts over two scripted loops, loop logic, scene smoke, asset presence) and the scripted screenshot tool used for TEST-REPORT evidence; they use the test API, not played input.

Files: `tests/harness.gd`, `tests/test_assets_present.gd`, `tests/test_audio_mix.gd`, `tests/test_loop_logic.gd`, `tests/test_slice_smoke.gd`, `tests/test_sound_triggers.gd`, `tools/capture_intro.gd`, `tools/capture_shots.gd`

## Excerpts shown (verbatim)

- B08: `godot/scenes/hari.gd` lines 83–90
- B10: `godot/autoload/loop_state.gd` lines 164–175
- B12: `godot/autoload/sound_bank.gd` lines 45–51
- B17: `godot/scenes/slice.gd` lines 23–32

## Code → visible result

- B08 → B09: In real play the call closes and PHONE becomes IDLE, then WALK and TALK: each state swaps the billboard image, at one height. (`media/B09.mp4`)
- B10 → B11: Holding T, the HUD shows >> x8 and the clock races; at 1:21 the overheard call and its clue fire once; at 1:40 at 1x Advay takes the keys once. (`media/B11.mp4`)
- B12 → B13: Recorded test output: exact per-event request counts (2/3/2/1/1), identical with both buses muted, matching the filmed run’s driver summary. (`media/B13.mp4`)
- B17 → B18: R1 before/after screenshots: lavender sky and washed-out marble become a night sky with warm pools under the string lights. (`media/B18.mp4`)
