# generate_detailed_parts.py
"""Generate more detailed character parts using Pillow (PIL).

The script creates simple yet more expressive geometric shapes for head, torso,
arms, legs and basic facial expressions. It outputs PNG files into the
`parts_detailed` folders for each character type (nomark, ally, villain).

The generated assets are minimalist – using rectangles, ellipses and polygons –
but include:
- Head shapes with chin and simple facial features
- Torso with shoulders
- Arms and legs with upper/lower segments and hands/feet
- A few expression variants (eyes and mouth)
- Multiple skin tones for diversity

Running the script requires Pillow (`pip install pillow`).
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw

# Configuration ---------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[3]  # workspace root
CHAR_TYPES = ["nomark", "ally", "villain"]
OUTPUT_SUBDIR = "parts_detailed"

# Image size for each part (width, height)
SIZE = {
    "head": (80, 80),
    "torso": (80, 100),
    "upper_arm": (20, 40),
    "lower_arm": (20, 40),
    "hand": (30, 30),
    "upper_leg": (20, 45),
    "lower_leg": (20, 45),
    "foot": (35, 25),
}

# Simple skin tone palette (RGB)
SKIN_TONES = [
    (255, 224, 189),  # light
    (224, 172, 105),  # medium‑light
    (198, 134, 66),   # medium
    (141, 85, 36),    # dark
]

# Helper to ensure output folder exists
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Drawing functions – each returns a PIL Image

def draw_head(color, expression="neutral"):
    """Draw a head with optional expression.
    expression: 'neutral', 'smile', 'frown'
    """
    w, h = SIZE["head"]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Head oval with a slight chin
    draw.ellipse([(5, 0), (w-5, h-20)], fill=color)
    # Chin triangle
    chin = [(w//2-10, h-20), (w//2+10, h-20), (w//2, h)]
    draw.polygon(chin, fill=color)
    # Eyes
    eye_radius = 5
    left_eye = (w//3 - eye_radius, h//3)
    right_eye = (2*w//3 - eye_radius, h//3)
    draw.ellipse([left_eye, (left_eye[0]+2*eye_radius, left_eye[1]+2*eye_radius)], fill="black")
    draw.ellipse([right_eye, (right_eye[0]+2*eye_radius, right_eye[1]+2*eye_radius)], fill="black")
    # Mouth
    if expression == "smile":
        draw.arc([(w//3, h//2), (2*w//3, h//2+20)], start=0, end=180, fill="black", width=2)
    elif expression == "frown":
        draw.arc([(w//3, h//2+10), (2*w//3, h//2+30)], start=180, end=360, fill="black", width=2)
    else:  # neutral
        draw.line([(w//3, h//2+10), (2*w//3, h//2+10)], fill="black", width=2)
    return img


def draw_torso(color):
    w, h = SIZE["torso"]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Simple rectangle torso with rounded top (shoulder area)
    draw.rectangle([(0, h//4), (w, h)], fill=color)
    draw.rounded_rectangle([(0, 0), (w, h//2)], radius=15, fill=color)
    return img


def draw_limb(part, color):
    w, h = SIZE[part]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (w, h)], fill=color)
    return img


def draw_hand(color):
    w, h = SIZE["hand"]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Simple oval hand
    draw.ellipse([(0, 0), (w, h)], fill=color)
    return img


def draw_foot(color):
    w, h = SIZE["foot"]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Rounded rectangle foot
    draw.rounded_rectangle([(0, 0), (w, h)], radius=5, fill=color)
    return img

# ---------------------------------------------------------------------------

def save_part(img: Image.Image, base_path: Path, name: str, tone_index: int):
    # Include tone index in filename to avoid overwriting when multiple tones are generated
    filename = f"{name}_tone{tone_index}.png"
    img.save(base_path / filename)


def generate_for_type(char_type: str):
    out_dir = BASE_DIR / "characters" / char_type / OUTPUT_SUBDIR
    ensure_dir(out_dir)
    for i, tone in enumerate(SKIN_TONES):
        # Heads with three expressions
        for expr in ["neutral", "smile", "frown"]:
            head = draw_head(tone, expression=expr)
            save_part(head, out_dir, f"head_{expr}", i)
        # Torso
        torso = draw_torso(tone)
        save_part(torso, out_dir, "torso", i)
        # Arms & legs (upper/lower, hands/feet)
        for part in ["upper_arm", "lower_arm", "hand", "upper_leg", "lower_leg", "foot"]:
            img = draw_limb(part, tone) if part != "hand" and part != "foot" else (draw_hand(tone) if part == "hand" else draw_foot(tone))
            save_part(img, out_dir, part, i)

def main():
    for ct in CHAR_TYPES:
        generate_for_type(ct)
    print("Generation complete.")

if __name__ == "__main__":
    main()
