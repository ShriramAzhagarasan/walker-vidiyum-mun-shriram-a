extends RefCounted
## The one "load texture or fall back to a placeholder" helper for all 3D art.
## load_texture() returns the PNG if present (imported, or raw and just dropped in), else null.
## placeholder() paints a simple stand-in Image in code, keyed by kind/variant.

const HARI_BANDS := {
	"idle": Color("8fa3bf"), "walk": Color("5fbf74"), "talk": Color("f2d24b"), "phone": Color("4cc9e0"),
	"startled": Color("e5484d"), "whiteout": Color("ffffff"), "relief": Color("ff9f43"), "keys": Color("d4a017"),
	"notes": Color("b07cff"), "overhear": Color("2f6fdb"),
}

static func load_texture(path: String) -> Texture2D:
	if path.is_empty():
		return null
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	if FileAccess.file_exists(path):          # dropped in but not imported yet
		var image := Image.load_from_file(path)
		if image:
			return ImageTexture.create_from_image(image)
	return null

static func texture_or_placeholder(path: String, kind: String, variant := "") -> Texture2D:
	var tex := load_texture(path)
	return tex if tex else ImageTexture.create_from_image(placeholder(kind, variant))

## Unshaded material for cel art (keeps its colours), alpha-scissored so depth sorting works.
static func cel_material(tex: Texture2D, tint := Color.WHITE) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_texture = tex
	m.albedo_color = tint
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
	m.alpha_scissor_threshold = 0.5
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m

static func lit_material(color: Color, emission := 0.0, emission_color := Color.BLACK) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	if emission > 0.0:
		m.emission_enabled = true
		m.emission = emission_color
		m.emission_energy_multiplier = emission
	return m

# --- placeholder images --------------------------------------------------------------

static func placeholder(kind: String, variant := "") -> Image:
	match kind:
		"hari": return _figure(Color("e8e2d0"), Color("3a4660"), variant, HARI_BANDS.get(variant, Color.GRAY))
		"manikandan": return _figure(Color("f1efe6"), Color("3b3a45"), "phone" if variant == "phone" else "idle", Color("c9c4b0"), true)
		"advay": return _figure(Color("d63384"), Color("2b4a7a"), "idle", Color("ffd23f"), false, true)
		"krishna": return _figure(Color("2a9d8f"), Color("e9e2cf"), "idle", Color("1d6f65"))
		"keys": return _keys()
		"beach": return _beach()
		"fire": return _fire()
	var img := Image.create(8, 8, false, Image.FORMAT_RGBA8)
	img.fill(Color.MAGENTA)
	return img

static func _figure(shirt: Color, pants: Color, pose: String, band: Color, moustache := false, speaker := false) -> Image:
	var w := 96
	var h := 216
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var white := pose == "whiteout"
	var skin := Color("e9e4ea") if white else Color("a8714a")
	if white:
		shirt = Color("fbfbff")
		pants = Color("d9dbe6")
	var cx := w / 2
	var spread := 10 if pose == "walk" else 4
	_line(img, Vector2(cx - 7, 120), Vector2(cx - 7 - spread, h - 2), 7, pants)
	_line(img, Vector2(cx + 7, 120), Vector2(cx + 7 + spread, h - 2), 7, pants)
	img.fill_rect(Rect2i(cx - 22, 48, 44, 78), shirt)
	img.fill_rect(Rect2i(cx - 22, 88, 44, 12), band)
	if speaker:
		for i in 5:
			_disc(img, Vector2(cx - 12 + (i % 3) * 12, 60 + i * 12), 3, Color("ffd23f"))
	var sr := Vector2(cx + 18, 54)
	var sl := Vector2(cx - 18, 54)
	match pose:
		"phone":
			_line(img, sr, Vector2(cx + 26, 30), 4, skin)
			img.fill_rect(Rect2i(cx + 20, 16, 9, 16), Color("20232b"))
			_line(img, sl, Vector2(cx - 24, 108), 4, skin)
		"startled":
			_line(img, sr, Vector2(cx + 40, 14), 4, skin)
			_line(img, sl, Vector2(cx - 40, 14), 4, skin)
		"talk":
			_line(img, sr, Vector2(cx + 44, 72), 4, skin)
			_line(img, sl, Vector2(cx - 24, 108), 4, skin)
		"keys":
			_line(img, sr, Vector2(cx + 44, 80), 4, skin)
			_disc(img, Vector2(cx + 44, 84), 6, Color("f5c542"))
			_line(img, sl, Vector2(cx - 24, 108), 4, skin)
		"relief":
			_line(img, sr, Vector2(cx + 30, 112), 4, skin)
			_line(img, sl, Vector2(cx - 30, 112), 4, skin)
		"notes":   # head down, both hands holding the phone at chest
			_line(img, sr, Vector2(cx + 6, 70), 4, skin)
			_line(img, sl, Vector2(cx - 6, 70), 4, skin)
			img.fill_rect(Rect2i(cx - 8, 60, 16, 12), Color("20232b"))
		"overhear":   # hand half-raised, listening
			_line(img, sr, Vector2(cx + 34, 44), 4, skin)
			_line(img, sl, Vector2(cx - 24, 108), 4, skin)
		_:
			_line(img, sr, Vector2(cx + 24, 108), 4, skin)
			_line(img, sl, Vector2(cx - 24, 108), 4, skin)
	if speaker:
		img.fill_rect(Rect2i(cx + 22, 96, 24, 14), Color("111827"))
	var head := Vector2(cx + (-6 if pose == "overhear" else 0), 32 if pose == "notes" else 26)   # notes: head down; overhear: head turned back
	_disc(img, head, 19, skin)
	img.fill_rect(Rect2i(cx - 19, 6, 38, 10), Color("cfcfd8") if white else Color("1b1716"))
	_disc(img, head + Vector2(9, -1), 4 if pose == "startled" else 2, Color("15121a"))
	if moustache:
		img.fill_rect(Rect2i(cx - 2, 33, 14, 3), Color("17130f"))
	if speaker:
		img.fill_rect(Rect2i(cx - 4, 21, 20, 6), Color("0b0b0f"))
	return img

