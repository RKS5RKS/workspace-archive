#!/usr/bin/env python3
"""
Simple Character Asset Generator
Creates basic character parts that can be assembled into poses
"""
from PIL import Image, ImageDraw
import os

# --- Directories ---
OUTPUT_DIR_HERO_PARTS = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts"
OUTPUT_DIR_VILLAIN_PARTS = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters/villain/parts"
os.makedirs(OUTPUT_DIR_HERO_PARTS, exist_ok=True)
os.makedirs(OUTPUT_DIR_VILLAIN_PARTS, exist_ok=True)

# --- Colors ---
# Hero
SKIN_HERO = (220, 180, 140, 255)
SHIRT_HERO = (60, 80, 120, 255)
PANTS_HERO = (40, 50, 70, 255)
HAIR_HERO = (30, 20, 15, 255)

# Villain
SKIN_VILLAIN = (180, 140, 130, 255)  # pale
SUIT_VILLAIN = (30, 30, 40, 255)      # dark suit
PANTS_VILLAIN = (20, 20, 25, 255)     # darker pants
HAIR_VILLAIN = (10, 5, 5, 255)        # black

def create_body_part(name, width, height, color, output_path, shape="rect"):
    """Create a simple body part image"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if shape == "rect":
        draw.rounded_rectangle([0, 0, width-1, height-1], radius=20, fill=color)
    elif shape == "oval":
        draw.ellipse([0, 0, width-1, height-1], fill=color)
        draw.ellipse([0, 0, width-1, height-1], outline=(50, 50, 50, 255), width=2)
    elif shape == "round_rect":
        draw.rounded_rectangle([0, 0, width-1, height-1], radius=30, fill=color)
    
    # Add outline
    draw.rounded_rectangle([0, 0, width-1, height-1], radius=20, outline=(50, 50, 50, 255), width=3)
    
    img.save(f"{output_path}/{name}.png")
    print(f"  ✓ Created {name} at {output_path}/{name}.png")

# --- Create Hero Parts ---
print("=== Creating Hero Body Parts ===")
# Head (oval with hair)
head_hero = Image.new("RGBA", (120, 140), (0,0,0,0))
draw = ImageDraw.Draw(head_hero)
draw.ellipse([10, 10, 110, 130], fill=SKIN_HERO)  # face
draw.ellipse([0, 0, 120, 50], fill=HAIR_HERO)  # hair
head_hero.save(f"{OUTPUT_DIR_HERO_PARTS}/head.png")

# Torso, Arms, Legs
create_body_part("torso", 100, 140, SHIRT_HERO, OUTPUT_DIR_HERO_PARTS, "round_rect")
create_body_part("left_arm", 35, 130, SKIN_HERO, OUTPUT_DIR_HERO_PARTS, "rect")
create_body_part("right_arm", 35, 130, SKIN_HERO, OUTPUT_DIR_HERO_PARTS, "rect")
create_body_part("left_leg", 40, 160, PANTS_HERO, OUTPUT_DIR_HERO_PARTS, "rect")
create_body_part("right_leg", 40, 160, PANTS_HERO, OUTPUT_DIR_HERO_PARTS, "rect")
print("Hero parts created.")

# --- Create Villain Parts ---
print("\n=== Creating Villain Body Parts ===")
# Head (evil eyes)
head_villain = Image.new("RGBA", (120, 140), (0,0,0,0))
draw = ImageDraw.Draw(head_villain)
draw.ellipse([10, 15, 110, 130], fill=SKIN_VILLAIN) # face
draw.ellipse([5, 0, 115, 45], fill=HAIR_VILLAIN) # hair
# Evil eyes
draw.ellipse([30, 45, 50, 60], fill=(200, 50, 50, 255))
draw.ellipse([70, 45, 90, 60], fill=(200, 50, 50, 255))
head_villain.save(f"{OUTPUT_DIR_VILLAIN_PARTS}/head.png")

# Torso, Arms, Legs
create_body_part("torso", 110, 150, SUIT_VILLAIN, OUTPUT_DIR_VILLAIN_PARTS, "round_rect")
create_body_part("left_arm", 35, 135, SUIT_VILLAIN, OUTPUT_DIR_VILLAIN_PARTS, "rect")
create_body_part("right_arm", 35, 135, SUIT_VILLAIN, OUTPUT_DIR_VILLAIN_PARTS, "rect")
create_body_part("left_leg", 42, 165, PANTS_VILLAIN, OUTPUT_DIR_VILLAIN_PARTS, "rect")
create_body_part("right_leg", 42, 165, PANTS_VILLAIN, OUTPUT_DIR_VILLAIN_PARTS, "rect")
print("Villain parts created.")

print("\n=== All Character Parts Created! ===")
print(f"Hero parts saved to: {OUTPUT_DIR_HERO_PARTS}")
print(f"Villain parts saved to: {OUTPUT_DIR_VILLAIN_PARTS}")
print("\nThese can now be assembled into poses using the rig system.")