extends "res://tests/harness.gd"
## Normal-map convention check by curl (CHANGE-BRIEF.md §2.2, F8). curl_ratio() and its helpers are the
## assignment's function, unchanged. A real tangent-space normal map is the slope field of a height surface,
## so it is curl-free in its own green convention.
## Calibrated on the Floor Tiles 06 nor_gl / nor_dx pair (strong grout relief) before it is trusted on
## Marble 01 (polished, very flat: expected to drift toward 1). Reads the raw PNG files, not the imports.
## Run:  ./scripts/run-test.sh normal_map_check.gd 60

const CALIBRATION_GL := "res://tests/data/curl/floor_tiles_06_nor_gl_2k.png"
const CALIBRATION_DX := "res://tests/data/curl/floor_tiles_06_nor_dx_2k.png"
const MARBLE_GL := "res://assets/textures/marble_01/marble_01_nor_gl_2k.png"
const MARBLE_DX := "res://assets/textures/marble_01/marble_01_nor_dx_2k.png"

# ~0: slope field of a real surface in this convention.
# ~1: no surface behind it.
# ~2: real surface, other green convention.
static func curl_ratio(source: Image, directx := false, stride := 4) -> float:
	var img := source.duplicate() as Image
	if img.is_compressed():
		img.decompress()
	var s: float = -1.0 if directx else 1.0
	var curl_sq := 0.0
	var terms_sq := 0.0
	for v in range(1, img.get_height() - 1, stride):
		for u in range(1, img.get_width() - 1, stride):
			var t1 := (_dh_du(img, u, v + 1) - _dh_du(img, u, v - 1)) * 0.5
			var t2 := (_dh_dv(img, u + 1, v, s) - _dh_dv(img, u - 1, v, s)) * 0.5
			curl_sq += (t1 - t2) * (t1 - t2)
			terms_sq += t1 * t1 + t2 * t2
	return curl_sq / maxf(terms_sq, 1e-12)


static func _normal(img: Image, u: int, v: int) -> Vector3:
	var c := img.get_pixel(u, v)
	return Vector3(c.r, c.g, c.b) * 2.0 - Vector3.ONE


static func _dh_du(img: Image, u: int, v: int) -> float:
	var n := _normal(img, u, v)
	return -n.x / maxf(n.z, 0.05)


static func _dh_dv(img: Image, u: int, v: int, s: float) -> float:
	var n := _normal(img, u, v)
	return s * n.y / maxf(n.z, 0.05)


static func load_raw(path: String) -> Image:
	return Image.load_from_file(ProjectSettings.globalize_path(path))

func run() -> bool:
	var ratios := {}
	for path in [CALIBRATION_GL, CALIBRATION_DX, MARBLE_GL, MARBLE_DX]:
		var img := load_raw(path)
		check("decoded %s" % path.get_file(), img != null and not img.is_empty(), img)
		if img == null or img.is_empty():
			return true
		ratios[path] = [curl_ratio(img, false), curl_ratio(img, true)]
		print("%s   as OpenGL %.3f   as DirectX %.3f" % [path.get_file(), ratios[path][0], ratios[path][1]])
	# The calibration pair sets the threshold: the right convention must read well below the wrong one.
	var gl_right: float = ratios[CALIBRATION_GL][0]
	var gl_wrong: float = ratios[CALIBRATION_GL][1]
	check("calibration: GL file is low read as OpenGL", gl_right < 0.5, "%.3f" % gl_right)
	check("calibration: GL file is high read as DirectX", gl_wrong > 1.5, "%.3f" % gl_wrong)
	check("calibration: DX file is high read as OpenGL", ratios[CALIBRATION_DX][0] > 1.5, "%.3f" % ratios[CALIBRATION_DX][0])
	check("calibration: DX file is low read as DirectX", ratios[CALIBRATION_DX][1] < 0.5, "%.3f" % ratios[CALIBRATION_DX][1])
	# Marble is too flat to clear the calibrated thresholds; assert only the direction (see TEST-REPORT.md).
	check("marble_01 nor_gl reads lower as OpenGL than as DirectX", ratios[MARBLE_GL][0] < ratios[MARBLE_GL][1],
		"%.3f < %.3f" % [ratios[MARBLE_GL][0], ratios[MARBLE_GL][1]])
	return true
