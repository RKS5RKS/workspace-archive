#!/usr/bin/env python3
"""
Improved Pose Generator - With more poses and CLI support
Usage: ./venv/bin/python pose_generator_v2.py [pose_name]
       ./venv/bin/python pose_generator_v2.py --list
       ./venv/bin/python pose_generator_v2.py --add-pose "pose_name,x,y,..."
"""
import os
import sys
import json

# Set up environment for model caching
os.environ['HOME'] = '/home/openclaw/.openclaw/workspace/comic_series'
os.environ['XDG_CACHE_HOME'] = '/home/openclaw/.openclaw/workspace/comic_series/.cache'

from PIL import Image
from rembg import remove

BASE_DIR = "/home/openclaw/.openclaw/workspace/comic_series"
OUTPUT_DIR = f"{BASE_DIR}/generated_poses"
CHAR_DIR = f"{BASE_DIR}/character_concepts"
CONFIG_FILE = f"{BASE_DIR}/pose_config.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Default poses
DEFAULT_POSES = {
    "standing": {"head": (422, 0), "torso": (352, 138), "left_arm": (70, 138), "right_arm": (1056, 138), "left_leg": (394, 346), "right_leg": (732, 346)},
    "arms_up": {"head": (422, 0), "torso": (352, 138), "left_arm": (70, 50), "right_arm": (1056, 50), "left_leg": (394, 346), "right_leg": (732, 346)},
    "arms_crossed": {"head": (422, 0), "torso": (352, 138), "left_arm": (450, 180), "right_arm": (750, 180), "left_leg": (394, 346), "right_leg": (732, 346)},
    "hands_hips": {"head": (422, 0), "torso": (352, 138), "left_arm": (250, 300), "right_arm": (930, 300), "left_leg": (394, 346), "right_leg": (732, 346)},
    "victory": {"head": (422, 0), "torso": (352, 138), "left_arm": (20, 20), "right_arm": (1150, 20), "left_leg": (394, 346), "right_leg": (732, 346)},
    "walking": {"head": (422, 20), "torso": (352, 150), "left_arm": (100, 180), "right_arm": (1000, 120), "left_leg": (350, 346), "right_leg": (780, 346)},
    "running": {"head": (422, 30), "torso": (352, 160), "left_arm": (20, 100), "right_arm": (1100, 200), "left_leg": (300, 346), "right_leg": (800, 346)},
    "punching": {"head": (422, 10), "torso": (352, 140), "left_arm": (70, 138), "right_arm": (1200, 150), "left_leg": (394, 346), "right_leg": (700, 346)},
    "crouching": {"head": (422, 100), "torso": (352, 250), "left_arm": (100, 300), "right_arm": (900, 300), "left_leg": (350, 500), "right_leg": (750, 500)},
    "jumping": {"head": (422, -50), "torso": (352, 100), "left_arm": (50, 50), "right_arm": (1100, 50), "left_leg": (320, 400), "right_leg": (750, 350)},
    "sitting": {"head": (422, 150), "torso": (352, 280), "left_arm": (150, 350), "right_arm": (850, 350), "left_leg": (300, 500), "right_leg": (750, 500)},
    "kneeling": {"head": (422, 200), "torso": (352, 300), "left_arm": (150, 380), "right_arm": (850, 380), "left_leg": (400, 550), "right_leg": (700, 550)},
    # New poses
    "defensive": {"head": (422, 0), "torso": (352, 138), "left_arm": (250, 50), "right_arm": (1150, 50), "left_leg": (394, 346), "right_leg": (732, 346)},
    "kick": {"head": (422, 0), "torso": (352, 138), "left_arm": (70, 138), "right_arm": (1056, 138), "left_leg": (200, 200), "right_leg": (732, 346)},
    "ducking": {"head": (422, 100), "torso": (352, 250), "left_arm": (150, 150), "right_arm": (850, 150), "left_leg": (394, 500), "right_leg": (732, 500)},
}

def load_config():
    """Load pose config or create default"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_POSES

def save_config(poses):
    """Save pose config"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(poses, f, indent=2)

