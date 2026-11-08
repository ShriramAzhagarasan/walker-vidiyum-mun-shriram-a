extends Node3D
## A6 Effect B frame-strip preview (CHANGE-BRIEF §E). FIXTURE: loads the real slice
## (level art, sky, string lights, Hari, the in-game camera rig), holds the clock at
## 10:00 PM (inside NIGHT, before the 1740 cutoff), stands Hari under the middle
## span so the camera frames the bulbs, hides the HUD, and at frame 10 instantiates
## the StringLightMoths effect under the real deck. The three emitters get the §B.3
## preview seeds (101/202/303) and `use_fixed_seed = true` here only; the effect
## scene itself leaves use_fixed_seed off. At frame 70 the night condition ends and
## all three emitters set `emitting = false`; existing moths fade over the next
## ~72 frames (2.4 s lifetime at 30 fps) and are gone by frame 145 (§E).

const SLICE := preload("res://scenes/slice.tscn")
const MOTHS := preload("res://effects/string_light_moths.tscn")
const HARI_UNDER_BULBS := Vector3(12.0, 0.0, 1.0)  # same spot the scuff preview uses
const HELD_CLOCK := 22 * 60                        # 10:00 PM: NIGHT, before 1740
const ACTIVATE_FRAME := 10
const DEACTIVATE_FRAME := 70                       # §E: condition ends here
const SEEDS := [101, 202, 303]                     # §B.3: preview copies only

var slice: Node3D
var moths: Node3D = null
var _frame := 0

func _ready() -> void:
	slice = SLICE.instantiate()
	add_child(slice)
	LoopState.test_hold_clock = true
	LoopState.test_advance_to(HELD_CLOCK)
	slice.get_node("HUD").visible = false
	var hari: CharacterBody3D = slice.get_node("Hari")
	hari.position = HARI_UNDER_BULBS
	hari.reset_physics_interpolation()
	slice.get_node("CameraRig").snap()

func _process(_delta: float) -> void:
	_frame += 1
	if _frame == ACTIVATE_FRAME:
		_activate()
	elif _frame == DEACTIVATE_FRAME and moths != null:
		for child in moths.get_children():
			if child is GPUParticles3D:
				(child as GPUParticles3D).emitting = false

func _activate() -> void:
	moths = MOTHS.instantiate()
	var ei := 0
	for child in moths.get_children():
		if child is GPUParticles3D:
			var cp := child as GPUParticles3D
			cp.use_fixed_seed = true
			cp.seed = SEEDS[ei]
			ei += 1
	slice.add_child(moths)
