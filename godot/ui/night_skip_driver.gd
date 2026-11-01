extends Node
## Drives the night-skip glow (CHANGE-BRIEF.md §1.5) on its parent's ShaderMaterial.
## Reads LoopState, never writes it. Steps by delta, so the fades take the same game time at any
## frame rate and follow Engine.time_scale (R2, R3, R6). Pausable, so the value freezes while the
## tree is paused (R7). move_toward turns around from the current value on a re-press or an early
## release (R4, R5).

const FADE_IN := 0.25      ## s from 0 to 1
const FADE_OUT := 0.5      ## s from 1 to 0
const PARAM := &"skip_amount"

var skip_amount := 0.0
var _material: ShaderMaterial

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_PAUSABLE
	_material = (get_parent() as CanvasItem).material as ShaderMaterial
	_apply()

## The state the glow shows: the player is skipping the night (the HUD's own ">> x8" condition).
static func state_holds() -> bool:
	return LoopState.fast_forward and LoopState.phase == LoopState.Phase.NIGHT

func _process(delta: float) -> void:
	var target := 1.0 if state_holds() else 0.0
	var duration := FADE_IN if target > skip_amount else FADE_OUT
	skip_amount = move_toward(skip_amount, target, delta / duration)
	_apply()

func _apply() -> void:
	if _material:
		_material.set_shader_parameter(PARAM, skip_amount)

## Debug key F9 (debug builds only): the controlled-value captures for the A5 human check, in a real windowed run.
## Writes evidence/a5/debug-key/skip_<value>.png at viewport resolution; 2.0 answers the hint_range question.
const CAPTURE_KEY := KEY_F9
const CAPTURE_VALUES := [0.0, 0.5, 1.0, 2.0]

func _unhandled_input(event: InputEvent) -> void:
	var key := event as InputEventKey
	if OS.is_debug_build() and key and key.pressed and not key.echo and key.keycode == CAPTURE_KEY:
		_capture_all()

func _capture_all() -> void:
	var dir := ProjectSettings.globalize_path("res://").path_join("../evidence/a5/debug-key")
	DirAccess.make_dir_recursive_absolute(dir)
	for v: float in CAPTURE_VALUES:
		await capture(self, _material, PARAM, v, dir.path_join("skip_%s.png" % str(v).replace(".", "_")))
	print("F9 captures written to ", dir)

## The course's capture function, unchanged.
func capture(driver: Node, mat: ShaderMaterial, param: StringName, value: float, path: String) -> void:
	driver.set_process(false)  # also set_physics_process(false) if the driver writes there
	mat.set_shader_parameter(param, value)
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(path)
	driver.set_process(true)
