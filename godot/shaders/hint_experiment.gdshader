
shader_type spatial;
render_mode unshaded;

uniform sampler2D strip_as_colour : source_color, filter_nearest;
uniform sampler2D strip_as_data : filter_nearest;

uniform bool use_source_color = false;

void fragment() {
    if (use_source_color) {
        ALBEDO = texture(strip_as_colour, UV).rgb;
    } else {
        ALBEDO = texture(strip_as_data, UV).rgb;
    }
}
