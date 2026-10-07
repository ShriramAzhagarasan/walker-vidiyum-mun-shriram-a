extends Node3D
## 2.5D presentation of the slice. Shows LoopState/Story through their signals and queries,
## and feeds back only the thin interface: Story.player_x (from Hari), Story.nearby_target.
## Swapping this scene for another presentation leaves the logic and tests untouched.

const Spec = preload("res://logic/hari_spec.gd")
const StoryData = preload("res://logic/story_data.gd")
const HariBody = preload("res://scenes/hari.gd")
const CameraRig = preload("res://scenes/camera_rig.gd")
const Surface = preload("res://scenes/textured_surface.gd")
const Billboard = preload("res://scenes/billboard_art.gd")
const ScreenCards = preload("res://ui/screen_cards.gd")
const NotesToast = preload("res://ui/notes_toast.gd")
const Whiteout = preload("res://ui/whiteout.gd")

const HARI_START := Vector3(7.5, 0, 1.0)
const ADVAY_AT_CAR := Vector3(5.6, 0, 0.3)
const ADVAY_ON_DECK := Vector3(12.0, 0, 2.2)
const ADVAY_LEAVES_CAR_AFTER := 12.0       ## game minutes after 1:40
const KEYS_MOVE_SECONDS := 0.6
const CRASH_FLASH_SECONDS := 1.4
const CRASH_WHITE_SECONDS := 1.2
# Clock colour stops: [minutes, sky top, sky horizon, ambient, light colour, light energy].
const SKY_KEYS := [
	[1200.0, Color("1d1b4f"), Color("4a3f86"), Color("2a2850"), Color("8fa0ff"), 0.35],
	[1290.0, Color("0b0a2a"), Color("1d2055"), Color("1b1a3c"), Color("7f8fe0"), 0.25],
	[1680.0, Color("0b0a2a"), Color("1d2055"), Color("1b1a3c"), Color("7f8fe0"), 0.25],
	[1740.0, Color("23235e"), Color("6b4a7d"), Color("3a3058"), Color("b090c0"), 0.3],
	[1775.0, Color("5a4a8a"), Color("e0897a"), Color("6a4c62"), Color("ffb090"), 0.5],
	[1795.0, Color("e98f9a"), Color("ffc477"), Color("a07068"), Color("ffc890"), 0.8],
]
const SUNRISE := [Color("ffb38a"), Color("ffe6a8"), Color("c09080"), Color("fff0d0"), 1.4]

@onready var env: Environment = $WorldEnvironment.environment
@onready var sky_light: DirectionalLight3D = $SkyLight
@onready var hari: HariBody = $Hari
@onready var rig: CameraRig = $CameraRig
@onready var manikandan: Node3D = $Manikandan
@onready var advay: Node3D = $Advay
@onready var krishna: Node3D = $Krishna
@onready var keys_icon: Node3D = $KeysIcon
@onready var suv: Node3D = $SUV
@onready var headlights: SpotLight3D = $SUV/Headlights
@onready var manikandan_sprite: Billboard = $Manikandan/Sprite
@onready var beach: Surface = $Backdrops/BeachBackdrop
@onready var fire_glow: Surface = $Backdrops/FireGlow
@onready var fire_light: OmniLight3D = $Backdrops/FireLight
@onready var toast: NotesToast = $HUD/NotesToast
@onready var cards: ScreenCards = $HUD/ScreenCards
@onready var whiteout: Whiteout = $HUD/Whiteout

var sunrise := 0.0
var _keys_path: Array[String] = []
var _keys_from := Vector3.ZERO
var _keys_t := 0.0
var _lit_key := Vector2(-1, -1)

func _ready() -> void:
	hari.camera = rig.camera
	LoopState.loop_started.connect(_on_loop_started)
	LoopState.phone_buzz.connect(cards.show_phone)                       # visual twin: incoming-call card
	LoopState.clue_saved.connect(_on_clue_saved)
	LoopState.keys_exchanged.connect(_on_keys_exchanged)
	LoopState.advay_arrived.connect(_on_advay_arrived)
	LoopState.dawn_crash.connect(_on_dawn_crash)
	LoopState.safe_dawn.connect(_on_safe_dawn)
	LoopState.slice_ended.connect(cards.show_end_card.bind(true))
	LoopState.pause_changed.connect(cards.set_paused)
	Story.dialogue_closed.connect(_on_dialogue_closed)
	LoopState.begin_slice()

func _process(delta: float) -> void:
	Story.nearby_target = _nearest_interactable()
	_update_npcs(delta)
	_update_keys_icon(delta)
	_update_lighting()

func _nearest_interactable() -> String:
	var best := ""
	var best_d := Spec.INTERACT_RANGE
	for npc in [manikandan, krishna]:
		var d := Vector2(npc.global_position.x - hari.global_position.x, npc.global_position.z - hari.global_position.z).length()
		if npc.visible and d <= best_d:
			best_d = d
			best = npc.name.to_lower()
	return best

# --- LoopState signals -------------------------------------------------------------

