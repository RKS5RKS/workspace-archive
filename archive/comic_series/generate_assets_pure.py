#!/usr/bin/env python3
"""
Pure Python Character Asset Generator
Creates PPM (Portable Pixel Map) images without external dependencies.
PPM is a simple text-based image format.
"""
import os
import math

ASSETS_DIR = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters"

# Colors (RGB)
SKIN = (255, 204, 181)      # #ffccb1
SHIRT_BLUE = (50, 100, 200) # #3264c8
SHIRT_RED = (128, 16, 16)   # #801010
SHIRT_GREEN = (50, 150, 80) # #329650
PANTS_DARK = (40, 50, 80)   # #283250
PANTS_BLACK = (20, 20, 20)  # #141414
HAIR = (40, 25, 15)         # #28190f
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIPS = (180, 100, 100)

def create_ppm(width, height, pixels):
    """Create PPM data string from pixel array."""
    ppm_data = f"P3\n{width} {height}\n255\n"
    for row in pixels:
        for r, g, b in row:
            ppm_data += f"{r} {g} {b} "
        ppm_data += "\n"
    return ppm_data

def draw_circle(cx, cy, radius, color, width, height, pixels):
    """Draw a filled circle on the pixel array."""
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            if dist <= radius:
                pixels[y][x] = color
    return pixels

def draw_rect(x1, y1, x2, y2, color, width, height, pixels):
    """Draw a filled rectangle on the pixel array."""
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            pixels[y][x] = color
    return pixels

# Character dimensions
W, H = 150, 300

def create_head(name):
    """Create head as PPM."""
    pixels = [[WHITE for _ in range(W)] for _ in range(H)]
    
    # Head circle
    draw_circle(75, 50, 40, SKIN, W, H, pixels)
    
    # Hair
    draw_rect(35, 20, 115, 45, HAIR, W, H, pixels)
    
    # Eyes (white + black pupils)
    draw_rect(50, 45, 70, 60, WHITE, W, H, pixels)
    draw_rect(80, 45, 100, 60, WHITE, W, H, pixels)
    draw_rect(55, 50, 65, 58, BLACK, W, H, pixels)
    draw_rect(85, 50, 95, 58, BLACK, W, H, pixels)
    
    # Lips
    draw_rect(60, 75, 90, 85, LIPS, W, H, pixels)
    
    # Save
    ppm = create_ppm(W, H, pixels)
    out_dir = f"{ASSETS_DIR}/{name}/parts_detailed"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/head.ppm", "w") as f:
        f.write(ppm)
    print(f"Created {out_dir}/head.ppm")

def create_torso(name, color):
    """Create torso as PPM."""
    pixels = [[WHITE for _ in range(W)] for _ in range(H)]
    
    # Main torso
    draw_rect(30, 90, 120, 220, color, W, H, pixels)
    
    # Neck
    draw_rect(60, 80, 90, 100, SKIN, W, H, pixels)
    
    # Collar line
    draw_rect(30, 90, 120, 95, (100, 100, 100), W, H, pixels)
    
    # Save
    ppm = create_ppm(W, H, pixels)
    out_dir = f"{ASSETS_DIR}/{name}/parts_detailed"
    with open(f"{out_dir}/torso.ppm", "w") as f:
        f.write(ppm)
    print(f"Created {out_dir}/torso.ppm")

def create_arm(name, color, side):
    """Create arm as PPM."""
    pixels = [[WHITE for _ in range(50)] for _ in range(150)]
    
    # Upper arm (shirt color)
    draw_rect(5, 0, 45, 60, color, 50, 150, pixels)
    
    # Lower arm (skin)
    draw_rect(5, 50, 40, 120, SKIN, 50, 150, pixels)
    
    # Hand
    draw_rect(5, 110, 40, 145, SKIN, 50, 150, pixels)
    
    # Save
    ppm = create_ppm(50, 150, pixels)
    out_dir = f"{ASSETS_DIR}/{name}/parts_detailed"
    with open(f"{out_dir}/{side}_arm.ppm", "w") as f:
        f.write(ppm)
    print(f"Created {out_dir}/{side}_arm.ppm")

def create_leg(name, color):
    """Create leg as PPM."""
    pixels = [[WHITE for _ in range(80)] for _ in range(200)]
    
    # Thigh
    draw_rect(5, 0, 35, 90, color, 80, 200, pixels)
    
    # Lower leg
    draw_rect(5, 80, 35, 180, color, 80, 200, pixels)
    
    # Foot
    draw_rect(0, 170, 40, 200, (30, 30, 30), 80, 200, pixels)
    
    # Save
    ppm = create_ppm(80, 200, pixels)
    out_dir = f"{ASSETS_DIR}/{name}/parts_detailed"
    with open(f"{out_dir}/leg.ppm", "w") as f:
        f.write(ppm)
    print(f"Created {out_dir}/leg.ppm")

# Generate for all characters
print("Generating character assets with pure Python...")
print()

print("Creating Nomark...")
create_head("nomark")
create_torso("nomark", SHIRT_BLUE)
create_arm("nomark", SHIRT_BLUE, "left")
create_arm("nomark", SHIRT_BLUE, "right")
create_leg("nomark", PANTS_DARK)

print("Creating Villain...")
create_head("villain")
create_torso("villain", SHIRT_RED)
create_arm("villain", SHIRT_RED, "left")
create_arm("villain", SHIRT_RED, "right")
create_leg("villain", PANTS_BLACK)

print("Creating Ally...")
create_head("ally")
create_torso("ally", SHIRT_GREEN)
create_arm("ally", SHIRT_GREEN, "left")
create_arm("ally", SHIRT_GREEN, "right")
create_leg("ally", (50, 50, 60))

print()
print("Done! PPM files created.")
print("Converting to PNG with FFmpeg...")