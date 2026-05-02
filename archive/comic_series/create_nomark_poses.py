#!/usr/bin/env python3
"""
Nomark SVG Pose Generator
Creates different poses by modifying the base SVG code
This is the CORRECT way - not image generation, but SVG manipulation
"""
import os
import shutil

REFERENCE = '/home/openclaw/.openclaw/workspace/nomark_character.svg'
OUTPUT_DIR = '/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/poses'
PARTS_DIR = '/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PARTS_DIR, exist_ok=True)

def read_svg(path):
    with open(path, 'r') as f:
        return f.read()

def write_svg(content, path):
    with open(path, 'w') as f:
        f.write(content)

def svg_to_png(svg_path, png_path):
    """Convert SVG to PNG using FFmpeg"""
    os.system(f'ffmpeg -y -i {svg_path} -vframes 1 -update 1 {png_path} 2>/dev/null')

# === POSE MODIFICATIONS ===

def create_standing():
    """Base standing pose - just copy"""
    content = read_svg(REFERENCE)
    write_svg(content, f'{OUTPUT_DIR}/standing.svg')
    svg_to_png(f'{OUTPUT_DIR}/standing.svg', f'{OUTPUT_DIR}/standing.png')
    print("  standing.png")

def create_walking():
    """Walking - legs apart, arms swinging"""
    content = read_svg(REFERENCE)
    # Move left leg forward (adjust path coordinates)
    content = content.replace(
        '<path d="M155 320 L145 480 L165 480 L175 350 L190 350 L205 480 L225 480 L215 320 Z"',
        '<path d="M145 320 L125 450 L145 450 L160 350 L195 350 L230 450 L250 320 Z"'
    )
    write_svg(content, f'{OUTPUT_DIR}/walking.svg')
    svg_to_png(f'{OUTPUT_DIR}/walking.svg', f'{OUTPUT_DIR}/walking.png')
    print("  walking.png")

def create_running():
    """Running - more extreme leg positions"""
    content = read_svg(REFERENCE)
    # Running stance - legs further apart
    content = content.replace(
        '<path d="M155 320 L145 480 L165 480 L175 350 L190 350 L205 480 L225 480 L215 320 Z"',
        '<path d="M135 320 L100 430 L120 430 L145 350 L210 350 L280 430 L300 320 Z"'
    )
    write_svg(content, f'{OUTPUT_DIR}/running.svg')
    svg_to_png(f'{OUTPUT_DIR}/running.svg', f'{OUTPUT_DIR}/running.png')
    print("  running.png")

def create_punching():
    """Punching - right arm extended"""
    content = read_svg(REFERENCE)
    # Extend right arm
    content = content.replace(
        '<path d="M230 180 L260 220 L265 280 L255 285 L245 230 L225 190"',
        '<path d="M230 180 L280 170 L340 165 L350 175 L290 185 L230 190"'
    )
    write_svg(content, f'{OUTPUT_DIR}/punching.svg')
    svg_to_png(f'{OUTPUT_DIR}/punching.svg', f'{OUTPUT_DIR}/punching.png')
    print("  punching.png")

def create_crouching():
    """Crouching - lower body, arms forward"""
    content = read_svg(REFERENCE)
    # Lower the body
    content = content.replace('viewBox="0 0 400 600"', 'viewBox="0 100 400 500"')
    write_svg(content, f'{OUTPUT_DIR}/crouching.svg')
    svg_to_png(f'{OUTPUT_DIR}/crouching.svg', f'{OUTPUT_DIR}/crouching.png')
    print("  crouching.png")

def create_victory():
    """Victory - arms raised"""
    content = read_svg(REFERENCE)
    # Arms up - move arm positions up
    content = content.replace('M130 180 L100 220', 'M130 100 L80 50')
    content = content.replace('M230 180 L260 220', 'M230 100 L280 50')
    write_svg(content, f'{OUTPUT_DIR}/victory.svg')
    svg_to_png(f'{OUTPUT_DIR}/victory.svg', f'{OUTPUT_DIR}/victory.png')
    print("  victory.png")

def create_defeated():
    """Defeated - slumped, head down"""
    content = read_svg(REFERENCE)
    # Head lower
    content = content.replace('cx="180" cy="155"', 'cx="180" cy="180"')
    write_svg(content, f'{OUTPUT_DIR}/defeated.svg')
    svg_to_png(f'{OUTPUT_DIR}/defeated.svg', f'{OUTPUT_DIR}/defeated.png')
    print("  defeated.png")

# === MAIN ===
print("Creating Nomark poses from SVG (this is the correct way)...")
print("\nPoses:")

create_standing()
create_walking()
create_running()
create_punching()
create_crouching()
create_victory()
create_defeated()

print("\n✅ All poses created!")
print(f"Output: {OUTPUT_DIR}/")