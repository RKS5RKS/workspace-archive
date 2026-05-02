#!/usr/bin/env python3
"""
Pose Editor Tool - Create different poses from a character image
by cutting into regions and repositioning them
"""
import os
import sys
from PIL import Image, ImageDraw, ImageOps

BASE_DIR = "/home/openclaw/.openclaw/workspace/comic_series"
OUTPUT_DIR = f"{BASE_DIR}/generated_poses"
CHAR_DIR = f"{BASE_DIR}/character_concepts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_character(path):
    """Load character image"""
    img = Image.open(path).convert("RGBA")
    print(f"Loaded: {img.size}")
    return img

def define_regions(width, height):
    """Define body regions for a typical standing character"""
    # These are relative coordinates (0-1 range)
    regions = {
        "head": (0.3, 0.0, 0.7, 0.25),
        "torso": (0.25, 0.2, 0.75, 0.55),
        "left_arm": (0.0, 0.2, 0.3, 0.45),
        "right_arm": (0.7, 0.2, 1.0, 0.45),
        "left_leg": (0.3, 0.5, 0.45, 1.0),
        "right_leg": (0.55, 0.5, 0.7, 1.0),
    }
    # Convert to pixel coords
    pixel_regions = {}
    for name, (x1, y1, x2, y2) in regions.items():
        pixel_regions[name] = (
            int(x1 * width),
            int(y1 * height),
            int(x2 * width),
            int(y2 * height)
        )
    return pixel_regions

def extract_region(img, bbox):
    """Extract a region from the image"""
    return img.crop(bbox)

def paste_region(base, region, pos):
    """Paste a region onto base at position"""
    result = base.copy()
    result.paste(region, pos, region)
    return result

def create_pose_variation(base_img, regions, pose_name, offsets):
    """
    Create a pose variation by moving regions
    offsets: dict of region_name -> (dx, dy) displacement
    """
    width, height = base_img.size
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # First, paste the original image as background (we'll mask later)
    # Actually, let's work with the original and overlay moved parts
    
    result = base_img.copy()
    
    for region_name, (dx, dy) in offsets.items():
        if region_name not in regions:
            continue
        
        bbox = regions[region_name]
        
        # Extract the region
        region_img = base_img.crop(bbox)
        
        # Calculate new position
        new_x = bbox[0] + dx
        new_y = bbox[1] + dy
        
        # Clear the original area (make transparent)
        # Create a mask for the region
        mask = region_img.split()[3] if region_img.mode == "RGBA" else None
        
        # Paste the moved region
        if dx != 0 or dy != 0:
            # For simplicity, we just overlay - this is a basic version
            # A real tool would need proper compositing
            result.paste(region_img, (new_x, new_y), mask)
    
    return result

def generate_preset_poses(base_img, regions):
    """Generate preset pose variations"""
    poses = []
    
    # Pose 1: Arms up
    offsets = {
        "left_arm": (-30, -40),
        "right_arm": (30, -40),
    }
    pose_img = create_pose_variation(base_img, regions, "arms_up", offsets)
    poses.append(("pose_arms_up.png", pose_img))
    
    # Pose 2: Arms crossed
    offsets = {
        "left_arm": (20, 10),
        "right_arm": (-20, 10),
    }
    pose_img = create_pose_variation(base_img, regions, "arms_crossed", offsets)
    poses.append(("pose_arms_crossed.png", pose_img))
    
    # Pose 3: Legs apart
    offsets = {
        "left_leg": (-20, 0),
        "right_leg": (20, 0),
    }
    pose_img = create_pose_variation(base_img, regions, "legs_apart", offsets)
    poses.append(("pose_legs_apart.png", pose_img))
    
    # Pose 4: Leaning right
    offsets = {
        "torso": (15, 0),
        "head": (15, 0),
        "left_arm": (10, 0),
        "right_arm": (10, 0),
    }
    pose_img = create_pose_variation(base_img, regions, "lean_right", offsets)
    poses.append(("pose_lean_right.png", pose_img))
    
    # Pose 5: Leaning left
    offsets = {
        "torso": (-15, 0),
        "head": (-15, 0),
        "left_arm": (-10, 0),
        "right_arm": (-10, 0),
    }
    pose_img = create_pose_variation(base_img, regions, "lean_left", offsets)
    poses.append(("pose_lean_left.png", pose_img))
    
    # Pose 6: Hands on hips
    offsets = {
        "left_arm": (25, 15),
        "right_arm": (-25, 15),
    }
    pose_img = create_pose_variation(base_img, regions, "hands_hips", offsets)
    poses.append(("pose_hands_hips.png", pose_img))
    
    # Pose 7: Knees bent
    offsets = {
        "left_leg": (0, 20),
        "right_leg": (0, 10),
    }
    pose_img = create_pose_variation(base_img, regions, "knees_bent", offsets)
    poses.append(("pose_knees_bent.png", pose_img))
    
    # Pose 8: Head tilt
    offsets = {
        "head": (0, 0),
    }
    pose_img = create_pose_variation(base_img, regions, "head_tilt", offsets)
    # Actually rotate head
    head_region = base_img.crop(regions["head"])
    head_rotated = head_region.rotate(15)
    pose_img = base_img.copy()
    pose_img.paste(head_rotated, (regions["head"][0], regions["head"][1]), head_rotated)
    poses.append(("pose_head_tilt.png", pose_img))
    
    return poses

def main():
    print("🎭 Pose Editor Tool")
    print("=" * 50)
    
    # Load base character
    base_char = f"{CHAR_DIR}/hero_01_action.jpg"
    
    if not os.path.exists(base_char):
        print(f"Character not found: {base_char}")
        # Try any jpg in character_concepts
        import glob
        candidates = glob.glob(f"{CHAR_DIR}/*.jpg")
        if candidates:
            base_char = candidates[0]
            print(f"Using: {base_char}")
        else:
            print("No character images found!")
            return
    
    base_img = load_character(base_char)
    width, height = base_img.size
    
    # Define body regions
    regions = define_regions(width, height)
    print(f"Character size: {width}x{height}")
    print(f"Regions: {list(regions.keys())}")
    
    # Generate pose variations
    print("\n🔄 Generating pose variations...")
    poses = generate_preset_poses(base_img, regions)
    
    # Save poses
    for filename, pose_img in poses:
        out_path = f"{OUTPUT_DIR}/{filename}"
        pose_img.convert("RGB").save(out_path, "JPEG", quality=95)
        print(f"   ✅ {filename}")
    
    print(f"\n🎉 Generated {len(poses)} poses in: {OUTPUT_DIR}")
    print("\nYou can now composite these into scenes!")

if __name__ == "__main__":
    main()