import bpy
import os

# =========================
# CONFIG
# =========================

GLB_PATH = "/root/nomark_project/exports/nomark_walk.glb"
TEXTURE_PATH = "/root/nomark_project/textures/nomark_skin_texture.png"
OUTPUT_PATH = "/root/nomark_project/exports/nomark_with_skin.glb"

# =========================
# STEP 1: IMPORT GLB
# =========================

print("=" * 50)
print("NOMARK SKIN + PROPER CAMERA")
print("=" * 50)

print("\n[1/6] Importing GLB...")
bpy.ops.import_scene.gltf(filepath=GLB_PATH)

mesh_obj = None
armature = None

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.name in ['Mannequin', 'Body']:
        mesh_obj = obj
    elif obj.type == 'ARMATURE':
        armature = obj

if not mesh_obj:
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break

print(f"  Mesh: {mesh_obj.name}")

# =========================
# STEP 2: LOAD TEXTURE
# =========================

print("\n[2/6] Loading skin texture...")

if "Nomark_Skin" in bpy.data.images:
    skin_tex = bpy.data.images["Nomark_Skin"]
else:
    skin_tex = bpy.data.images.load(TEXTURE_PATH)
    skin_tex.name = "Nomark_Skin"

print(f"  Texture: {skin_tex.name}")

# =========================
# STEP 3: CREATE TEXTURED MATERIAL
# =========================

print("\n[3/6] Creating textured material...")

mat = bpy.data.materials.get("Nomark_Skin_Mat")
if mat:
    bpy.data.materials.remove(mat)

mat = bpy.data.materials.new(name="Nomark_Skin_Mat")
mat.use_nodes = True
mat.blend_method = 'OPAQUE'
mat.shadow_method = 'OPAQUE'

nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

# Image texture
tex_node = nodes.new('ShaderNodeTexImage')
tex_node.location = (-300, 0)
tex_node.image = skin_tex

# Principled BSDF
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (100, 0)

# Output
output = nodes.new('ShaderNodeOutputMaterial')
output.location = (400, 0)

# Connect - texture to base color
links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("  Material with texture created")

# =========================
# STEP 4: ASSIGN TO MESH
# =========================

print("\n[4/6] Assigning material...")

mesh = mesh_obj.data
mesh.materials.clear()
mesh.materials.append(mat)

print("  Material assigned")

# =========================
# STEP 5: SETUP SCENE - CORRECT CAMERA
# =========================

print("\n[5/6] Setting up scene with CORRECT camera...")

scene = bpy.context.scene

# Hide extra objects
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.name not in [mesh_obj.name, 'Mannequin', 'Rig']:
        obj.hide_set(True)
        obj.hide_render = True

# CRITICAL CAMERA SETTINGS - fixes clipping, shows full body
bpy.ops.object.camera_add(location=(0, -6, 1.2))
cam = bpy.context.active_object
cam.rotation_euler = (1.54, 0, 0)  # 2% tilt down for FULL BODY
cam.data.clip_start = 0.001
cam.data.clip_end = 1000
scene.camera = cam

print(f"  Camera location: (0, -6, 1.2)")
print(f"  Camera rotation: (1.54, 0, 0)")

# Light
bpy.ops.object.light_add(type='SUN')
light = bpy.context.active_object
light.data.energy = 3.0

print("  Scene configured with proper camera")

# =========================
# STEP 6: EXPORT
# =========================

print("\n[6/6] Exporting GLB...")

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_PATH,
    export_format='GLB',
    export_materials='EXPORT',
    export_colors=True
)

print("\n" + "=" * 50)
print("DONE!")
print("=" * 50)
print(f"Output: {OUTPUT_PATH}")
print("=" * 50)