static func _keys() -> Image:
	var img := Image.create(32, 32, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var gold := Color("f5c542")
	_disc(img, Vector2(11, 11), 8, gold)
	_disc(img, Vector2(11, 11), 4, Color(0, 0, 0, 0))
	_line(img, Vector2(15, 15), Vector2(28, 28), 3, gold)
	_line(img, Vector2(24, 24), Vector2(20, 29), 2, gold)
	return img

## Beach view seen past the railing: sea, village boats, old fence, rock shrine. Sky is transparent.
## Seen from the deck the image's LEFT edge is toward +x, so the village side (with the fire
## overlay) is on the left; the rock shrine is toward the middle.
static func _beach() -> Image:
	var w := 1024
	var h := 384
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	img.fill_rect(Rect2i(0, 180, w, 110), Color("24366b"))            # sea
	img.fill_rect(Rect2i(0, 180, w, 2), Color("6f86c9"))
	for i in 10:
		img.fill_rect(Rect2i((i * 97) % 700, 196 + i * 9, 300, 1), Color(0.6, 0.7, 1, 0.5))
	img.fill_rect(Rect2i(0, 290, w, 94), Color("6b5b6e"))             # sand
	for p in [Vector2(120, 186), Vector2(470, 188), Vector2(880, 186)]:
		_disc(img, p, 2, Color("ffd36b"))                            # boat lights at sea
	for i in 4:                                                      # village huts
		var hx := 90 + i * 70
		img.fill_rect(Rect2i(hx, 262, 50, 36), Color("8b6f55"))
		for k in 16:
			img.fill_rect(Rect2i(hx - 8 + k * 2, 262 - k, 66 - k * 4, 2), Color("b59a5e"))
	for bx in [120, 400]:                                            # catamarans on the sand
		img.fill_rect(Rect2i(bx, 318, 90, 10), Color("3f6fa0"))
		img.fill_rect(Rect2i(bx + 44, 282, 3, 36), Color("6b5a45"))
	_disc(img, Vector2(330, 332), 10, Color("ff8c2b"))               # small bonfire
	for i in 12:                                                     # old fence
		img.fill_rect(Rect2i(440 + i * 22, 270 + (i % 3) * 2, 4, 40), Color("8a7a66"))
	img.fill_rect(Rect2i(440, 282, 260, 2), Color("a89a88"))
	_disc(img, Vector2(780, 300), 56, Color("575866"))                # rock with a small shrine
	img.fill_rect(Rect2i(766, 210, 28, 30), Color("efe6d8"))
	_line(img, Vector2(760, 210), Vector2(780, 192), 3, Color("c0392b"))
	_line(img, Vector2(780, 192), Vector2(800, 210), 3, Color("c0392b"))
	return img

static func _fire() -> Image:
	var img := Image.create(256, 256, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for i in 6:
		_disc(img, Vector2(128, 170), 120 - i * 18, Color(1, 0.45 + i * 0.07, 0.1, 0.55 + i * 0.07))
	return img

static func _disc(img: Image, c: Vector2, r: int, color: Color) -> void:
	for y in range(-r, r + 1):
		for x in range(-r, r + 1):
			if x * x + y * y <= r * r:
				var p := Vector2i(int(c.x) + x, int(c.y) + y)
				if p.x >= 0 and p.y >= 0 and p.x < img.get_width() and p.y < img.get_height():
					img.set_pixelv(p, color)

static func _line(img: Image, a: Vector2, b: Vector2, half_width: int, color: Color) -> void:
	var n := int(a.distance_to(b)) + 1
	for i in n + 1:
		_disc(img, a.lerp(b, float(i) / n), half_width, color)
