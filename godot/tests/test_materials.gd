extends "res://tests/harness.gd"
## A5 materials audit (CHANGE-BRIEF.md §1.3, §2.1-2.5; see godot/MATERIALS.md).
## Headless-only: parses the shader source, loads every .tres through the resource loader, loads the slice and hint
## scenes, and asserts every row of MATERIALS.md. For each normal map it also reads the raw PNG bytes and prints
## curl_ratio under both conventions, using the course helper in godot/tests/normal_map_check.gd.
## Run:  ./scripts/run-test.sh test_materials.gd 60
## Headless draws nothing: this proves wiring, uniform contracts, texture paths and .import flags, never the look.

const NormalCheck = preload("res://tests/normal_map_check.gd")

const DECK_SHADER := "res://shaders/deck_marble.gdshader"
const HINT_SHADER := "res://shaders/hint_experiment.gdshader"
const NIGHT_SHADER := "res://shaders/night_skip.gdshader"

const MARBLE_DRY := "res://materials/marble_dry.tres"
const MARBLE_WET := "res://materials/marble_wet.tres"
const HINT_A := "res://materials/hint_a_source_color.tres"
const HINT_B := "res://materials/hint_b_no_hint.tres"
const NIGHT_MAT := "res://materials/night_skip.tres"

const DIFF := "res://assets/textures/marble_01/marble_01_diff_2k.png"
const ROUGH := "res://assets/textures/marble_01/marble_01_rough_2k.png"
const NOR_GL := "res://assets/textures/marble_01/marble_01_nor_gl_2k.png"
const NOR_DX := "res://assets/textures/marble_01/marble_01_nor_dx_2k.png"
const HINT_STRIP := "res://assets/textures/hint_strip_3x1.png"

## Each row: param -> [glsl_type, hint_text_in_source, default_in_source].
## Hint text is matched by substring so "source_color, filter_nearest" works regardless of surrounding whitespace.
const DECK_UNIFORMS := {
	"albedo_tex":       ["sampler2D", "source_color, filter_linear_mipmap, repeat_enable", ""],
	"albedo_tint":      ["vec4",      "source_color",                                      "vec4(1.0)"],
	"tile_size_m":      ["float",     "hint_range(0.25, 4.0)",                             "1.0"],
	"roughness_tex":    ["sampler2D", "filter_linear_mipmap, repeat_enable",               ""],
	"normal_tex":       ["sampler2D", "hint_normal, filter_linear_mipmap, repeat_enable",  ""],
	"roughness_scale":  ["float",     "hint_range(0.0, 2.0)",                              "1.0"],
	"specular_amount":  ["float",     "hint_range(0.0, 1.0)",                              "0.5"],
	"normal_depth":     ["float",     "hint_range(0.0, 2.0)",                              "1.0"],
}
const HINT_UNIFORMS := {
	"strip_as_colour":    ["sampler2D", "source_color, filter_nearest", ""],
	"strip_as_data":      ["sampler2D", "filter_nearest",               ""],
	"use_source_color":   ["bool",      "",                             "false"],
}
const NIGHT_UNIFORMS := {
	"skip_amount":    ["float", "hint_range(0.0, 1.0)",             "0.0"],
	"skip_tint":      ["vec4",  "source_color",                     "vec4(1.0, 0.6, 0.2, 1.0)"],
	"tint_strength": ["float", "hint_range(0.0, 1.0)",              "0.5"],
}

## get_shader_uniform_list() returns these Variant types for each uniform.
const UNIFORM_LIST_TYPES := {
	# deck_marble
	"albedo_tex":        TYPE_OBJECT,  # sampler2D exposed as Texture
	"albedo_tint":       TYPE_COLOR,
	"tile_size_m":       TYPE_FLOAT,
	"roughness_tex":     TYPE_OBJECT,
	"normal_tex":        TYPE_OBJECT,
	"roughness_scale":   TYPE_FLOAT,
	"specular_amount":   TYPE_FLOAT,
	"normal_depth":      TYPE_FLOAT,
	# hint_experiment
	"strip_as_colour":   TYPE_OBJECT,
	"strip_as_data":     TYPE_OBJECT,
	"use_source_color":  TYPE_BOOL,
	# night_skip
	"skip_amount":       TYPE_FLOAT,
	"skip_tint":         TYPE_COLOR,
	"tint_strength":     TYPE_FLOAT,
}

