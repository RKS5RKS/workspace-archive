# NOMARK Animation - Exact Working Steps

## 1. Connect to Server
```python
import paramiko
key = paramiko.Ed25519Key.from_private_key_file('/home/openclaw/.openclaw/credentials/ssh/id_ed25519')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='143.244.145.155', port=22, username='root', pkey=key, timeout=15)
```

## 2. Render Script (AVI_RAW format)
```python
import bpy

# Import GLB with embedded animation
bpy.ops.import_scene.gltf(filepath="/root/nomark_project/exports/nomark_walk.glb")

# Apply dark navy material
for o in bpy.context.selected_objects:
    if o.type == 'MESH':
        o.data.materials.clear()
        mat = bpy.data.materials.new(name="NOMARK")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.18, 1)
        o.data.materials.append(mat)

# Find armature
armature = None
for o in bpy.context.selected_objects:
    if o.type == 'ARMATURE':
        armature = o

# Activate animation - USE TRACK NAME, not action name
# For punch: track.name == "Punch_Jab" -> action = Punch_Jab_Rig
if armature and armature.animation_data:
    for track in armature.animation_data.nla_tracks:
        if track.name == "Punch_Jab" and track.strips:  # CHANGE THIS for different animations
            armature.animation_data.action = track.strips[0].action

# FIX CLIPPING: Hide extra objects in scene (Cube, Icosphere cut body)
for o in bpy.context.scene.objects:
    if o.type == 'MESH' and o.name not in ['Mannequin', 'Rig']:
        o.hide_set(True)
        o.hide_render = True

# Camera - (0, -6, 1.2) shows full body with 2% tilt down
bpy.ops.object.camera_add(location=(0, -6, 1.2))
cam = bpy.context.active_object
bpy.context.scene.camera = cam
cam.rotation_euler = (1.54, 0, 0)  # 2% tilt down for full body
cam.data.clip_start = 0.001
cam.data.clip_end = 1000

# Light
bpy.ops.object.light_add(type='SUN')
bpy.context.active_object.data.energy = 2.5

# Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 360
bpy.context.scene.cycles.samples = 8  # CRITICAL: Use 8 samples, NOT default (64/128)!

# AVI_RAW format - the only working video format
bpy.context.scene.render.image_settings.file_format = 'AVI_RAW'
bpy.context.scene.render.filepath = "/root/nomark_project/exports/punch_fixed.avi"
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 30

bpy.ops.render.render(animation=True)
```

## 3. Convert to MP4
```bash
ffmpeg -y -i input.avi -c:v mpeg4 -q:v 3 output.mp4
```

## Animation Track Names (from GLB)
- Walk: `Walk_Loop`
- Punch_Jab: `Punch_Jab`
- Punch_Cross: `Punch_Cross`
- Idle: `Idle_Loop`
- Dance: `Dance_Loop`
- Sword: `Sword_Attack`
- Jump: `Jump_Start`
- Roll: `Roll`
- Sprint: `Sprint_Loop`
- Jog: `Jog_Fwd_Loop`

## Animation Frame Counts (from GLB)
- Walk_Loop: 32 frames
- Sword_Attack: 36 frames
- Roll: 35 frames
- Punch_Jab: 20 frames
- Jump_Start: 32 frames
- Jog_Fwd_Loop: 22 frames
- Idle_Loop: 60 frames
- Dance_Loop: 24 frames
- Sprint_Loop: 16 frames
- Punch_Cross: 20 frames

## How to Render 3-Second Videos (90 frames)
Run sequentially, not in parallel!
```python
# Upload render script and run in background
ssh.exec_command('cd /root/nomark_project && nohup blender --background --python render_all_3s.py > render_all.log 2>&1 &')
```

## CRITICAL: Always Use 8 Samples!
Blender defaults to 64-128 samples, which makes rendering SLOW. Always set:
```python
bpy.context.scene.cycles.samples = 8
```
This makes rendering ~8x faster!

## How to Loop Animations (Non-Looping Ones)
Some animations don't loop naturally (Punch_Jab, Punch_Cross, Sword_Attack, Jump_Start, Roll). Use ffmpeg instead of trying to manipulate Blender keyframes:

1. Render the animation once (e.g., Roll = 35 frames)
2. Use ffmpeg to repeat it 3x:
```bash
# Create concat list
cat > roll-concat.txt << 'EOF'
file 'Roll_once.avi'
file 'Roll_once.avi'
file 'Roll_once.avi'
EOF

# Concatenate
ffmpeg -y -f concat -safe 0 -i roll-concat.txt -c:v mpeg4 -q:v 3 Roll_3s_loop.mp4
```

This creates a perfect 3-second loop!

## How to Create Transitions Between Animations
1. Edit `/root/nomark_project/transition_script.py` to set:
   - ANIM_A = "Roll"  # First animation name
   - ANIM_B = "Dance_Loop"  # Second animation name
2. Run: `blender --background --python transition_script.py`
3. Script auto-detects animation lengths from GLB
4. Output: `transition_full_cycle.mp4` in exports folder
5. Convert: `ffmpeg -y -framerate 30 -i transition_full_cycle.mp4%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4`

## Transition Script Key Features
- Automatically gets frame counts from GLB (uses full animation cycles)
- Uses SLERP interpolation for smooth bone rotation transitions
- Default: 15 transition frames between animations
- Lower samples (8) for faster rendering
