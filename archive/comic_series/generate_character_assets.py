#!/usr/bin/env python3
"""
Character Asset Generator
Creates more detailed character parts using PIL
"""
import os
from PIL import Image, ImageDraw, ImageFilter

# Configuration
OUTPUT_DIR = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters"

def create_detailed_head(outfit_name, skin_tone=(255, 220, 177), expression="neutral"):
    """Create a detailed head shape"""
    img = Image.new('RGBA', (200, 250), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Head shape (oval with slight jaw)
    head_color = skin_tone + (255,)
    
    # Main head
    draw.ellipse([30, 20, 170, 200], fill=head_color)
    
    # Jaw line
    draw.arc([50, 120, 150, 200], start=0, end=180, fill=skin_tone + (200,), width=3)
    
    # Eyes
    eye_color = (50, 30, 20, 255)
    # Left eye
    draw.ellipse([55, 80, 85, 105], fill=(255, 255, 255, 255))
    draw.ellipse([65, 88, 78, 100], fill=eye_color)
    draw.ellipse([68, 90, 73, 95], fill=(0, 0, 0, 255))  # pupil
    # Right eye  
    draw.ellipse([115, 80, 145, 105], fill=(255, 255, 255, 255))
    draw.ellipse([122, 88, 135, 100], fill=eye_color)
    draw.ellipse([127, 90, 132, 95], fill=(0, 0, 0, 255))
    
    # Eyebrows
    draw.line([(50, 70), (90, 65)], fill=(60, 40, 20, 255), width=4)
    draw.line([(110, 65), (150, 70)], fill=(60, 40, 20, 255), width=4)
    
    # Nose
    draw.line([(100, 95), (95, 120), (105, 120)], fill=(skin_tone[0]-20, skin_tone[1]-20, skin_tone[2]-20, 200), width=3)
    
    # Mouth based on expression
    if expression == "neutral":
        draw.line([(80, 145), (120, 145)], fill=(180, 100, 100, 255), width=3)
    elif expression == "happy":
        draw.arc([75, 135, 125, 160], start=0, end=180, fill=(200, 80, 80, 255), width=4)
    elif expression == "angry":
        draw.line([(75, 155), (95, 145)], fill=(180, 80, 80, 255), width=3)
        draw.line([(125, 155), (105, 145)], fill=(180, 80, 80, 255), width=3)
    elif expression == "talking":
        draw.ellipse([85, 140, 115, 160], fill=(150, 50, 50, 255))
    
    # Hair (simple style)
    hair_color = (40, 25, 15, 255)
    draw.ellipse([25, 10, 175, 70], fill=hair_color)
    draw.ellipse([35, 0, 100, 40], fill=hair_color)
    
    # Ears
    draw.ellipse([20, 90, 40, 130], fill=head_color)
    draw.ellipse([160, 90, 180, 130], fill=head_color)
    
    return img

def create_detailed_torso(outfit_name="shirt", shirt_color=(50, 100, 200)):
    """Create a detailed torso"""
    img = Image.new('RGBA', (200, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Body shape (rounded rectangle)
    torso_color = shirt_color + (255,)
    draw.rounded_rectangle([30, 0, 170, 280], radius=20, fill=torso_color)
    
    # Neck
    neck_color = (255, 220, 177, 255)
    draw.rectangle([80, -30, 120, 30], fill=neck_color)
    
    # Shoulders
    draw.ellipse([20, 10, 60, 60], fill=shirt_color)
    draw.ellipse([140, 10, 180, 60], fill=shirt_color)
    
    # Collar detail
    draw.polygon([(80, 0), (100, 30), (120, 0)], fill=(shirt_color[0]-30, shirt_color[1]-30, shirt_color[2]-30, 255))
    
    return img

def create_detailed_arm(side="left", arm_color=(255, 220, 177), sleeve_color=(50, 100, 200)):
    """Create a detailed arm"""
    img = Image.new('RGBA', (80, 250), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Upper arm (sleeve)
    if side == "left":
        draw.rounded_rectangle([0, 0, 60, 100], radius=15, fill=sleeve_color)
        # Lower arm (skin)
        draw.rounded_rectangle([10, 90, 55, 200], radius=12, fill=arm_color)
        # Hand
        draw.ellipse([15, 190, 50, 240], fill=arm_color)
    else:
        draw.rounded_rectangle([20, 0, 80, 100], radius=15, fill=sleeve_color)
        draw.rounded_rectangle([25, 90, 70, 200], radius=12, fill=arm_color)
        draw.ellipse([30, 190, 65, 240], fill=arm_color)
    
    return img

def create_detailed_leg(pants_color=(40, 50, 80)):
    """Create a detailed leg"""
    img = Image.new('RGBA', (100, 350), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Upper leg (pants)
    draw.rounded_rectangle([10, 0, 90, 150], radius=10, fill=pants_color)
    
    # Lower leg (pants)
    draw.rounded_rectangle([10, 140, 45, 330], radius=8, fill=pants_color)
    draw.rounded_rectangle([55, 140, 90, 330], radius=8, fill=pants_color)
    
    # Shoes
    shoe_color = (30, 30, 30, 255)
    draw.ellipse([5, 320, 50, 350], fill=shoe_color)
    draw.ellipse([50, 320, 95, 350], fill=shoe_color)
    
    return img

def create_detailed_foot():
    """Create a detailed foot"""
    img = Image.new('RGBA', (100, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Shoe shape
    draw.ellipse([0, 0, 90, 45], fill=(30, 30, 30, 255))
    draw.ellipse([70, 10, 100, 40], fill=(30, 30, 30, 255))
    
    return img

def create_detailed_hand(skin_tone=(255, 220, 177)):
    """Create a detailed hand"""
    img = Image.new('RGBA', (60, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Palm
    draw.ellipse([10, 20, 50, 70], fill=skin_tone + (255,))
    
    # Fingers
    draw.ellipse([5, 0, 20, 30], fill=skin_tone + (255,))
    draw.ellipse([18, -5, 32, 25], fill=skin_tone + (255,))
    draw.ellipse([31, -2, 44, 28], fill=skin_tone + (255,))
    draw.ellipse([43, 5, 55, 35], fill=skin_tone + (255,))
    
    return img

def generate_character_set(character_name, base_path):
    """Generate a complete character asset set"""
    char_path = os.path.join(base_path, character_name, "parts_detailed")
    os.makedirs(char_path, exist_ok=True)
    
    print(f"Generating {character_name}...")
    
    # Define character colors based on name
    if character_name == "nomark":
        skin = (255, 220, 177)
        shirt = (50, 100, 200)  # Blue
        pants = (40, 50, 80)    # Dark blue
    elif character_name == "villain":
        skin = (180, 140, 120)
        shirt = (80, 20, 20)    # Red/dark
        pants = (20, 20, 20)    # Black
    elif character_name == "ally":
        skin = (160, 120, 90)
        shirt = (50, 150, 80)   # Green
        pants = (50, 50, 60)    # Gray
    else:
        skin = (255, 220, 177)
        shirt = (100, 100, 100)
        pants = (40, 40, 40)
    
    # Generate parts
    # Head
    head = create_detailed_head(character_name, skin, "neutral")
    head.save(os.path.join(char_path, "head.png"))
    print(f"  ✓ head.png")
    
    # Head expressions
    for expr in ["happy", "angry", "talking"]:
        head_expr = create_detailed_head(character_name, skin, expr)
        head_expr.save(os.path.join(char_path, f"head_{expr}.png"))
        print(f"  ✓ head_{expr}.png")
    
    # Torso
    torso = create_detailed_torso(character_name, shirt)
    torso.save(os.path.join(char_path, "torso.png"))
    print(f"  ✓ torso.png")
    
    # Arms
    for side in ["left", "right"]:
        arm = create_detailed_arm(side, skin, shirt)
        arm.save(os.path.join(char_path, f"{side}_arm.png"))
        print(f"  ✓ {side}_arm.png")
        
        # Lower arm (without sleeve)
        lower_arm = create_detailed_arm(side, skin, (0, 0, 0, 0))
        lower_arm.save(os.path.join(char_path, f"{side}_lower_arm.png"))
        print(f"  ✓ {side}_lower_arm.png")
    
    # Hands
    for side in ["left", "right"]:
        hand = create_detailed_hand(skin)
        hand.save(os.path.join(char_path, f"{side}_hand.png"))
        print(f"  ✓ {side}_hand.png")
    
    # Legs
    leg = create_detailed_leg(pants)
    leg.save(os.path.join(char_path, "leg.png"))
    print(f"  ✓ leg.png")
    
    # Split leg into upper/lower
    upper_leg = create_detailed_leg(pants).crop((0, 0, 100, 150))
    upper_leg.save(os.path.join(char_path, "upper_leg.png"))
    lower_leg = create_detailed_leg(pants).crop((0, 140, 100, 350))
    lower_leg.save(os.path.join(char_path, "lower_leg.png"))
    print(f"  ✓ upper_leg.png, lower_leg.png")
    
    # Feet
    for side in ["left", "right"]:
        foot = create_detailed_foot()
        foot.save(os.path.join(char_path, f"{side}_foot.png"))
        print(f"  ✓ {side}_foot.png")
    
    print(f"{character_name} complete!")

if __name__ == "__main__":
    base = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters"
    
    for char in ["nomark", "villain", "ally"]:
        generate_character_set(char, base)
    
    print("\n✅ All character assets generated!")