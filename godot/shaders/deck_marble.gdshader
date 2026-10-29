
shader_type spatial;

group_uniforms surface;
uniform sampler2D albedo_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform vec4 albedo_tint : source_color = vec4(1.0);
uniform float tile_size_m : hint_range(0.25, 4.0) = 1.0;

group_uniforms finish;
uniform sampler2D roughness_tex : filter_linear_mipmap, repeat_enable;
uniform sampler2D normal_tex : hint_normal, filter_linear_mipmap, repeat_enable;
uniform float roughness_scale : hint_range(0.0, 2.0) = 1.0;
uniform float specular_amount : hint_range(0.0, 1.0) = 0.5;
uniform float normal_depth : hint_range(0.0, 2.0) = 1.0;

group_uniforms;

varying vec3 world_position;

void vertex() {
    world_position = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
    vec2 uv = world_position.xz / tile_size_m;

    ALBEDO = texture(albedo_tex, uv).rgb * albedo_tint.rgb;

    ROUGHNESS = clamp(
        texture(roughness_tex, uv).r * roughness_scale,
        0.0,
        1.0
    );

    SPECULAR = specular_amount;

    NORMAL_MAP = texture(normal_tex, uv).rgb;
    NORMAL_MAP_DEPTH = normal_depth;
}
