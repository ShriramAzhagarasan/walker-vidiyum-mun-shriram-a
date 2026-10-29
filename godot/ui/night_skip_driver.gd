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
