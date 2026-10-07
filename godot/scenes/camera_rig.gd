extends Node3D
## Telltale-style follow camera: damped follow of Hari with per-zone framing presets
## blended smoothly by Hari's x. Presets are data: offset from Hari, look-at offset, FOV.

const PRESETS := {
	"gate": {"offset": Vector3(2.4, 2.0, 3.1), "look": Vector3(-0.6, 1.1, -1.8), "fov": 54.0},     # on the deck, looking at the SUV and villa (playtest 3: the old preset sat off the deck and framed the wall)
	"deck": {"offset": Vector3(0.0, 1.9, 4.5), "look": Vector3(0.0, 1.25, 0.0), "fov": 45.0},      # medium
	"railing": {"offset": Vector3(-2.6, 1.8, -2.6), "look": Vector3(2.6, 1.0, 3.2), "fov": 50.0},  # swings past Hari to the sea
}
const GATE_END_X := 5.0
const RAILING_START_X := 20.0
const BLEND_HALF_WIDTH := 1.5           ## m either side of a zone boundary
const FOLLOW_SHARPNESS := 4.5           ## higher = snappier damping
const CAMERA_Z_RANGE := Vector2(-5.5, 9.0)

@export var target_path: NodePath
var target: Node3D
var shake := 0.0                         ## seconds of shake left
var _look := Vector3.ZERO
@onready var camera: Camera3D = $Camera

func _ready() -> void:
	target = get_node(target_path)
	snap()

## Blend weights for the three presets at x.
static func zone_weights(x: float) -> Dictionary:
	var to_deck := smoothstep(GATE_END_X - BLEND_HALF_WIDTH, GATE_END_X + BLEND_HALF_WIDTH, x)
	var to_rail := smoothstep(RAILING_START_X - BLEND_HALF_WIDTH, RAILING_START_X + BLEND_HALF_WIDTH, x)
	return {"gate": 1.0 - to_deck, "deck": to_deck * (1.0 - to_rail), "railing": to_rail}

func _target_pos() -> Vector3:
	return target.get_global_transform_interpolated().origin   # physics interpolation: smooth at any display rate

func desired() -> Array:
	var tp := _target_pos()
	var weights := zone_weights(tp.x)
	var offset := Vector3.ZERO
	var look := Vector3.ZERO
	var fov := 0.0
	for zone in weights:
		offset += PRESETS[zone].offset * weights[zone]
		look += PRESETS[zone].look * weights[zone]
		fov += PRESETS[zone].fov * weights[zone]
	var pos: Vector3 = tp + offset
	pos.z = clampf(pos.z, CAMERA_Z_RANGE.x, CAMERA_Z_RANGE.y)
	return [pos, tp + look, fov]

func snap() -> void:
	var d := desired()
	camera.global_position = d[0]
	_look = d[1]
	camera.fov = d[2]
	camera.look_at(_look)

func _process(delta: float) -> void:
	var d := desired()
	var k := 1.0 - exp(-FOLLOW_SHARPNESS * delta)
	camera.global_position = camera.global_position.lerp(d[0], k)
	_look = _look.lerp(d[1], k)
	camera.fov = lerpf(camera.fov, d[2], k)
	camera.look_at(_look)
	shake = maxf(shake - delta, 0.0)
	if shake > 0.0:
		var a := 0.08 * shake
		camera.global_position += Vector3(randf_range(-a, a), randf_range(-a, a), 0.0)
