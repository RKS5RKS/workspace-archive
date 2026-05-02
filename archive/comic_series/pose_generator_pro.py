#!/usr/bin/env python3
"""
Proper Pose Generator - Uses background removal + part extraction + repositioning
"""
import os
import sys

# Set up environment for model caching
os.environ['HOME'] = '/home/openclaw/.openclaw/workspace/comic_series'
os.environ['XDG_CACHE_HOME'] = '/home/openclaw/.openclaw/workspace/comic_series/.cache'

from PIL import Image
from rembg import remove

BASE_DIR = "/home/openclaw/.openclaw/workspace/comic_series"
OUTPUT_DIR = f"{BASE_DIR}/generated_poses"
CHAR_DIR = f"{BASE_DIR}/character_concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
    
    # Define regions (proportional to image size)
    parts = {
        'head': (0.30 * w, 0.00 * h, 0.70 * w, 0.22 * h),
        'torso': (0.25 * w, 0.18 * h, 0.75 * h, 0.48 * h),
        'left_arm': (0.00 * w, 0.18 * h, 0.25 * w, 0.40 * h),
        'right_arm': (0.75 * w, 0.18 * h, 1.00 * w, 0.40 * h),
        'left_leg': (0.28 * w, 0.45 * h, 0.45 * w, 1.00 * h),
        'right_leg': (0.55 * w, 0.45 * h, 0.72 * w, 1.00 * h),
    }
    
    extracted = {}
    for name, (x1, y1, x2, y2) in parts.items():
        bbox = (int(x1), int(y1), int(x2), int(y2))
        part = char_img.crop(bbox)
        extracted[name] = part
        print(f"Extracted {name}: {part.size}")
    
    return extracted

def create_pose(parts, pose_name, positions):
    """
    Create a pose by positioning parts
    positions: dict of part_name -> (x, y) top-left position on canvas
    """
    # Canvas size matches original
    canvas = Image.new('RGBA', (1408, 768), (0, 0, 0, 0))
    
    for part_name, pos in positions.items():
        if part_name in parts:
            canvas.paste(parts[pos[0]], pos[1], parts[pos[0]])
    
    return canvas

def generate_poses(parts):
    """Generate all preset poses"""
    poses = {}
    
    # Base standing pose
    poses['standing'] = {
        'head': (422, 0),
        'torso': (352, 138),
        'left_arm': (70, 138),
        'right_arm': (1056, 138),
        'left_leg': (394, 346),
        'right_leg': (732, 346),
    }
    
    # Arms raised
    poses['arms_up'] = {
        'head': (422, 0),
        'torso': (352, 138),
        'left_arm': (70, 50),
        'right_arm': (1056, 50),
        'left_leg': (394, 346),
        'right_leg': (732, 346),
    }
    
    # Arms crossed
    poses['arms_crossed'] = {
        'head': (422, 0),
        'torso': (352, 138),
        'left_arm': (450, 180),
        'right_arm': (750, 180),
        'left_leg': (394, 346),
        'right_leg': (732, 346),
    }
    
    # Hands on hips
    poses['hands_hips'] = {
        'head': (422, 0),
        'torso': (352, 138),
        'left_arm': (250, 300),
        'right_arm': (930, 300),
        'left_leg': (394, 346),
        'right_leg': (732, 346),
    }
    
    # Victory pose
    poses['victory'] = {
        'head': (422, 0),
        'torso': (352, 138),
        'left_arm': (20, 20),
        'right_arm': (1150, 20),
        'left_leg': (394, 346),
        'right_leg': (732, 346),
    }
    
    # Walking
    poses['walking'] = {
        'head': (422, 20),
        'torso': (352, 150),
        'left_arm': (100, 180),
        'right_arm': (1000, 120),
        'left_leg': (350, 346),
        'right_leg': (780, 346),
    }
    
    return poses

def main():
    print("=" * 50)
    print("PROPER POSE GENERATOR")
    print("=" * 50)
    
    # Load character and remove background
    char_path = f"{CHAR_DIR}/hero_01_action.jpg"
    char_no_bg = load_and_remove_bg(char_path)
    
    # Save transparent version
    char_no_bg.save(f"{OUTPUT_DIR}/hero_transparent.png")
    print(f"Saved transparent: {OUTPUT_DIR}/hero_transparent.png")
    
    # Extract parts
    print("\nExtracting parts...")
    parts = extract_parts(char_no_bg)
    
    # Generate poses
    print("\nGenerating poses...")
    pose_configs = generate_poses(parts)
    
    for pose_name, positions in pose_configs.items():
        canvas = Image.new('RGBA', (1408, 768), (0, 0, 0, 0))
        
        for part_name, pos in positions.items():
            if part_name in parts:
                canvas.paste(parts[part_name], pos, parts[part_name])
        
        # Save
        out_path = f"{OUTPUT_DIR}/pose_{pose_name}.png"
        canvas.save(out_path)
        print(f"  ✅ {pose_name}: {out_path}")
    
    print("\n" + "=" * 50)
    print("DONE! Check:", OUTPUT_DIR)

if __name__ == "__main__":
    main()