extends "res://tests/harness.gd"
## Fresh-copy asset check: every generated asset the slice uses is present, loads, and has the
## expected shape (sprites with alpha and feet on the bottom edge, looping-ready OGG music, short SFX).
## If any file is missing, the game silently falls back to a placeholder or silence, so this
## test is what proves the submitted copy really shows and plays the generated assets.

const HARI_STATES := ["idle", "walk", "talk", "phone", "notes", "overhear", "startled", "keys", "whiteout", "relief"]
const NPCS := ["manikandan", "manikandan_phone", "advay", "krishna"]
const ENV := ["marble", "villa", "beach_backdrop", "fire_glow", "suv"]
const SFX := ["phone_buzz", "clue_saved", "keys_exchanged", "dawn_crash", "safe_dawn"]
const MUSIC := ["party_loop", "gaana_loop"]

func _sprite_ok(path: String) -> void:
	var tex := load(path) as Texture2D
	check("loads " + path, tex != null)
	if tex == null:
		return
	var img := tex.get_image()
	if img.is_compressed():
		img.decompress()
	var w := img.get_width()
	var h := img.get_height()
	check("  alpha channel " + path.get_file(), img.detect_alpha() != Image.ALPHA_NONE, img.get_format())
	check("  transparent corner " + path.get_file(), img.get_pixel(0, 0).a < 0.05, img.get_pixel(0, 0))
	var bottom_hit := false
	for y in range(h - 1, h - 12, -1):
		for x in range(0, w, 2):
			if img.get_pixel(x, y).a > 0.5:
				bottom_hit = true
				break
		if bottom_hit:
			break
	check("  feet within 12 px of the bottom edge " + path.get_file(), bottom_hit, "%dx%d" % [w, h])

func run() -> bool:
	for s in HARI_STATES:
		_sprite_ok("res://assets/art/hari/%s.png" % s)
	for n in NPCS:
		_sprite_ok("res://assets/art/npc/%s.png" % n)
	for e in ENV:
		var tex := load("res://assets/art/env/%s.png" % e) as Texture2D
		check("loads env " + e, tex != null and tex.get_width() >= 512, tex.get_size() if tex else null)
	for s in SFX:
		var st := load("res://assets/audio/sfx/%s.ogg" % s) as AudioStream
		check("loads sfx " + s, st != null and st.get_length() > 0.2 and st.get_length() <= 4.0, st.get_length() if st else null)
	for m in MUSIC:
		var st := load("res://assets/audio/music/%s.ogg" % m) as AudioStream
		check("loads music " + m, st != null and st.get_length() > 8.0, st.get_length() if st else null)
	return true
