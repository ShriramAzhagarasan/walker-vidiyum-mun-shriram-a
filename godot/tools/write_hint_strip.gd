## Writes the hint-experiment texture (CHANGE-BRIEF.md §2.5): a 3×1 PNG of greys 64, 128, 192.
## Imported Lossless with no mipmaps, so the shader samples exactly these bytes.
##   godot --headless --path godot -s res://tools/write_hint_strip.gd
extends SceneTree

const OUT := "res://assets/textures/hint_strip_3x1.png"
const GREYS := [64, 128, 192]

func _initialize() -> void:
	var img := Image.create(GREYS.size(), 1, false, Image.FORMAT_RGB8)
	for x in GREYS.size():
		img.set_pixel(x, 0, Color8(GREYS[x], GREYS[x], GREYS[x]))
	var err := img.save_png(OUT)
	var back := Image.load_from_file(ProjectSettings.globalize_path(OUT))
	var read := []
	for x in back.get_width():
		read.append(back.get_pixel(x, 0).r8)
	print("wrote %s: %s (err %d), read back %s" % [OUT, GREYS, err, read])
	quit(0 if err == OK and read == GREYS else 1)