## .import rows read from the .import file; mode and mipmap flags from CHANGE-BRIEF.md §2.2, §2.5.
const IMPORT_EXPECTED := {
	DIFF:       {"compress/mode": 2, "compress/normal_map": 2, "mipmaps/generate": true,  "detect_3d/compress_to": 0},
	ROUGH:      {"compress/mode": 2, "compress/normal_map": 2, "mipmaps/generate": true,  "detect_3d/compress_to": 0},
	NOR_GL:     {"compress/mode": 2, "compress/normal_map": 1, "mipmaps/generate": true,  "detect_3d/compress_to": 0},
	NOR_DX:     {"compress/mode": 0, "compress/normal_map": 2, "mipmaps/generate": false, "detect_3d/compress_to": 0},
	HINT_STRIP: {"compress/mode": 0, "compress/normal_map": 2, "mipmaps/generate": false, "detect_3d/compress_to": 0},
}

## Review fix: the imported format, measured with get_image().get_format() on this machine (macOS, desktop import).
## It confirms the enums above: compress/mode 2 gives a VRAM format, normal_map 1 gives the two-channel normal format,
## and compress/mode 0 stays uncompressed RGB8.
const FORMAT_EXPECTED := {
	DIFF:       Image.FORMAT_DXT1,
	ROUGH:      Image.FORMAT_DXT1,
	NOR_GL:     Image.FORMAT_RGTC_RG,
	NOR_DX:     Image.FORMAT_RGB8,
	HINT_STRIP: Image.FORMAT_RGB8,
}

func run() -> bool:
	check_shader_source(DECK_SHADER, DECK_UNIFORMS)
	check_shader_source(HINT_SHADER, HINT_UNIFORMS)
	check_shader_source(NIGHT_SHADER, NIGHT_UNIFORMS)

	check_uniform_list(DECK_SHADER, DECK_UNIFORMS.keys())
	check_uniform_list(HINT_SHADER, HINT_UNIFORMS.keys())
	check_uniform_list(NIGHT_SHADER, NIGHT_UNIFORMS.keys())

	check_marble_material(MARBLE_DRY, "dry", {})
	check_marble_material(MARBLE_WET, "wet", {"roughness_scale": 0.3, "specular_amount": 0.8})
	check_hint_material(HINT_A, true)
	check_hint_material(HINT_B, false)
	check_night_material()

	for path in IMPORT_EXPECTED:
		check_import(path, IMPORT_EXPECTED[path])
	for path in FORMAT_EXPECTED:
		check_format(path, FORMAT_EXPECTED[path])

	await check_scene_wiring()

	curl_report("marble_01_nor_gl", NOR_GL)
	curl_report("marble_01_nor_dx", NOR_DX)
	return true

# ---- shader source and uniform list ----------------------------------------------------------------

func read_source(path: String) -> String:
	var src := FileAccess.get_file_as_string(path)
	check("shader source readable: %s" % path.get_file(), src != "", path)
	return src

func check_shader_source(path: String, expected: Dictionary) -> void:
	var src := read_source(path)
	if src == "":
		return
	# Match `uniform <type> <name> [: <hints>] [= <default>];`
	var re := RegEx.create_from_string(
		"uniform\\s+(\\w+)\\s+(\\w+)\\s*(?::\\s*([^=;]+?)\\s*)?(?:=\\s*([^;]+?)\\s*)?;")
	var declared := {}
	for m in re.search_all(src):
		declared[m.get_string(2)] = [m.get_string(1), m.get_string(3), m.get_string(4)]
	for name in expected:
		var want: Array = expected[name]
		var got: Array = declared.get(name, [])
		var ok_type: bool = got.size() == 3 and got[0] == want[0]
		var ok_hint: bool = got.size() == 3 and (want[1] == "" or (got[1] as String).find(want[1]) != -1)
		var ok_def: bool = got.size() == 3 and (want[2] == "" or (got[2] as String).strip_edges() == want[2])
		check("source %s: %s %s declared" % [path.get_file(), want[0], name], ok_type, got)
		check("source %s: %s hints contain '%s'" % [path.get_file(), name, want[1]], ok_hint, got)
		check("source %s: %s default = %s" % [path.get_file(), name, want[2]], ok_def, got)
		# Review fix: "hints contain" is a substring match, so a data sampler that gained source_color (F6) still
		# passed it. A sampler whose expected hints lack source_color must not have it.
		if want[0] == "sampler2D" and not (want[1] as String).contains("source_color"):
			check("source %s: data sampler %s has no source_color" % [path.get_file(), name],
				got.size() == 3 and not (got[1] as String).contains("source_color"), got)

