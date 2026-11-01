# Language notes (Assignment 5)

## Line numbers in godot/shaders/standard_generated.gdshader
- shader_type: line 3; render_mode: line 4
- Inspector albedo colour: line 6; normal-map strength: line 20
- Albedo sampler: line 7 (source_color, filter_linear_mipmap, repeat_enable)
- Normal-map sampler: line 19 (hint_roughness_normal, filter_linear_mipmap, repeat_enable)
- Writes ALBEDO: line 35; ROUGHNESS: line 43; NORMAL_MAP: line 46


## Questions
1. What does shader_type decide? (each type you used, citing the shader_type line of each shader)

shader_type decides what kind of shader I am writing and which built-in variables and functions are available. I used canvas_item for my 2D phone status bar and spatial for the 3D marble floors and hint experiment.

References: night_skip.gdshader:1, deck_marble.gdshader:2, hint_experiment.gdshader:2.

2. Which processor functions did you write, and when does each run? What would change if the colour line moved into vertex(), and why?

I used vertex() to calculate the world position of each vertex and fragment() to calculate the colour and surface properties of each pixel.

If I moved my colour line into vertex(), the result would be calculated at vertices and interpolated between them instead of changing each pixel individually. I would also need to account for the different inputs available in the vertex stage.

References: deck_marble.gdshader:20–22 (vertex), deck_marble.gdshader:24–39 (fragment), night_skip.gdshader:7–9.

3. Three built-ins you read and two you wrote. Which of the read ones are read-only?

I read MODEL_MATRIX, VERTEX, and COLOR. MODEL_MATRIX is read-only and helps convert a vertex position into world space. VERTEX can be modified in vertex(), while COLOR can be modified in the CanvasItem fragment() function.

I wrote to ALBEDO and ROUGHNESS to control the marble's colour and surface finish.

References: deck_marble.gdshader:21, night_skip.gdshader:8, deck_marble.gdshader:27–33.

4. For each hint you used: does it change only the Inspector, or also the value the shader receives? (cite the hint experiment)

hint_range controls the Inspector slider but doesn't clamp values set through code.

source_color changes how colour values are interpreted, including decoding sRGB textures into linear colour space.

hint_normal identifies normal-map data. filter_nearest keeps pixels sharp, while filter_linear_mipmap smooths texture sampling. repeat_enable makes textures repeat.

In my experiment, Quad A showed (64, 128, 192), while Quad B showed (137, 188, 225), confirming that source_color affects the sampled values.

References: night_skip.gdshader:3–5, deck_marble.gdshader:5–14, hint_experiment.gdshader:5–6.


5. Does hint_range clamp a value set from code? (cite what you observed)

No. My capture showed that setting skip_amount to 2.0 was accepted even though the Inspector range was 0 to 1.

At 1.0, the battery pixel was (249, 197, 147), while at 2.0 it became (253, 151, 51). This confirms the value wasn't clamped.

Reference: night_skip.gdshader:3.

Evidence: evidence/a5/ controlled-value captures.

6. Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in your textured shader?

The generated shader uses source_color on line 7 for the albedo texture. The normal-map sampler on line 19 uses hint_roughness_normal without source_color, so it is treated as data rather than ordinary colour.

In my marble shader, I used source_color for albedo_tex, hint_normal for normal_tex, and no colour hint for roughness_tex.

References: standard_generated.gdshader:7,19, deck_marble.gdshader:5,10–11.


7. fragment() runs for every pixel at once. Why can't it read what the neighbouring pixel's fragment() computes, and how does game state reach it instead?

Each fragment runs independently, and many fragments are processed in parallel on the GPU. Because of this, one fragment cannot directly read what another fragment is currently calculating.

In my game, the driver passes the fast-forward state through the skip_amount uniform. The shader uses that value to calculate the orange tint.

References: night_skip.gdshader:3, night_skip.gdshader:7–9.

8. Two things the Godot shading language provides that plain GLSL does not, or makes you write yourself.

First, Godot provides shader_type, which lets me choose between canvas_item and spatial shaders without writing separate GLSL entry-point programs.

Second, Godot provides uniform hints and group_uniforms that connect shader settings directly to the Inspector. I used these to organize the marble material's surface and finish controls.

References: night_skip.gdshader:1, deck_marble.gdshader:4–16.