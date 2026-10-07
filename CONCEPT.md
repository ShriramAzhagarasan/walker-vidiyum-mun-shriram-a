# Vidiyum Mun (விடியும் முன், "Before Dawn"): concept

*Revision 1, 2026-10-06, committed before any generation. Story: Shriram (`design/input/STORY-BIBLE-v1.md`, `-v2.md`). This page: drafted by Claude from that story, reviewed by Shriram.*

## The game in two sentences
You are **Hari**, a broke final-year engineering student at the last party on a rich family's illegally fenced beach on ECR, Chennai. Every dawn something terrible happens and you wake at 8 PM again, so you explore the night, talk to the people the party ignores, and carry what you learn into the next loop to change how dawn arrives.

## Core loop
**Explore → notice → note → dawn → return earlier.**
- **Repeat:** walk the night while the clock runs (8 PM to dawn), overhear and talk to people, and save what you learn to Hari's phone notes. Dawn resets the night and keeps the notes.
- **Decide each loop:** *where to be, and whom to talk to, before the moments that matter* (e.g. 1:40 AM, when Advay takes the car keys). You can't be everywhere in one night.
- **Risk:** miss a window and the tragedy plays out again. You lose the whole night, and the dawn sounds just as bad as last time.

The slice proves one full turn of this loop: loop 1 earns two clues (an overheard call, the keys taken); loop 2 uses them before 1:40 to keep the keys with Manikandan.

## Pillars
| Pillar | What it means for the player | Visual choice that honours it | Sound choice that honours it |
|---|---|---|---|
| **See the people nobody sees** | The only verb that changes the night is paying attention to the driver, the watchman and the village. | Manikandan is drawn and lit with the same care and size as the rich guests, and stands in his own pool of light by the SUV. | The village's gaana music stays audible under the party's dance music all night. |
| **Every loop, you see more** | Knowledge is the only thing you keep. | The phone-notes clue card. The *Ask about Selvam* choice appears only once the clues exist. Hari wakes with damp patches on his shirt. | A soft clue chime, the same every time, so "I learned something" becomes a sound the player listens for. |
| **Dawn is always coming** | A clock is always running. | The phone-style clock on the HUD. The sky shifts from indigo to pre-dawn grey to pink as the night runs out. | The party music thins after 3 AM. At dawn both musics stop and the highway takes over. |
| **The night belongs to Chennai** | This could only be ECR. | A white glass villa on Italian marble beside a fishing village. Warm string lights, the orange sodium glow from the road, a plain rock as a shrine. Hari's checked shirt and rubber chappals among the sneakers. | Tanglish lines, gaana-style hand percussion, crows at first light, waves. |

## Art direction
**2.5D, Telltale-style:** a real-time 3D deck in Godot (marble floor, glass villa, glowing pool, warm point lights, a sky that follows the clock) with **flat cel-shaded illustrated characters** standing in it as billboards, one static image per state.

Cel shading (flat colour areas and a dark outline) is easier to keep identical across poses from a free local model than painted shading. It also leaves mood and depth to the 3D lighting, which serves *Dawn is always coming*. The ordinary middle-class details (the checked shirt, the cracked phone, the chappals) carry *See the people nobody sees*.

**Reference notes, in words:**
- **Material and light:** polished Italian marble reflecting warm ~2700 K string lights and the cyan of a lit pool, with glass walls glowing amber from inside.
- **Air and place:** a humid coastal night over the Bay of Bengal. Haze softens the far lights, fishing-boat lamps sit on the horizon, and a small bonfire burns behind a wire fence.
- **Era and mood:** 2020s Chennai, lit by phone screens and the orange sodium glow of East Coast Road. Dawn arrives as a pink, washed-out sky over wet sand, beautiful and wrong.

**Not:** glossy luxury-ad rendering, anime idol faces, cartoon exaggeration of the village, brand logos, or any real person's likeness.

## Audio direction
- **What it should make the player feel:**
  - *8 PM:* outsider excitement, too loud.
  - *Midnight to 3 AM:* uneasy, because something is building across the fence.
  - *Dawn:* dread, then the shock of a sound you never see.
  - *The safe dawn in loop 2:* relief that sours.
- **Two musics across one fence:** the party's electronic dance loop (synth bass, four-on-the-floor) and the village's gaana-style loop (hand percussion, harmonium, raw energy). Walking toward the railing crossfades from one to the other: the fence, heard.
- **When the music changes or stops:**
  - **Pause:** muffled through a low-pass filter and 8 dB quieter.
  - **After 3 AM:** the party loop thins out.
  - **At dawn:** both stop, before the horn and brake screech (the failure) or before the waves and crows (the safe dawn).
  - **Ending:** stays stopped at the end card.
  - **Restart:** at 8 PM, together with Amma's call.
- **Never shown, only heard:** the crash. The highway exists only as sound.
- **Muted readability:** every sound has a visual twin. The phone UI shows Amma's call, the notes card shows a clue, a keys icon shows the keys changing hands, headlights, shake and white-out show the crash, and a sunrise shows the safe dawn.

## Scope of the A2 slice
- **Location:** one location (gate → marble pool deck → railing above the beach), two loops, about 5–6 minutes of play.
- **Characters:** Hari (playable, 10 states), Manikandan (2 states), Advay (1), Krishna (1, ambient).
- **Out of scope:** the beach, the village, the house interior, loops 3 onward, voice acting, video cutscenes, full 3D character models.
