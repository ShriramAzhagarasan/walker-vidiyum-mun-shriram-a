shader_type canvas_item;

uniform float skip_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 skip_tint : source_color = vec4(1.0, 0.6, 0.2, 1.0);
uniform float tint_strength : hint_range(0.0, 1.0) = 0.5;

void fragment() {
    COLOR.rgb = mix(COLOR.rgb, skip_tint.rgb, skip_amount * tint_strength);
}
