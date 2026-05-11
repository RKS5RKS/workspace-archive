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

### WORKING TRANSITION SCRIPT (v9 - Universal)

This script plays Animation A once, then does a smooth SLERP transition to Animation B (which loops).

```python
import bpy
import mathutils
from mathutils import Quaternion, Vector

# =========================
# CONFIG - EDIT THESE
# =========================

GLB_PATH = "/root/nomark_project/exports/nomark_walk.glb"
OUTPUT_PATH = "/root/nomark_project/exports/transition_output.mp4"

ANIM_A = "Jump_Start"      # First animation (plays once)
ANIM_B = "Swim_Fwd_Loop"   # Second animation (loops)

TARGET_FRAMES = 90         # Total frames (3 seconds @ 30fps)
TRANSITION_FRAMES = 30     # Frames for SLERP transition

# =========================
# IMPORT GLB
# =========================

bpy.ops.import_scene.gltf(filepath=GLB_PATH)

# =========================
# FIND ARMATURE
# =========================

armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

if armature is None:
    raise Exception("No armature found.")

# =========================
# GET ACTIONS FROM NLA TRACKS
# =========================

def get_action_from_track(track_name):
    if armature.animation_data:
        for track in armature.animation_data.nla_tracks:
            if track.name == track_name and track.strips:
                return track.strips[0].action
    return None

action_a = get_action_from_track(ANIM_A)
action_b = get_action_from_track(ANIM_B)

if action_a is None:
    raise Exception(f"Animation '{ANIM_A}' not found.")
if action_b is None:
    raise Exception(f"Animation '{ANIM_B}' not found.")

print(f"Using: {action_a.name} -> {action_b.name}")

# =========================
# CREATE FINAL ACTION
# =========================

if armature.animation_data is None:
    armature.animation_data_create()

final_action = bpy.data.actions.new("Universal_Transition")
armature.animation_data.action = final_action

# =========================
# HELPER FUNCTIONS
# =========================

def clear_pose():
    """Reset pose to default"""
    bpy.context.scene.frame_set(0)
    for pb in armature.pose.bones:
        pb.rotation_mode = 'QUATERNION'
        pb.location = (0, 0, 0)
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.scale = (1, 1, 1)

def evaluate_pose(action, frame):
    """Evaluate pose from any action at a specific frame"""
    orig_action = armature.animation_data.action
    armature.animation_data.action = action
    bpy.context.scene.frame_set(int(frame))
    
    pose_data = {}
    for pb in armature.pose.bones:
        pose_data[pb.name] = {
            "location": pb.location.copy(),
            "rotation": pb.rotation_quaternion.copy(),
            "scale": pb.scale.copy()
        }
    
    armature.animation_data.action = orig_action
    return pose_data

def insert_pose(frame, pose_dict):
    """Insert pose keyframes into final action"""
    bpy.context.scene.frame_set(frame)
    armature.animation_data.action = final_action
    
    for pb in armature.pose.bones:
        if pb.name not in pose_dict:
            continue
        pb.rotation_mode = 'QUATERNION'
        data = pose_dict[pb.name]
        pb.location = data["location"]
        pb.rotation_quaternion = data["rotation"]
        pb.scale = data["scale"]
        pb.keyframe_insert(data_path="location", frame=frame)
        pb.keyframe_insert(data_path="rotation_quaternion", frame=frame)
        pb.keyframe_insert(data_path="scale", frame=frame)

def blend_poses(pose_a, pose_b, t):
    """SLERP blend between two poses"""
    result = {}
    for bone_name in pose_a.keys():
        if bone_name not in pose_b:
            continue
        a = pose_a[bone_name]
        b = pose_b[bone_name]
        loc = a["location"].lerp(b["location"], t)
        rot = Quaternion.slerp(a["rotation"], b["rotation"], t)
        scale = a["scale"].lerp(b["scale"], t)
        result[bone_name] = {"location": loc, "rotation": rot, "scale": scale}
    return result

# =========================
# BUILD TRANSITION
# =========================

a_start, a_end = action_a.frame_range
b_start, b_end = action_b.frame_range
a_start, a_end = int(a_start), int(a_end)
b_start, b_end = int(b_start), int(b_end)
a_frame_count = a_end - a_start + 1

print(f"A: {a_start}-{a_end} ({a_frame_count} frames), B: {b_start}-{b_end}")

# Capture end of A and start of B
pose_a_end = evaluate_pose(action_a, a_end)
pose_b_start = evaluate_pose(action_b, b_start)

clear_pose()

# Play Animation A once (no loop)
current_frame = 1
for src_frame in range(a_start, a_end + 1):
    pose = evaluate_pose(action_a, src_frame)
    insert_pose(current_frame, pose)
    current_frame += 1

# SLERP Transition
for i in range(TRANSITION_FRAMES):
    t = i / (TRANSITION_FRAMES - 1)
    blended = blend_poses(pose_a_end, pose_b_start, t)
    insert_pose(current_frame, blended)
    current_frame += 1

# Play Animation B (loop to end)
while current_frame <= TARGET_FRAMES:
    src_frame = b_start + ((current_frame - a_frame_count - TRANSITION_FRAMES - 1) % (b_end - b_start + 1))
    pose = evaluate_pose(action_b, src_frame)
    insert_pose(current_frame, pose)
    current_frame += 1

# =========================
# RENDER
# =========================

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TARGET_FRAMES

for o in scene.objects:
    if o.type == 'MESH' and o.name not in ['Mannequin', 'Rig']:
        o.hide_set(True)
        o.hide_render = True

bpy.ops.object.camera_add(location=(0, -6, 1.2))
cam = bpy.context.active_object
scene.camera = cam
cam.rotation_euler = (1.54, 0, 0)

bpy.ops.object.light_add(type='SUN')
bpy.context.active_object.data.energy = 2.5

scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 4
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.image_settings.file_format = 'AVI_RAW'
scene.render.filepath = "/root/nomark_project/exports/transition_output.avi"

bpy.ops.render.render(animation=True)
```

### To use:
1. Save as `/root/nomark_project/transition_script.py`
2. Edit ANIM_A and ANIM_B at the top
3. Run: `blender --background --python /root/nomark_project/transition_script.py`
4. Convert: `ffmpeg -y -i transition_output.avi -c:v libx264 -preset fast -crf 23 transition_output.mp4`

### Key fix that makes it work:
- `evaluate_pose` saves/restores the original action
- `insert_pose` explicitly sets `armature.animation_data.action = final_action` before each keyframe
- Without both of these, Blender auto-switches actions and the source animation plays instead of the transition
