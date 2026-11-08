extends Node3D
## A6 Effect A frame-strip preview (CHANGE-BRIEF §E). Spawns a FootstepScuff instance at the
## planned Hari position, over the deck background the brief names, at the in-game deck camera
## preset (offset (0, 1.9, 4.5) from Hari, look (0, 1.25, 0), FOV 45°, from godot/scenes/camera_rig.gd).
## No gameplay wiring — the preview only triggers instances and reads the night exports on itself.

const SCUFF := preload("res://effects/footstep_scuff.tscn")
const HARI_DARK_GATE := Vector3(3.5, 0.0, 0.0)   # §0: dark stretch is x < 5
const HARI_UNDER_BULB := Vector3(12.0, 0.0, 0.0) # §0: a warm bulb sits at (12, 2.7, -2.4)
const BULB_LOCAL := Vector3(0.0, 2.7, -2.4)      # offset from Hari to the warm bulb, §0
const CAMERA_LOCAL := Vector3(0.0, 1.9, 4.5)     # deck preset offset from Hari
const CAMERA_LOOK_LOCAL := Vector3(0.0, 1.25, 0.0)
const TRIGGER_FRAME_FIRST := 10
const TRIGGER_FRAME_SECOND := 21                 # §E, 11 frames after the first (one real step at 30 FPS capture)

@export var lit: bool = false                    # false = dark gate, true = under the warm string light
@export var retrigger: bool = false              # on = spawn a second scuff at frame 21 while the first is still alive

@onready var camera: Camera3D = $Camera3D
@onready var bulb: OmniLight3D = $WarmBulb
@onready var spawn_marker: Marker3D = $SpawnMarker

var _frame: int = 0

func _ready() -> void:
	var hari := HARI_UNDER_BULB if lit else HARI_DARK_GATE
	spawn_marker.position = hari
	bulb.position = hari + BULB_LOCAL
	bulb.visible = lit
	camera.position = hari + CAMERA_LOCAL
	camera.look_at(hari + CAMERA_LOOK_LOCAL, Vector3.UP)

func _process(_delta: float) -> void:
	_frame += 1
	if _frame == TRIGGER_FRAME_FIRST:
		_spawn_scuff()
	elif retrigger and _frame == TRIGGER_FRAME_SECOND:
		_spawn_scuff()

func _spawn_scuff() -> void:
	var inst: Node3D = SCUFF.instantiate()
	inst.position = spawn_marker.position
	add_child(inst)
	for child in inst.get_children():
		(child as CPUParticles3D).emitting = true
