#!/usr/bin/env python3
"""
Character Asset Generator v2 - Fixed colors
Creates visible character parts with proper colors
"""
import os

ASSETS_DIR = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters"

# Colors (RGB) - BRIGHT COLORS for visibility
SKIN = (255, 180, 150)      # Peachy skin
SHIRT_BLUE = (50, 100, 230) # Bright blue
SHIRT_RED = (200, 30, 30)   # Bright red
SHIRT_GREEN = (50, 180, 80) # Bright green
PANTS = (30, 30, 60)        # Dark blue pants
BLACK = (20, 20, 20)        # Black
HAIR = (40, 25, 15)         # Dark brown

def create_ppm_rgb(width, height, pixels):
    """Create PPM with explicit RGB values."""
    ppm = f"P3\n{width} {height}\n255\n"
    for row in pixels:
        for r, g, b in row:
            ppm += f"{r} {g} {b} "
        ppm += "\n"
    return ppm

def fill_rect(pixels, x1, y1, x2, y2, color):
    for y in range(max(0, y1), min(len(pixels), y2)):
        for x in range(max(0, x1), min(len(pixels[0]), x2)):
            pixels[y][x] = color

def fill_circle(cx, cy, radius, color, pixels):
    for y in range(len(pixels)):
        for x in range(len(pixels[0])):
            if (x-cx)**2 + (y-cy)**2 <= radius**2:
                pixels[y][x] = color

# Character: Nomark (Blue shirt, dark pants)
def create_nomark():
    name = "nomark"
    W, H = 150, 250
    
    # Head
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_circle(75, 40, 35, SKIN, pixels)  # Face
    fill_rect(pixels, 40, 10, 110, 25, HAIR)  # Hair
    fill_rect(pixels, 55, 35, 70, 42, (30,30,30))  # Eye L
    fill_rect(pixels, 80, 35, 95, 42, (30,30,30))  # Eye R
    fill_rect(pixels, 60, 55, 90, 62, (180,80,80))  # Mouth
    
    out = f"{ASSETS_DIR}/{name}/parts_detailed"
    os.makedirs(out, exist_ok=True)
    with open(f"{out}/head.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/head.ppm")
    
    # Torso (blue shirt)
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 25, 70, 125, 200, SHIRT_BLUE)  # Body
    fill_rect(pixels, 60, 60, 90, 75, SKIN)  # Neck
    
    with open(f"{out}/torso.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/torso.ppm")
    
    # Left arm
    W, H = 40, 120
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 5, 0, 35, 50, SHIRT_BLUE)  # Upper
    fill_rect(pixels, 5, 45, 35, 110, SKIN)  # Lower + hand
    
    with open(f"{out}/left_arm.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/left_arm.ppm")
    
    # Right arm
    with open(f"{out}/right_arm.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/right_arm.ppm")
    
    # Legs
    W, H = 50, 150
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 5, 0, 22, 70, PANTS)  # Leg L
    fill_rect(pixels, 23, 0, 45, 70, PANTS)  # Leg R
    fill_rect(pixels, 2, 130, 24, 150, BLACK)  # Foot L
    fill_rect(pixels, 26, 130, 48, 150, BLACK)  # Foot R
    
    with open(f"{out}/leg.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/leg.ppm")

# Character: Villain (Red)
def create_villain():
    name = "villain"
    W, H = 150, 250
    
    # Head - more angular/evil
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_circle(75, 40, 35, SKIN, pixels)
    fill_rect(pixels, 40, 5, 110, 22, (20,10,10))  # Dark hair
    fill_rect(pixels, 50, 32, 68, 40, (30,30,30))  # Angry eyes
    fill_rect(pixels, 82, 32, 100, 40, (30,30,30))
    fill_rect(pixels, 60, 52, 90, 58, (100,30,30))  # Frown
    
    out = f"{ASSETS_DIR}/{name}/parts_detailed"
    os.makedirs(out, exist_ok=True)
    with open(f"{out}/head.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/head.ppm")
    
    # Torso (red)
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 25, 70, 125, 200, SHIRT_RED)
    fill_rect(pixels, 60, 60, 90, 75, SKIN)
    
    with open(f"{out}/torso.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/torso.ppm")
    
    # Arms
    W, H = 40, 120
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 5, 0, 35, 50, SHIRT_RED)
    fill_rect(pixels, 5, 45, 35, 110, SKIN)
    
    for arm in ["left_arm", "right_arm"]:
        with open(f"{out}/{arm}.ppm", "w") as f:
            f.write(create_ppm_rgb(W, H, pixels))
        print(f"Created {out}/{arm}.ppm")
    
    # Legs
    W, H = 50, 150
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 5, 0, 22, 70, BLACK)
    fill_rect(pixels, 23, 0, 45, 70, BLACK)
    fill_rect(pixels, 2, 130, 24, 150, BLACK)
    fill_rect(pixels, 26, 130, 48, 150, BLACK)
    
    with open(f"{out}/leg.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/leg.ppm")

# Character: Ally (Green)
def create_ally():
    name = "ally"
    W, H = 150, 250
    
    # Head
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_circle(75, 40, 35, SKIN, pixels)
    fill_rect(pixels, 40, 8, 110, 25, (60,40,20))  # Hair
    fill_rect(pixels, 55, 35, 70, 42, (30,30,30))
    fill_rect(pixels, 80, 35, 95, 42, (30,30,30))
    fill_rect(pixels, 62, 55, 88, 62, (150,100,100))
    
    out = f"{ASSETS_DIR}/{name}/parts_detailed"
    os.makedirs(out, exist_ok=True)
    with open(f"{out}/head.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/head.ppm")
    
    # Torso (green)
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 25, 70, 125, 200, SHIRT_GREEN)
    fill_rect(pixels, 60, 60, 90, 75, SKIN)
    
    with open(f"{out}/torso.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/torso.ppm")
    
    # Arms
    W, H = 40, 120
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 5, 0, 35, 50, SHIRT_GREEN)
    fill_rect(pixels, 5, 45, 35, 110, SKIN)
    
    for arm in ["left_arm", "right_arm"]:
        with open(f"{out}/{arm}.ppm", "w") as f:
            f.write(create_ppm_rgb(W, H, pixels))
        print(f"Created {out}/{arm}.ppm")
    
    # Legs
    W, H = 50, 150
    pixels = [[BLACK for _ in range(W)] for _ in range(H)]
    fill_rect(pixels, 5, 0, 22, 70, (50,50,60))
    fill_rect(pixels, 23, 0, 45, 70, (50,50,60))
    fill_rect(pixels, 2, 130, 24, 150, BLACK)
    fill_rect(pixels, 26, 130, 48, 150, BLACK)
    
    with open(f"{out}/leg.ppm", "w") as f:
        f.write(create_ppm_rgb(W, H, pixels))
    print(f"Created {out}/leg.ppm")

print("Generating V2 character assets with VISIBLE colors...")
print()
create_nomark()
print()
create_villain()
print()
create_ally()
print()
print("Converting to PNG...")