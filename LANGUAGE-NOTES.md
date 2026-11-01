# Language Notes — Assignment 5

## Annotating the Generated Shader

**Line 3 — `shader_type spatial`**

I used `spatial` because this shader is meant for 3D objects. It allows the material to interact with lighting and lets me control properties like colour, roughness, and normal maps.

**Line 4 — `render_mode`**

This line controls how Godot renders the material.

- `blend_mix` uses normal alpha blending.
- `depth_draw_opaque` writes opaque surfaces to the depth buffer so Godot knows which surfaces are in front.
- `cull_back` skips the back faces of the mesh.
- `diffuse_burley` controls how diffuse light reflects from the surface.
- `specular_schlick_ggx` calculates the shiny reflections and highlights.

These settings help the marble react to lighting in the 3D scene.

**Line 6 — Albedo Colour**

This uniform matches the Albedo Color setting in the Inspector. It controls the base colour that gets multiplied with the texture.

**Line 7 — Albedo Texture**

The albedo sampler uses `source_color` because the marble image stores colour in sRGB. Godot needs to convert it into linear colour space before doing the lighting calculations. Without the hint, the marble could look washed out.

**Line 14 — Roughness Texture**

`hint_roughness_r` tells Godot that roughness information is stored in the red channel for its roughness-limiting feature. There is no `source_color` because roughness is numerical data, not a colour. The shader reads the red channel when calculating roughness.

**Line 19 — Normal Map**

The normal texture uses `hint_roughness_normal`, which identifies it as a normal map used by the roughness limiter. It does not need `source_color` because its RGB values represent surface directions rather than visible colours.

**Line 20 — Normal Scale**

This matches the Normal Map Scale setting in the Inspector. It controls how strongly the normal map affects the appearance of small details on the surface.

**Line 35 — ALBEDO**

This line multiplies the sampled albedo texture by the material's colour. In my `deck_marble.gdshader`, line 27 does something similar, except I use world-position-based coordinates to keep the marble scale consistent across the floors.

**Line 43 — ROUGHNESS**

This line multiplies the roughness texture value by the material's roughness setting. My marble shader does this on lines 29–33, but I also use `clamp()` to keep the result between 0 and 1.

**Line 46 — NORMAL_MAP**

This line reads the normal texture and assigns it to `NORMAL_MAP`. My marble shader does the same thing on line 37, using world XZ coordinates to sample the texture.

---

## Questions

### 1. What does shader_type decide?

`shader_type` tells Godot what kind of shader I am writing and which functions and built-in variables I can use.

For my phone status bar, I used `canvas_item` because it is a 2D HUD element. For the marble floors and hint experiment, I used `spatial` because those are 3D objects.

**References:** `night_skip.gdshader:1`, `deck_marble.gdshader:2`, `hint_experiment.gdshader:2`.

### 2. Which processor functions did you write, and when does each run?

I used two main functions, `vertex()` and `fragment()`.

In `night_skip.gdshader`, I only used `fragment()` because I just needed to change the colour of the phone status bar.

In `deck_marble.gdshader`, I used both. `vertex()` runs for every vertex and calculates the world position, while `fragment()` runs for each fragment and calculates the marble's colour, roughness, and normal-map values.

In `hint_experiment.gdshader`, I only used `fragment()` because I wanted to compare how the same texture is sampled with and without `source_color`.

If I moved the night-skip colour calculation into `vertex()`, it would calculate the tint at the corners and interpolate it across the rectangle. Since the draw colour and `skip_amount` are the same at every corner, I wouldn't expect the bar to look noticeably different in this specific case, assuming the colour is passed through correctly. However, this would be different for an object with varying colours or textures.

**References:** `night_skip.gdshader:7–9`, `deck_marble.gdshader:20–22`, `deck_marble.gdshader:24–39`, `hint_experiment.gdshader:10–16`.

### 3. Name three built-ins you read and two you wrote. Which are read-only?

The three built-ins I read are `MODEL_MATRIX`, `VERTEX`, and `COLOR`.

`MODEL_MATRIX` is read-only, and I use it to convert a vertex position from local space into world space.

`VERTEX` contains the vertex position. It is not read-only because it can be changed inside `vertex()`.

