# --- EXPORT: export_asset(blend, root, glb) opens one asset's .blend, selects its root Empty and the parts under it (not the
#     camera or light), and writes binary glTF with Blender's own exporter: +Y Up on (Blender Z-up -> Godot Y-up), modifiers
#     applied, materials exported. Enum values are read from the operator, not assumed. Run once per asset.
import bpy, os

REPO = "/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a"

def export_asset(blend, root_name, glb):
    if bpy.data.filepath != os.path.join(REPO, blend):
        bpy.ops.wm.open_mainfile(filepath=os.path.join(REPO, blend))
    root = bpy.data.objects[root_name]
    bpy.ops.object.select_all(action="DESELECT")
    for o in [root, *root.children_recursive]:
        o.select_set(True)
    bpy.context.view_layer.objects.active = root
    out = os.path.join(REPO, glb)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:                                               # the format enum is dynamic and reads back empty, so try GLB and report
        bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_selection=True, export_yup=True, export_apply=True)
    except TypeError as e:
        print("export_format GLB rejected:", e); raise
    print(blend, "->", glb, os.path.getsize(out), "bytes | exported:", sorted(o.name for o in bpy.context.selected_objects))

# How it was run (~20:39 EDT), each line its own execute_blender_code call after exec() of this file:
#   export_asset("blender/fence_segment.blend", "fence_segment", "godot/assets/models/fence_segment.glb")   -> 12596 bytes
#   export_asset("blender/rock_shrine.blend", "rock_shrine", "godot/assets/models/rock_shrine.glb")         -> failed, see below
#   export_asset("blender/suv.blend", "suv", "godot/assets/models/suv.glb")                                 -> failed, see below
# The first version read export_format's enum list, which comes back empty for this dynamic enum (IndexError); fixed by
# passing "GLB" directly. Then: opening a .blend inside the same call loses the window context, and the exporter needs
# bpy.context.active_object ("'Context' object has no attribute 'active_object'"). Fix: open the file in one call
# (bpy.ops.wm.open_mainfile) and export in the next. suv.glb -> 39276 bytes, rock_shrine.glb -> 32440 bytes.