def load_and_remove_bg(image_path):
    """Load image and remove background"""
    print(f"Loading: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    print("Removing background...")
    no_bg = remove(img)
    return no_bg

def extract_parts(char_img):
    """Extract body parts with transparency"""
    w, h = char_img.size
    
    parts = {
        'head': (0.35 * w, 0.02 * h, 0.65 * w, 0.20 * h),
        'torso': (0.30 * w, 0.20 * h, 0.70 * w, 0.55 * h),
        'left_arm': (0.05 * w, 0.18 * h, 0.30 * w, 0.45 * h),
        'right_arm': (0.70 * w, 0.18 * h, 0.95 * w, 0.45 * h),
        'left_leg': (0.28 * w, 0.45 * h, 0.45 * w, 1.00 * h),
        'right_leg': (0.55 * w, 0.45 * h, 0.80 * w, 1.00 * h),
    }
    
    extracted = {}
    for name, (x1, y1, x2, y2) in parts.items():
        bbox = (int(x1), int(y1), int(x2), int(y2))
        part = char_img.crop(bbox)
        extracted[name] = part
    
    return extracted

def create_pose(parts, positions, canvas_size=(1408, 768)):
    """Create a pose by positioning parts on canvas"""
    canvas = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    
    for part_name, pos in positions.items():
        if part_name in parts:
            canvas.paste(parts[part_name], pos, parts[part_name])
    
    return canvas

def generate_pose(pose_name, parts, poses):
    """Generate a single pose"""
    if pose_name not in poses:
        print(f"Unknown pose: {pose_name}")
        print(f"Available: {', '.join(poses.keys())}")
        return None
    
    positions = poses[pose_name]
    canvas = create_pose(parts, positions)
    return canvas

def main():
    print("=" * 50)
    print("POSE GENERATOR v2")
    print("=" * 50)
    
    # Load config
    poses = load_config()
    
    # Handle CLI arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            print("\nAvailable poses:")
            for name in poses:
                print(f"  - {name}")
            return
        
        elif sys.argv[1] == "--add-pose":
            # Add custom pose: --add-pose "name,head_x,head_y,torso_x,torso_y,..."
            if len(sys.argv) < 3:
                print("Usage: --add-pose \"name,x,y,x,y,...\"")
                return
            try:
                parts = sys.argv[2].split(',')
                name = parts[0]
                coords = [int(x) for x in parts[1:]]
                if len(coords) != 12:
                    print("Need 12 coordinates (head, torso, l_arm, r_arm, l_leg, r_leg)")
                    return
                poses[name] = {
                    'head': (coords[0], coords[1]),
                    'torso': (coords[2], coords[3]),
                    'left_arm': (coords[4], coords[5]),
                    'right_arm': (coords[6], coords[7]),
                    'left_leg': (coords[8], coords[9]),
                    'right_leg': (coords[10], coords[11]),
                }
                save_config(poses)
                print(f"Added pose: {name}")
            except Exception as e:
                print(f"Error: {e}")
            return
        
        else:
            # Generate specific pose(s)
            target_poses = sys.argv[1].split(',')
    else:
        target_poses = list(poses.keys())
    
    # Load character
    char_path = f"{CHAR_DIR}/hero_01_action.jpg"
    if not os.path.exists(char_path):
        print(f"Character not found: {char_path}")
        return
    
    # Check for cached transparent version
    cached_path = f"{OUTPUT_DIR}/hero_transparent.png"
    if os.path.exists(cached_path):
        print("Loading cached transparent image...")
        char_no_bg = Image.open(cached_path).convert("RGBA")
    else:
        char_no_bg = load_and_remove_bg(char_path)
        char_no_bg.save(cached_path)
    
    # Extract parts
    print("Extracting body parts...")
    parts = extract_parts(char_no_bg)
    
    # Generate poses
    for pose_name in target_poses:
        pose_name = pose_name.strip()
        if pose_name in poses:
            canvas = generate_pose(pose_name, parts, poses)
            if canvas:
                out_path = f"{OUTPUT_DIR}/pose_{pose_name}.png"
                canvas.save(out_path)
                print(f"  ✅ {pose_name}: {out_path}")
    
    print("\n" + "=" * 50)
    print("Done!")

if __name__ == "__main__":
    main()