#!/usr/bin/env python3
"""
Character Pose Generator - Creates poses from a base character image
Uses ffmpeg for image manipulation (no AI generation)
"""
import os
import subprocess
import json

BASE_DIR = "/home/openclaw/.openclaw/workspace/comic_series"
OUTPUT_DIR = f"{BASE_DIR}/generated_poses"
CHAR_DIR = f"{BASE_DIR}/character_concepts"
LOC_DIR = f"{BASE_DIR}/locations"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_ffmpeg(cmd):
    """Run ffmpeg command"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        return False
    return True

def generate_poses(base_char_path, output_prefix="pose"):
    """Generate multiple poses from a base character image"""
    poses = []
    
    # 1. Original (base)
    out_file = f"{OUTPUT_DIR}/{output_prefix}_01_original.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 2. Horizontal flip (mirror)
    out_file = f"{OUTPUT_DIR}/{output_prefix}_02_mirror.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "hflip,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 3. Zoomed in (tight crop)
    out_file = f"{OUTPUT_DIR}/{output_prefix}_03_zoom.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "scale=iw*1.5:ih*1.5,crop=1280:720:100:0,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 4. Rotated slightly right
    out_file = f"{OUTPUT_DIR}/{output_prefix}_04_rotated_right.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "rotate=5*PI/180,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 5. Rotated slightly left
    out_file = f"{OUTPUT_DIR}/{output_prefix}_05_rotated_left.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "rotate=-5*PI/180,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 6. Different crop - upper body
    out_file = f"{OUTPUT_DIR}/{output_prefix}_06_upper_body.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "crop=720:720:280:0,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 7. Different crop - focused on character
    out_file = f"{OUTPUT_DIR}/{output_prefix}_07_focused.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "crop=800:800:240:0,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 8. Flipped + zoomed
    out_file = f"{OUTPUT_DIR}/{output_prefix}_08_mirror_zoom.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "hflip,scale=iw*1.3:ih*1.3,crop=1280:720:50:0,scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 9. Tilted right
    out_file = f"{OUTPUT_DIR}/{output_prefix}_09_tilt_right.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "rotate=10*PI/180:ow=hypot(ow,oh):oh=hypot(ow,oh),scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 10. Tilted left
    out_file = f"{OUTPUT_DIR}/{output_prefix}_10_tilt_left.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "rotate=-10*PI/180:ow=hypot(ow,oh):oh=hypot(ow,oh),scale=1280:720", out_file]):
        poses.append(out_file)
    
    # 11. Wide shot (zoomed out)
    out_file = f"{OUTPUT_DIR}/{output_prefix}_11_wide.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "scale=iw*0.8:ih*0.8,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black", out_file]):
        poses.append(out_file)
    
    # 12. Lower crop (legs focus)
    out_file = f"{OUTPUT_DIR}/{output_prefix}_12_lower.jpg"
    if run_ffmpeg(["ffmpeg", "-y", "-i", base_char_path, "-vf", "crop=720:720:280:200,scale=1280:720", out_file]):
        poses.append(out_file)
    
    return poses

def composite_scene(location_path, character_path, output_path, char_x=400, char_y=200, char_scale=0.5):
    """Composite character into a scene"""
    # Scale character
    temp_char = f"{OUTPUT_DIR}/temp_char_scaled.jpg"
    scale_factor = int(1280 * char_scale)
    run_ffmpeg(["ffmpeg", "-y", "-i", character_path, "-vf", f"scale={scale_factor}:-1", temp_char])
    
    # Overlay on location
    cmd = [
        "ffmpeg", "-y",
        "-i", location_path,
        "-i", temp_char,
        "-filter_complex", f"overlay={char_x}:{char_y}",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Cleanup temp
    if os.path.exists(temp_char):
        os.remove(temp_char)
    
    return result.returncode == 0

def create_video_from_images(image_paths, output_path, duration_per_image=2):
    """Create video from sequence of images"""
    # Create concat file
    concat_file = f"{OUTPUT_DIR}/concat_list.txt"
    with open(concat_file, "w") as f:
        for img in image_paths:
            f.write(f"file '{img}'\n")
            f.write(f"duration {duration_per_image}\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",
        "-shortest",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(concat_file)
    return result.returncode == 0

def main():
    print("🎭 Character Pose Generator")
    print("=" * 40)
    
    # Use an existing character as base
    base_char = f"{CHAR_DIR}/hero_01_action.jpg"
    
    if not os.path.exists(base_char):
        print(f"Base character not found: {base_char}")
        return
    
    print(f"📷 Using base character: {base_char}")
    
    # Generate poses
    print("\n🔄 Generating poses...")
    poses = generate_poses(base_char, "hero_demo")
    
    print(f"✅ Generated {len(poses)} poses:")
    for p in poses:
        print(f"   - {os.path.basename(p)}")
    
    # Create demo video
    print("\n🎬 Creating demo video...")
    demo_video = f"{OUTPUT_DIR}/hero_demo_video.mp4"
    if create_video_from_images(poses, demo_video, duration_per_image=1.5):
        size = os.path.getsize(demo_video)
        print(f"✅ Demo video created: {demo_video} ({size/1024:.1f}KB)")
    
    # Composite demo
    print("\n🏠 Creating scene composite...")
    locations = [
        f"{LOC_DIR}/futuristic_street_night.jpg",
        f"{LOC_DIR}/spaceship_hangar.jpg",
        f"{LOC_DIR}/abandoned_factory.jpg"
    ]
    
    for i, loc in enumerate(locations[:2]):  # Just first 2 for demo
        out_scene = f"{OUTPUT_DIR}/scene_{i+1}_composite.jpg"
        if composite_scene(loc, poses[0], out_scene, char_x=300+100*i, char_y=150, char_scale=0.4):
            print(f"   ✅ {os.path.basename(out_scene)}")
    
    print("\n" + "=" * 40)
    print("🎉 Pose generation complete!")
    print(f"📁 Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()