func check_uniform_list(path: String, names: Array) -> void:
	var sh: Shader = load(path)
	check("shader loads: %s" % path.get_file(), sh != null, sh)
	if sh == null:
		return
	var listed := {}
	for u in sh.get_shader_uniform_list():
		listed[u.name] = u.type
	# An empty list means the shader failed to parse; check this before per-name checks.
	check("%s uniform list is non-empty (parses)" % path.get_file(), listed.size() >= names.size(), listed)
	for name in names:
		var want: int = UNIFORM_LIST_TYPES[name]
		check("%s uniform list: %s is %s" % [path.get_file(), name, type_string(want)],
			listed.get(name, -1) == want, type_string(listed.get(name, TYPE_NIL)))

# ---- material resources ----------------------------------------------------------------------------

func check_marble_material(path: String, kind: String, overrides: Dictionary) -> void:
	var mat: ShaderMaterial = load(path)
	check("material loads: %s" % path.get_file(), mat != null, mat)
	if mat == null:
		return
	check("%s uses deck_marble.gdshader" % path.get_file(),
		mat.shader != null and mat.shader.resource_path == DECK_SHADER, mat.shader)
	# Textures: three samplers, bound to the three Marble 01 files, never to the DX normal.
	_check_texture_param(mat, &"albedo_tex", DIFF, path)
	_check_texture_param(mat, &"roughness_tex", ROUGH, path)
	_check_texture_param(mat, &"normal_tex", NOR_GL, path)
	# Overridden scalar uniforms (whatever's in the dict); everything else must stay unset so the shader defaults apply.
	var defaults := {"roughness_scale": 1.0, "specular_amount": 0.5, "normal_depth": 1.0, "tile_size_m": 1.0}
	for p in defaults:
		var set_value: Variant = mat.get_shader_parameter(p)
		if overrides.has(p):
			check("%s overrides %s = %s" % [path.get_file(), p, overrides[p]],
				set_value != null and is_equal_approx(float(set_value), overrides[p]), set_value)
		else:
			check("%s does not override %s (shader default %s applies)" % [path.get_file(), p, defaults[p]],
				set_value == null, set_value)
	# Guard: no DX normal must be bound anywhere on this material.
	for name in [&"albedo_tex", &"roughness_tex", &"normal_tex"]:
		var tex: Texture2D = mat.get_shader_parameter(name)
		if tex == null:
			continue
		check("%s %s is not the DX normal" % [path.get_file(), name],
			tex.resource_path != NOR_DX, tex.resource_path)

func check_hint_material(path: String, expected_bool: bool) -> void:
	var mat: ShaderMaterial = load(path)
	check("material loads: %s" % path.get_file(), mat != null, mat)
	if mat == null:
		return
	check("%s uses hint_experiment.gdshader" % path.get_file(),
		mat.shader != null and mat.shader.resource_path == HINT_SHADER, mat.shader)
	_check_texture_param(mat, &"strip_as_colour", HINT_STRIP, path)
	_check_texture_param(mat, &"strip_as_data", HINT_STRIP, path)
	var b: Variant = mat.get_shader_parameter(&"use_source_color")
	check("%s use_source_color = %s" % [path.get_file(), expected_bool],
		b != null and bool(b) == expected_bool, b)

func check_night_material() -> void:
	var mat: ShaderMaterial = load(NIGHT_MAT)
	check("material loads: %s" % NIGHT_MAT.get_file(), mat != null, mat)
	if mat == null:
		return
	check("%s uses night_skip.gdshader" % NIGHT_MAT.get_file(),
		mat.shader != null and mat.shader.resource_path == NIGHT_SHADER, mat.shader)
	# Night-skip material must not override any uniform; the three defaults live in the shader source.
	for p in NIGHT_UNIFORMS:
		var set_value: Variant = mat.get_shader_parameter(p)
		check("%s does not override %s (driver/material defaults apply)" % [NIGHT_MAT.get_file(), p],
			set_value == null, set_value)

func _check_texture_param(mat: ShaderMaterial, param: StringName, want: String, mat_path: String) -> void:
	var tex: Texture2D = mat.get_shader_parameter(param)
	check("%s binds %s to %s" % [mat_path.get_file(), param, want.get_file()],
		tex != null and tex.resource_path == want, tex.resource_path if tex else "null")

# ---- .import files ---------------------------------------------------------------------------------

