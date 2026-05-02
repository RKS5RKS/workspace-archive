#!/usr/bin/env python3
"""
Animation Generator - Creates walking animation from character parts
Pure Python + FFmpeg - no external image libraries needed
"""
import os
import math
import shutil

ASSETS = "/home/openclaw/.openclaw/workspace/comic_series/assets"
OUTPUT = "/home/openclaw/.openclaw/workspace/comic_series/assets/output/anim_walk"
CHAR_DIR = f"{ASSETS}/characters/nomark/parts_detailed"

# Colors
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0)  # We'll use black as transparent for now

def load_ppm(path):
    """Load PPM file into pixel array."""
    with open(path, 'r') as f:
        lines = f.readlines()
    
    # Parse header
    width, height = map(int, lines[1].split())
    
    # Parse pixels
    pixels = []
    data = lines[3].strip().split()
    for y in range(height):
        row = []
        for x in range(width):
            idx = (y * width + x) * 3
            r, g, b = int(data[idx]), int(data[idx+1]), int(data[idx+2])
            row.append((r, g, b))
        pixels.append(row)
    
    return pixels

def create_canvas(w, h, color=WHITE):
    """Create empty canvas."""
    return [[color for _ in range(w)] for _ in range(h)]

def composite(src, dest, x, y):
    """Composite source onto destination at position."""
    h, w = len(src), len(src[0])
    dest_h, dest_w = len(dest), len(dest[0])
    
    for sy in range(h):
        for sx in range(w):
            dx, dy = x + sx, y + sy
            if 0 <= dx < dest_w and 0 <= dy < dest_h:
                # Simple alpha: if not white, use it
                if src[sy][sx] != WHITE:
                    dest[dy][dx] = src[sy][sx]
    return dest

def save_ppm(pixels, path):
    """Save pixel array as PPM."""
    h, w = len(pixels), len(pixels[0])
    ppm = f"P3\n{w} {h}\n255\n"
    for row in pixels:
        for r, g, b in row:
            ppm += f"{r} {g} {b} "
        ppm += "\n"
    with open(path, 'w') as f:
        f.write(ppm)

# Animation settings
W, H = 640, 360
FPS = 12
FRAMES = 24  # 2 seconds

print("Loading character parts...")
head = load_ppm(f"{CHAR_DIR}/head.png")
torso = load_ppm(f"{CHAR_DIR}/torso.png")
arm_l = load_ppm(f"{CHAR_DIR}/left_arm.png")
arm_r = load_ppm(f"{CHAR_DIR}/right_arm.png")
leg = load_ppm(f"{CHAR_DIR}/leg.png")

print(f"Head: {len(head[0])}x{len(head)}, Torso: {len(torso[0])}x{len(torso)}")

# Create frames directory
os.makedirs(OUTPUT, exist_ok=True)
shutil.rmtree(f"{OUTPUT}/*")

print(f"Creating {FRAMES} animation frames...")

for frame in range(FRAMES):
    # Calculate walk cycle position
    walk_offset = int(math.sin(frame * 2 * math.pi / FRAMES) * 20)
    leg_offset_l = int(math.sin(frame * 2 * math.pi / FRAMES) * 10)
    leg_offset_r = int(math.sin((frame + FRAMES/2) * 2 * math.pi / FRAMES) * 10)
    
    # Create background (dark alley)
    canvas = create_canvas(W, H, (15, 15, 25))
    
    # Character position (center)
    cx, cy = W // 2 - 75, H // 2 - 100
    
    # Composite character parts
    # Legs
    composite(leg, canvas, cx + 15 + leg_offset_l, cy + 130)
    composite(leg, canvas, cx + 55 + leg_offset_r, cy + 130)
    
    # Torso
    composite(torso, canvas, cx, cy + 50)
    
    # Arms (swinging)
    arm_swing_l = int(math.sin((frame + FRAMES/2) * 2 * math.pi / FRAMES) * 15)
    arm_swing_r = int(math.sin(frame * 2 * math.pi / FRAMES) * 15)
    composite(arm_l, canvas, cx - 35 + arm_swing_l, cy + 55)
    composite(arm_r, canvas, cx + 85 + arm_swing_r, cy + 55)
    
    # Head
    composite(head, canvas, cx + 25, cy)
    
    # Save frame
    save_ppm(canvas, f"{OUTPUT}/frame_{frame:03d}.ppm")
    
    if frame % 6 == 0:
        print(f"  Frame {frame}/{FRAMES}")

print("Converting to video with FFmpeg...")

# Convert PPM to PNG then to video
os.makedirs(f"{OUTPUT}/png", exist_ok=True)

for f in range(FRAMES):
    ppm_file = f"{OUTPUT}/frame_{f:03d}.ppm"
    png_file = f"{OUTPUT}/png/frame_{f:03d}.png"
    os.system(f"ffmpeg -i {ppm_file} -frames:v 1 {png_file} -y 2>/dev/null")

# Create video
video_path = f"{ASSETS}/output/walking_character.mp4"
os.system(f"ffmpeg -framerate {FPS} -i {OUTPUT}/png/frame_%03d.png -c:v libx264 -pix_fmt yuv420p -vf scale=640:360 {video_path} -y 2>/dev/null")

print(f"Done! Video: {video_path}")

# Verify
import subprocess
result = subprocess.run(
    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
    capture_output=True, text=True
)
print(f"Duration: {result.stdout.strip()}s")