`COLOR` contains the colour of the object. It is also writable in my CanvasItem shader because I use it to output the new orange colour.

The two built-ins I wrote are `ALBEDO` and `ROUGHNESS`. I use `ALBEDO` to set the marble's base colour and `ROUGHNESS` to control how rough or shiny its surface appears.

**References:** `deck_marble.gdshader:21`, `night_skip.gdshader:8`, `deck_marble.gdshader:27–33`.

### 4. For each hint, does it change only the Inspector or also the shader's values?

I learned that not every hint does the same thing.

`hint_range` mainly changes the Inspector slider. It doesn't clamp values that are assigned through code.

`source_color` affects how colour values are interpreted. On a colour texture, it enables the correct sRGB-to-linear conversion. I also use it on `skip_tint` to identify that uniform as a colour.

`hint_normal` tells Godot that the texture is a normal map. It mainly affects how the texture is identified and handled, rather than applying ordinary colour decoding.

`filter_nearest` and `filter_linear_mipmap` affect texture sampling. Nearest keeps texels separate, while linear filtering blends samples and mipmaps help at different distances.

`repeat_enable` changes how textures are sampled outside the normal 0–1 UV range, allowing them to tile instead of stopping at the edge.

The hint experiment helped me understand this. Quad A, with `source_color`, showed 64, 128, and 192. Quad B, without it, showed 137, 188, and 225. The difference was visible even though both quads used the same image.

**References:** `night_skip.gdshader:3–5`, `deck_marble.gdshader:5–14`, `hint_experiment.gdshader:5–6`.

### 5. Does hint_range clamp a value set from code?

No. I confirmed this using the controlled-value capture.

Even though the `skip_amount` uniform has a range from 0 to 1, setting it to 2.0 from code still affected the shader.

At 1.0, the battery pixel was (249, 197, 147). At 2.0, it became (253, 151, 51).

This showed me that `hint_range` only restricts the Inspector slider and doesn't enforce the limit on values coming from code. If I want an actual limit, I need to handle that in my code.

**Reference:** `night_skip.gdshader:3`.

**Evidence:** `evidence/a5/debug-key/skip_2_0.png` and `TEST-REPORT.md:265`.

### 6. Which lines make the albedo sample as colour and the normal map as data?

In the generated shader, line 7 uses `source_color` for the albedo texture because it contains visible colour.

Line 19 uses `hint_roughness_normal` for the normal texture without `source_color`, since it contains directional data.

The roughness texture on line 14 also has no `source_color`. It uses `hint_roughness_r`, while the shader reads the roughness value from the red channel on lines 41–43.

In my `deck_marble.gdshader`, I followed the same idea. The albedo texture uses `source_color` on line 5, roughness is sampled as data on line 10, and the normal texture uses `hint_normal` on line 11.

**References:** `standard_generated.gdshader:7,14,19,41–43`, `deck_marble.gdshader:5,10–11`.

### 7. Why can't fragment() read what a neighbouring pixel is computing, and how does game state reach it?

The GPU runs many fragments in parallel, and each one calculates its own output. Because of this, a fragment cannot directly access the unfinished calculation of another fragment.

In my game, the shader gets information about the fast-forward state through a uniform called `skip_amount`.

The driver reads the game state and updates that uniform. The shader then uses the value to blend the phone status bar toward orange.

This way, the shader doesn't need to access the game state directly.

**References:** `night_skip.gdshader:3`, `night_skip.gdshader:7–9`, `night_skip_driver.gd:32`.

### 8. Name two things Godot shading language provides that plain GLSL does not, or makes you write yourself.

One thing is `shader_type`. In Godot, I can directly choose `canvas_item` for 2D or `spatial` for 3D, and Godot provides the appropriate shader functions and built-ins. In regular GLSL, shader stages and their entry points need to be set up differently.

The second thing is the way Godot handles uniforms through the Inspector. I can use `hint_range` to create sliders, `source_color` for colour settings, and `group_uniforms` to organize related properties.

For my marble shader, I separated these into `surface` and `finish` groups, which makes the settings easier to understand and adjust without changing the actual shader code.

**References:** `night_skip.gdshader:1`, `deck_marble.gdshader:4–16`.