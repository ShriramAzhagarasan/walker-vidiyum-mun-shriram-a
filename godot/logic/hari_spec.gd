extends RefCounted
## Hari's size, collision and movement, in one place (metres). The character sheet references these.

const HEIGHT_M := 1.75              ## sprite image height maps to this (pixel_size = HEIGHT_M / texture height)
const CAPSULE_RADIUS := 0.28
const CAPSULE_HEIGHT := 1.70        ## total capsule height, bottom at the feet (y = 0)
const WALK_SPEED := 2.2             ## m/s on the XZ plane, camera-relative, no jumping
const INTERACT_RANGE := 1.6         ## m (XZ distance) to talk to an NPC
const PLACEHOLDER_PX := Vector2i(96, 216)   ## generated placeholder image size (same 4:9 frame as the art)
