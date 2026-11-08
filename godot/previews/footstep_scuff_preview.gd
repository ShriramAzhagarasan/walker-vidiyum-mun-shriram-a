extends Node3D
## A6 Effect A frame-strip preview (CHANGE-BRIEF §E). FIXTURE: loads the real slice (level art, sky, string lights,
## Hari, the in-game camera rig), holds the clock at 10:00 PM, stands Hari still at the dark gate or under the warm
## bulbs, hides the HUD, and spawns a FootstepScuff at Hari's floor position on frame 10 (and frame 21 with
## `retrigger`). The scuff's particles use a fixed seed here only, so before/after strips are comparable; the effect
## scene itself never sets one (repeats in play must vary).

const SLICE := preload("res://scenes/slice.tscn")
const SCUFF := preload("res://effects/footstep_scuff.tscn")
const HARI_DARK_GATE := Vector3(3.5, 0.0, 1.0)   # §0: the darkest stretch is the gate end (x < 5)
const HARI_UNDER_BULBS := Vector3(12.0, 0.0, 1.0) # §0: under the string lights, middle span
const HELD_CLOCK := 22 * 60                       # 10:00 PM, the A5 judging time; no timeline event before 1:20 AM
const TRIGGER_FRAME_FIRST := 10
const TRIGGER_FRAME_SECOND := 21                  # §E, 11 frames after the first (one real step at 30 fps)
const PREVIEW_SEED := 6

@export var lit: bool = false                     # false = dark gate, true = under the warm string lights
@export var retrigger: bool = false               # on = a second scuff at frame 21 while the first is still alive

var slice: Node3D
var _frame := 0

func _ready() -> void:
	slice = SLICE.instantiate()
	add_child(slice)                              # slice._ready() starts loop 1 at 8:00 PM
	LoopState.test_hold_clock = true
	LoopState.test_advance_to(HELD_CLOCK)
	slice.get_node("HUD").visible = false
	var hari: CharacterBody3D = slice.get_node("Hari")
	hari.position = HARI_UNDER_BULBS if lit else HARI_DARK_GATE
	hari.reset_physics_interpolation()
	slice.get_node("CameraRig").snap()

func _process(_delta: float) -> void:
	_frame += 1
	if _frame == TRIGGER_FRAME_FIRST or (retrigger and _frame == TRIGGER_FRAME_SECOND):
		_spawn_scuff()

func _spawn_scuff() -> void:
	var inst: Node3D = SCUFF.instantiate()
	for child in inst.get_children():
		(child as CPUParticles3D).use_fixed_seed = true
		(child as CPUParticles3D).seed = PREVIEW_SEED
	var hari: Node3D = slice.get_node("Hari")
	inst.position = Vector3(hari.global_position.x, 0.0, hari.global_position.z)
	slice.add_child(inst)
	for child in inst.get_children():
		(child as CPUParticles3D).emitting = true