func check_import(path: String, want: Dictionary) -> void:
	var cfg := ConfigFile.new()
	var err := cfg.load(path + ".import")
	check("import readable: %s.import" % path.get_file(), err == OK, err)
	if err != OK:
		return
	for key in want:
		var got: Variant = cfg.get_value("params", key, null)
		check("%s params/%s = %s" % [path.get_file(), key, want[key]],
			got == want[key], got)

func check_format(path: String, want: int) -> void:
	var tex: Texture2D = load(path)
	var img := tex.get_image() if tex else null
	check("%s imported format is %d" % [path.get_file(), want], img != null and img.get_format() == want,
		img.get_format() if img else "null")

# ---- scene wiring (headless instantiation) --------------------------------------------------------

func check_scene_wiring() -> void:
	# Slice: FloorWest/East/Front use marble_dry; FloorBack uses marble_wet.
	var slice: Node = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	await steps(2)
	for name in ["FloorWest", "FloorEast", "FloorFront"]:
		var mi: MeshInstance3D = slice.get_node("Deck/" + name)
		var m: Material = mi.material_override
		check("Deck/%s material_override is marble_dry.tres" % name,
			m != null and m.resource_path == MARBLE_DRY, m.resource_path if m else "null")
	var back: MeshInstance3D = slice.get_node("Deck/FloorBack")
	var back_m: Material = back.material_override
	check("Deck/FloorBack material_override is marble_wet.tres",
		back_m != null and back_m.resource_path == MARBLE_WET,
		back_m.resource_path if back_m else "null")
	# Night-skip material lives on HUD/StatusBar.
	var bar := slice.get_node("HUD/StatusBar") as Control
	check("HUD/StatusBar material is night_skip.tres",
		bar != null and bar.material != null and bar.material.resource_path == NIGHT_MAT,
		bar.material.resource_path if (bar and bar.material) else "null")
	# Review fix: MATERIALS.md §4 states the slice lighting the marble is judged under; pin it.
	var slice_env := (slice.get_node("WorldEnvironment") as WorldEnvironment).environment
	check("slice env tonemap_mode = 2 (Filmic)", slice_env.tonemap_mode == Environment.TONE_MAPPER_FILMIC, slice_env.tonemap_mode)
	check("slice env glow_enabled = true", slice_env.glow_enabled, slice_env.glow_enabled)
	check("slice env fog_enabled = true (not in brief §2.1)", slice_env.fog_enabled, slice_env.fog_enabled)
	slice.queue_free()
	await steps(2)

	# Hint-experiment: QuadA uses hint_a, QuadB uses hint_b; env is Linear, exposure 1.0, glow off.
	var hint: Node = load("res://scenes/hint_experiment.tscn").instantiate()
	root.add_child(hint)
	await steps(2)
	var qa := hint.get_node("QuadA") as MeshInstance3D
	var qb := hint.get_node("QuadB") as MeshInstance3D
	check("QuadA material_override is hint_a_source_color.tres",
		qa.material_override != null and qa.material_override.resource_path == HINT_A,
		qa.material_override.resource_path if qa.material_override else "null")
	check("QuadB material_override is hint_b_no_hint.tres",
		qb.material_override != null and qb.material_override.resource_path == HINT_B,
		qb.material_override.resource_path if qb.material_override else "null")
	var env := (hint.get_node("WorldEnvironment") as WorldEnvironment).environment
	check("hint env tonemap_mode = 0 (Linear)", env.tonemap_mode == 0, env.tonemap_mode)
	check("hint env tonemap_exposure = 1.0", is_equal_approx(env.tonemap_exposure, 1.0), env.tonemap_exposure)
	check("hint env glow_enabled = false", not env.glow_enabled, env.glow_enabled)
	check("hint env fog_enabled = false", not env.fog_enabled, env.fog_enabled)
	check("hint env adjustment_enabled = false", not env.adjustment_enabled, env.adjustment_enabled)
	hint.queue_free()
	await steps(2)

# ---- normal-map convention report (course helper) --------------------------------------------------

func curl_report(label: String, path: String) -> void:
	var img := NormalCheck.load_raw(path)
	check("decoded %s" % label, img != null and not img.is_empty(), img)
	if img == null or img.is_empty():
		return
	var gl := NormalCheck.curl_ratio(img, false)
	var dx := NormalCheck.curl_ratio(img, true)
	print("%s   as OpenGL %.3f   as DirectX %.3f" % [label, gl, dx])
	# Non-asserted print, as in normal_map_check.gd: Marble 01 is polished and drifts toward 1.
	# The convention direction is already asserted by normal_map_check.gd; this report is for the reader.
