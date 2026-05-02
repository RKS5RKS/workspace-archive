"""Example usage of the SceneComposer.

This script demonstrates how to:
1. Set up minimal placeholder assets if they do not exist.
2. Create a simple scene with a hero character walking on a background.
3. Export the scene to a video file (output.mp4).
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw

# Ensure the placeholder assets exist
def create_placeholder_assets(root: str = "assets"):
    # Background
    locations_dir = Path(root) / "locations"
    locations_dir.mkdir(parents=True, exist_ok=True)
    bg_path = locations_dir / "scene1.png"
    if not bg_path.is_file():
        bg = Image.new("RGBA", (640, 360), (135, 206, 235, 255))  # sky blue
        draw = ImageDraw.Draw(bg)
        draw.rectangle([0, 250, 640, 360], fill=(34, 139, 34, 255))  # ground
        bg.save(bg_path)
        print(f"Created placeholder background: {bg_path}")

    # Character frames
    char_dir = Path(root) / "characters" / "hero" / "parts_detailed"
    char_dir.mkdir(parents=True, exist_ok=True)
    # idle frame
    idle_path = char_dir / "idle_0.png"
    if not idle_path.is_file():
        char = Image.new("RGBA", (100, 200), (255, 0, 0, 0))
        draw = ImageDraw.Draw(char)
        draw.ellipse([25, 20, 75, 70], fill=(255, 223, 196, 255))  # head
        draw.rectangle([30, 70, 70, 180], fill=(0, 120, 200, 255))   # body
        char.save(idle_path)
        print(f"Created placeholder character idle frame: {idle_path}")
    # walk frames (two simple variations)
    for i in range(2):
        walk_path = char_dir / f"walk_{i}.png"
        if not walk_path.is_file():
            char = Image.new("RGBA", (100, 200), (0, 0, 0, 0))
            draw = ImageDraw.Draw(char)
            draw.ellipse([25, 20, 75, 70], fill=(255, 223, 196, 255))
            # simple leg movement by shifting a rectangle
            offset = -5 if i == 0 else 5
            draw.rectangle([30, 70, 70, 180 + offset], fill=(0, 120, 200, 255))
            char.save(walk_path)
            print(f"Created placeholder walk frame {i}: {walk_path}")

if __name__ == "__main__":
    create_placeholder_assets()
    # Import after assets are in place
    from scene_composer import SceneComposer

    composer = SceneComposer()
    composer.create_scene_video(
        background_name="scene1",
        character_specs=[
            {
                "character": "hero",
                "action": "walk",
                "position": (270, 150),
                "animation_speed": 2,  # slower walk
            }
        ],
        output_path="hero_scene.mp4",
        duration_seconds=4,
        fps=24,
        camera_path=None,
    )
    print("Generated video: hero_scene.mp4")
