#!/bin/bash
cd /home/openclaw/.openclaw/workspace/comic_series
source ./venv/bin/activate
export HOME=/home/openclaw/.openclaw/workspace/comic_series
export XDG_CACHE_HOME=/home/openclaw/.openclaw/workspace/comic_series/.cache

# Process hero images
python3 << 'PYTHON'
import os
from rembg import remove
from PIL import Image

chars_dir = "/home/openclaw/.openclaw/workspace/comic_series/character_concepts"
output_dir = "/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/poses"

hero_images = [
    "hero_01_action.jpg",
    "hero_01_combat.jpg", 
    "hero_01_aiming.jpg"
]

for img_name in hero_images:
    input_path = os.path.join(chars_dir, img_name)
    if os.path.exists(input_path):
        output_name = img_name.replace(".jpg", "_no_bg.png")
        output_path = os.path.join(output_dir, output_name)
        print(f"Processing: {img_name}")
        img = Image.open(input_path)
        result = remove(img)
        result.save(output_path)
        print(f"  → Saved: {output_name}")

print("Done processing hero images")
PYTHON
