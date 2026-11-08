## Writes the moth silhouette PNG used by Effect B's particles (CHANGE-BRIEF §B.3).
## Thin SceneTree entry point; the pixel formula lives in tools/moth_texture.gd so
## the same code can be run from a test harness when godot's CLI isn't available.
##   godot --headless --path godot -s res://tools/write_moth_texture.gd
extends SceneTree

const MT := preload("res://tools/moth_texture.gd")

func _initialize() -> void:
	var err := MT.save_all()
	print("wrote %s and %s: %dx%d (err %d)" % [MT.OUT_PNG, MT.OUT_TRES, MT.W, MT.H, err])
	quit(0 if err == OK else 1)