func _on_loop_started(_index: int) -> void:
	cards.clear()
	whiteout.clear_white(0.8)
	sunrise = 0.0
	headlights.light_energy = 0.0
	hari.position = HARI_START
	hari.velocity = Vector3.ZERO
	advay.position = ADVAY_AT_CAR
	_keys_path.clear()
	rig.snap()

func _on_dialogue_closed(id: String) -> void:
	if id.begins_with("amma"):
		cards.hide_phone()

func _on_clue_saved(id: String) -> void:
	toast.push(StoryData.clue(id))                                       # visual twin: notes card

func _on_keys_exchanged(from: String, to: String) -> void:
	_keys_from = _anchor(from)                                           # visual twin: keys travel
	_keys_path.assign(["hari", to] if to == "manikandan" else [to])
	_keys_t = 0.0

func _on_advay_arrived(took_keys: bool) -> void:
	advay.position = ADVAY_AT_CAR
	cards.show_caption("advay_takes_keys" if took_keys else "advay_refused")

func _on_dawn_crash() -> void:
	# visual twins: headlight sweep from the SUV, camera shake, then the white-out
	rig.shake = CRASH_FLASH_SECONDS
	whiteout.play_crash(CRASH_FLASH_SECONDS, CRASH_WHITE_SECONDS)
	var tween := create_tween()
	tween.tween_property(headlights, "light_energy", 14.0, 0.3)
	tween.parallel().tween_property(headlights, "rotation_degrees:y", -60.0, CRASH_FLASH_SECONDS).from(-120.0)

func _on_safe_dawn() -> void:
	create_tween().tween_property(self, "sunrise", 1.0, 2.5)            # visual twin: sunrise

# --- presentation ------------------------------------------------------------------

func _update_npcs(delta: float) -> void:
	var on_phone: bool = LoopState.manikandan_on_phone()
	manikandan_sprite.set_art("res://assets/art/npc/manikandan_phone.png" if on_phone else "res://assets/art/npc/manikandan.png", "phone" if on_phone else "")
	advay.visible = LoopState.advay_present()
	if advay.visible:
		var leave: bool = LoopState.clock_minutes >= LoopState.ADVAY_TIME + ADVAY_LEAVES_CAR_AFTER
		advay.position = advay.position.move_toward(ADVAY_ON_DECK if leave else ADVAY_AT_CAR, 1.4 * delta)

func _update_keys_icon(delta: float) -> void:
	if _keys_path.is_empty():
		keys_icon.position = _anchor(LoopState.keys_holder)
		return
	_keys_t += delta / KEYS_MOVE_SECONDS
	var target := _anchor(_keys_path[0])
	var t := smoothstep(0.0, 1.0, minf(_keys_t, 1.0))
	keys_icon.position = _keys_from.lerp(target, t) + Vector3(0, sin(t * PI) * 0.4, 0)
	if _keys_t >= 1.0:
		_keys_from = target
		_keys_path.pop_front()
		_keys_t = 0.0

func _anchor(holder: String) -> Vector3:
	match holder:
		"manikandan": return manikandan.position + Vector3(0.25, 1.0, 0.1)
		"advay": return advay.position + Vector3(0.3, 1.0, 0.1)
		"hari": return hari.position + Vector3(0.35, 1.0, 0.1)
		_: return suv.position + Vector3(0.6, 1.3, 1.0)                 # on the SUV's dashboard

func _update_lighting() -> void:
	var m: float = LoopState.clock_minutes
	var key := Vector2(snappedf(m, 0.5), snappedf(sunrise, 0.02))
	if key == _lit_key:
		return                                  # sky material is costly to update; only on change
	_lit_key = key
	var c: Array = SKY_KEYS[0].duplicate()
	for i in range(1, SKY_KEYS.size()):
		var a: Array = SKY_KEYS[i - 1]
		var b: Array = SKY_KEYS[i]
		if m >= a[0]:
			var t := clampf((m - a[0]) / (b[0] - a[0]), 0.0, 1.0)
			for k in range(1, 5):
				c[k] = a[k].lerp(b[k], t)
			c[5] = lerpf(a[5], b[5], t)
	for k in range(1, 5):
		c[k] = c[k].lerp(SUNRISE[k - 1], sunrise)
	c[5] = lerpf(c[5], SUNRISE[4], sunrise)
	var sky_mat := env.sky.sky_material as ProceduralSkyMaterial
	sky_mat.sky_top_color = c[1]
	sky_mat.sky_horizon_color = c[2]
	sky_mat.ground_horizon_color = c[2]
	env.ambient_light_color = c[3]
	env.fog_light_color = c[2].darkened(0.3)
	sky_light.light_color = c[4]
	sky_light.light_energy = c[5]
	beach.set_tint(Color(0.45, 0.5, 0.75).lerp(Color.WHITE, clampf((m - 1720.0) / 75.0, 0.0, 1.0)).lerp(Color.WHITE, sunrise))
	# Fire on the village side rises from 4:45 AM, every loop.
	var glow := clampf((m - LoopState.FIRE_GLOW_TIME) / 20.0, 0.0, 1.0)
	fire_glow.set_tint(Color(1, 1, 1, glow))
	fire_light.light_energy = glow * 4.0
