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
print("NOMARK SKIN TEXTURE PIPELINE")
print("=" * 50)

print("\n[1/7] Importing GLB...")
bpy.ops.import_scene.gltf(filepath=GLB_PATH)

mesh_obj = None
armature = None

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.name in ['Mannequin', 'Body']:
        mesh_obj = obj
    elif obj.type == 'ARMATURE':
        armature = obj

if not mesh_obj:
    for obj in bpy.context.scene.objects.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break

print(f"  Mesh: {mesh_obj.name}")
print(f"  Armature: {armature.name if armature else 'None'}")

# =========================
# STEP 2: LOAD TEXTURE
# =========================

print("\n[2/7] Loading skin texture...")

# Check if texture already exists
if "Nomark_Skin_Texture" in bpy.data.images:
    skin_tex = bpy.data.images["Nomark_Skin_Texture"]
else:
    skin_tex = bpy.data.images.load(TEXTURE_PATH)
    skin_tex.name = "Nomark_Skin_Texture"

print(f"  Texture loaded: {skin_tex.name} ({skin_tex.size[0]}x{skin_tex.size[1]})")

# =========================
# STEP 3: CREATE TEXTURE NODE
# =========================

print("\n[3/7] Creating texture nodes...")

# Create texture datablock
if "Nomark_Skin_Tex" not in bpy.data.textures:
    skin_tex_node = bpy.data.textures.new("Nomark_Skin_Tex", 'IMAGE')
    skin_tex_node.image = skin_tex
else:
    skin_tex_node = bpy.data.textures["Nomark_Skin_Tex"]
    skin_tex_node.image = skin_tex

# =========================
# STEP 4: CREATE MATERIAL WITH TEXTURE
# =========================

print("\n[4/7] Creating textured material...")

# Create or get material
mat = bpy.data.materials.get("Nomark_Skin_Material")
if mat:
    bpy.data.materials.remove(mat)

mat = bpy.data.materials.new(name="Nomark_Skin_Material")
mat.use_nodes = True
mat.blend_method = 'OPAQUE'
mat.shadow_method = 'OPAQUE'

nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Create nodes
output = nodes.new('ShaderNodeOutputMaterial')
output.location = (400, 0)

bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (100, 0)

# Image texture node
tex_node = nodes.new('ShaderNodeTexImage')
tex_node.location = (-300, 0)
tex_node.image = skin_tex

# Connect texture to base color
links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

# Also connect to some roughness variation
# Create a separate texture node for roughness (using same texture but grayscale)
tex_rough = nodes.new('ShaderNodeTexImage')
tex_rough.location = (-300, -200)
tex_rough.image = skin_tex

# Set to non-color for proper interpretation
# Actually for now just use color directly

links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("  Material created with skin texture")

# =========================
# STEP 5: ASSIGN MATERIAL TO MESH
# =========================

print("\n[5/7] Assigning material to mesh...")

mesh = mesh_obj.data

# Clear existing materials
mesh.materials.clear()

# Add new material
mesh.materials.append(mat)

print("  Material assigned")

# =========================
# STEP 6: SETUP SCENE
# =========================

print("\n[6/7] Setting up scene...")

scene = bpy.context.scene

# Hide extra objects
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.name not in [mesh_obj.name, 'Mannequin', 'Rig']:
        obj.hide_set(True)
        obj.hide_render = True

# Camera - full body
bpy.ops.object.camera_add(location=(0, -6, 1.2))
cam = bpy.context.active_object
bpy.context.scene.camera = cam
cam.rotation_euler = (1.54, 0, 0)

# Light
bpy.ops.object.light_add(type='SUN')
light = bpy.context.active_object
light.data.energy = 3.0

print("  Scene configured")

# =========================
# STEP 7: EXPORT GLB
# =========================

print("\n[7/7] Exporting GLB with textures...")

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_PATH,
    export_format='GLB',
    export_materials='EXPORT',
    export_colors=True,
    export_cameras=False,
    export_lights=False,
    export_extras=True
)

print("\n" + "=" * 50)
print("SKIN TEXTURE PIPELINE COMPLETE!")
print("=" * 50)
print(f"Output: {OUTPUT_PATH}")
print("=" * 50)