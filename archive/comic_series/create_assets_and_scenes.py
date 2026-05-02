#!/usr/bin/env python3
"""
Simple Character Asset Generator & Animator
Creates and assembles character parts into poses and scenes
"""
from PIL import Image, ImageDraw
import os

# --- Directories ---
PARTS_DIR_HERO = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts"
PARTS_DIR_VILLAIN = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters/villain/parts"
LOCATIONS_DIR = "/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
OUTPUT_DIR = "/home/openclaw/.openclaw/workspace/comic_series/assets/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load Parts ---
def load_parts(char_type="hero"):
    parts = {}
    if char_type == "hero":
        parts_dir = PARTS_DIR_HERO
    elif char_type == "villain":
        parts_dir = PARTS_DIR_VILLAIN
    else:
        raise ValueError("Unknown character type")

    for name in ['head', 'torso', 'left_arm', 'right_arm', 'left_leg', 'right_leg']:
        path = os.path.join(parts_dir, f"{name}.png")
        if os.path.exists(path):
            parts[name] = Image.open(path).convert("RGBA")
        else:
            print(f"Warning: Part '{name}' not found for {char_type} at {path}")
    return parts

# --- Rigging & Posing ---
def compose_pose(char_parts, pose_name, canvas_size=(1280, 720)):
    """Compose a character pose"""
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    cx, cy = canvas_size[0] // 2, canvas_size[1] // 2 + 50
    
    poses = {
        "standing": {'left_leg': (-20, 80), 'right_leg': (25, 80), 'torso': (0, 0),
                     'head': (0, -130), 'left_arm': (-60, -10), 'right_arm': (60, -10)},
        "arms_up": {'left_leg': (-20, 80), 'right_leg': (25, 80), 'torso': (0, 0),
                    'head': (0, -130), 'left_arm': (-70, -90), 'right_arm': (70, -90)},
        "walking": {'left_leg': (-30, 90), 'right_leg': (20, 70), 'torso': (0, 10),
                    'head': (0, -120), 'left_arm': (40, 10), 'right_arm': (-40, -10)},
        "punching": {'left_leg': (-20, 80), 'right_leg': (25, 80), 'torso': (10, 0),
                     'head': (5, -125), 'left_arm': (-50, 10), 'right_arm': (140, -20)},
        "sitting": {'left_leg': (-40, 140), 'right_leg': (30, 140), 'torso': (0, 50),
                    'head': (0, -80), 'left_arm': (-30, 20), 'right_arm': (30, 20)},
        "crouching": {'left_leg': (-25, 110), 'right_leg': (30, 110), 'torso': (0, 30),
                      'head': (0, -100), 'left_arm': (-20, 10), 'right_arm': (20, 10)},
        "pointing": {'left_leg': (-20, 80), 'right_leg': (25, 80), 'torso': (0, 0),
                     'head': (0, -130), 'left_arm': (60, -80), 'right_arm': (-60, -10)},
    }
    
    pose = poses.get(pose_name, poses["standing"])
    order = ['left_leg', 'right_leg', 'torso', 'head', 'left_arm', 'right_arm']
    
    for p in order:
        if p not in char_parts:
            continue
        img = char_parts[p]
        ox, oy = pose.get(p, (0, 0))
        x, y = cx + ox - img.width // 2, cy + oy - img.height // 2
        canvas.paste(img, (int(x), int(y)), img)
    
    return canvas

# --- Scene Composition ---
def create_scene(background_path, character_image_path, output_path, char_x=400, char_y=250):
    """Compose a scene with background and character"""
    bg = Image.open(background_path).convert("RGBA")
    bg = bg.resize((1280, 720)) # Standardize background size
    
    char_img = Image.open(character_image_path).convert("RGBA") # Load character image here
    
    scale_factor = 0.7
    char_img = char_img.resize((int(char_img.width * scale_factor), int(char_img.height * scale_factor)))
    
    x_offset = char_x - char_img.width // 2
    y_offset = char_y - char_img.height // 2
    
    bg.paste(char_img, (int(x_offset), int(y_offset)), char_img)
    bg.save(output_path)
    return output_path

# --- Main Execution ---
if __name__ == "__main__":
    print("=== Generating Character Poses and Scenes ===")
    
    # Load hero and villain parts
    hero_parts = load_parts("hero")
    villain_parts = load_parts("villain")
    
    poses_to_generate = ["standing", "arms_up", "walking", "punching", "sitting", "crouching", "pointing"]
    
    # Generate poses for Hero
    print("\n--- Generating Hero Poses ---")
    for pose_name in poses_to_generate:
        if not hero_parts: continue
        hero_pose_canvas = compose_pose(hero_parts, pose_name)
        output_path = os.path.join(OUTPUT_DIR, f"hero_{pose_name}.png")
        hero_pose_canvas.save(output_path)
        print(f"  ✓ Saved: {output_path}")

    # Generate poses for Villain
    print("\n--- Generating Villain Poses ---")
    for pose_name in poses_to_generate:
        if not villain_parts: continue
        villain_pose_canvas = compose_pose(villain_parts, pose_name)
        output_path = os.path.join(OUTPUT_DIR, f"villain_{pose_name}.png")
        villain_pose_canvas.save(output_path)
        print(f"  ✓ Saved: {output_path}")
    
    # --- Create Scene Library ---
    print("\n--- Creating Scene Library ---")
    all_pose_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png") and ("hero_" in f or "villain_" in f)]
    locations_dir = "/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
    locations = sorted([f for f in os.listdir(locations_dir) if f.endswith(".jpg")])[:5]
    
    print(f"Found {len(all_pose_files)} poses, {len(locations)} locations")
    
    scene_count = 0
    for pose_file_name in all_pose_files:
        for loc_file in locations:
            scene_name = f"scene_{scene_count:03d}.png"
            out_path = os.path.join(OUTPUT_DIR, scene_name)
            
            try:
                create_scene(
                    os.path.join(locations_dir, loc_file),
                    os.path.join(OUTPUT_DIR, pose_file_name), # Pass the pose file path here
                    out_path,
                    char_x=640,
                    char_y=550
                )
                print(f"  ✓ Created scene: {scene_name}")
                scene_count += 1
            except FileNotFoundError:
                print(f"Warning: Missing background file {loc_file} or pose file {pose_file_name}")
                continue

    print(f"\nGenerated {scene_count} scenes in {OUTPUT_DIR}")

    # --- Create Animation Sequence ---
    print("\n=== Creating Animation Sequence ===")
    animation_frames = sorted([f for f in os.listdir(OUTPUT_DIR) if f.startswith('scene_') and f.endswith('.png')])[:10]

    frame_list_path = os.path.join(OUTPUT_DIR, "animation_frames.txt")
    with open(frame_list_path, "w") as f:
        for frame in animation_frames:
            f.write(f"file '{frame}'\n")
    
    print(f"Animation frames selected: {len(animation_frames)}")
    print(f"Frame list saved to: {frame_list_path}")

    print("\n=== Process Complete ===")