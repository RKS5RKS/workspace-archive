#!/usr/bin/env python3
"""
Simple Character Rig System
Handles layered character composition with proper anchor points
"""
import os
import json

os.environ['HOME'] = '/home/openclaw/.openclaw/workspace/comic_series'
os.environ['XDG_CACHE_HOME'] = '/home/openclaw/.openclaw/workspace/comic_series/.cache'

from PIL import Image

BASE_DIR = "/home/openclaw/.openclaw/workspace/comic_series"
ASSETS_DIR = f"{BASE_DIR}/assets"
OUTPUT_DIR = f"{BASE_DIR}/assets/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

class BodyPart:
    """A single body part with anchor point"""
    def __init__(self, name, image_path, anchor_x, anchor_y):
        self.name = name
        self.anchor_x = anchor_x  # Where this part connects to parent
        self.anchor_y = anchor_y
        if os.path.exists(image_path):
            self.image = Image.open(image_path).convert("RGBA")
            self.width = self.image.width
            self.height = self.image.height
        else:
            self.image = None
            self.width = 0
            self.height = 0
    
    def get_offset_position(self, parent_x, parent_y):
        """Get position to paste this part relative to parent anchor"""
        return (parent_x - self.anchor_x, parent_y - self.anchor_y)

class Rig:
    """
    Character rig with hierarchical body parts
    Layer order matters for rendering (back to front)
    """
    def __init__(self, name):
        self.name = name
        self.parts = {}
        self.canvas_size = (1280, 720)
        self.root_position = (640, 200)  # Hip center position
        
        # Define layer order (back to front)
        self.layer_order = [
            'left_leg', 'right_leg',  # Back layer
            'torso',  # Middle
            'head', 'left_arm', 'right_arm'  # Front
        ]
    
    def add_part(self, part_name, image_path, anchor_x, anchor_y):
        """Add a body part with its anchor point"""
        self.parts[part_name] = BodyPart(part_name, image_path, anchor_x, anchor_y)
    
    def set_pose(self, pose_config):
        """
        Set pose by updating part positions relative to root
        pose_config: dict of part_name -> (offset_x, offset_y) from default position
        """
        self.pose = pose_config
    
    def render(self, output_path=None):
        """Render the character at current pose"""
        canvas = Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))
        
        # Root position (hip center)
        root_x, root_y = self.root_position
        
        # Default positions for each part (where they attach)
        default_positions = {
            'left_leg': (root_x - 30, root_y + 50),
            'right_leg': (root_x + 30, root_y + 50),
            'torso': (root_x, root_y),
            'head': (root_x, root_y - 80),
            'left_arm': (root_x - 60, root_y - 40),
            'right_arm': (root_x + 60, root_y - 40),
        }
        
        # Apply pose offsets
        for part_name in self.layer_order:
            if part_name not in self.parts:
                continue
            
            part = self.parts[part_name]
            if part.image is None:
                continue
            
            # Get default position
            base_x, base_y = default_positions.get(part_name, (root_x, root_y))
            
            # Apply pose offset if defined
            offset_x, offset_y = self.pose.get(part_name, (0, 0))
            
            # Calculate final position
            final_x = base_x + offset_x
            final_y = base_y + offset_y
            
            # Paste part (use alpha channel as mask)
            canvas.paste(part.image, (final_x, final_y), part.image)
        
        if output_path:
            canvas.save(output_path)
        
        return canvas

# Pre-defined poses
POSES = {
    "standing": {
        'left_leg': (0, 0),
        'right_leg': (0, 0),
        'torso': (0, 0),
        'head': (0, 0),
        'left_arm': (0, 0),
        'right_arm': (0, 0),
    },
    "arms_up": {
        'left_leg': (0, 0),
        'right_leg': (0, 0),
        'torso': (0, 0),
        'head': (0, 0),
        'left_arm': (0, -80),
        'right_arm': (0, -80),
    },
    "arms_crossed": {
        'left_leg': (0, 0),
        'right_leg': (0, 0),
        'torso': (0, 0),
        'head': (0, 0),
        'left_arm': (40, 20),
        'right_arm': (-40, 20),
    },
    "walking": {
        'left_leg': (-20, 0),
        'right_leg': (20, 0),
        'torso': (0, 5),
        'head': (0, 0),
        'left_arm': (30, 0),
        'right_arm': (-30, 0),
    },
    "punching": {
        'left_leg': (0, 0),
        'right_leg': (0, 0),
        'torso': (10, 0),
        'head': (5, 0),
        'left_arm': (0, 0),
        'right_arm': (100, 0),  # Extend right arm
    },
    "crouching": {
        'left_leg': (0, 50),
        'right_leg': (0, 50),
        'torso': (0, 50),
        'head': (0, 50),
        'left_arm': (0, 30),
        'right_arm': (0, 30),
    },
    "jumping": {
        'left_leg': (-30, -50),
        'right_leg': (30, -30),
        'torso': (0, -30),
        'head': (0, -30),
        'left_arm': (-30, -30),
        'right_arm': (30, -30),
    },
}

def create_nomark_rig():
    """Create the Nomark character rig"""
    rig = Rig("nomark")
    
    # Add body parts with anchor points
    # Anchor points are where each part connects to its parent
    # For legs: anchor at top (hip connection)
    # For torso: anchor at top center (neck connection)  
    # For arms: anchor at top (shoulder connection)
    # For head: anchor at bottom (neck connection)
    
    # Note: You'll need transparent PNGs for these
    # The paths would be from the processed assets
    base_path = f"{ASSETS_DIR}/characters/nomark/poses"
    
    # These are placeholder - we'll update after processing
    rig.add_part('left_leg', f"{base_path}/leg_left.png", 20, 0)
    rig.add_part('right_leg', f"{base_path}/leg_right.png", 20, 0)
    rig.add_part('torso', f"{base_path}/torso.png", 50, 0)
    rig.add_part('head', f"{base_path}/head.png", 40, 60)
    rig.add_part('left_arm', f"{base_path}/arm_left.png", 10, 0)
    rig.add_part('right_arm', f"{base_path}/arm_right.png", 10, 0)
    
    return rig

def test_rig():
    """Test the rig system"""
    print("Testing Rig System...")
    
    # Create a test rig with colored rectangles
    rig = Rig("test")
    
    # Create simple colored parts for testing
    for part_name in ['left_leg', 'right_leg', 'torso', 'head', 'left_arm', 'right_arm']:
        # Create a colored rectangle as placeholder
        img = Image.new('RGBA', (100, 100), (200, 200, 200, 255))
        # Draw a simple shape
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([10, 10, 90, 90], fill=(100, 150, 200, 255))
        
        # Save as test part
        test_path = f"{OUTPUT_DIR}/test_{part_name}.png"
        img.save(test_path)
        
        # Add to rig with anchor points
        if 'leg' in part_name:
            rig.add_part(part_name, test_path, 50, 0)  # Top center anchor
        elif part_name == 'torso':
            rig.add_part(part_name, test_path, 50, 50)  # Top center
        elif part_name == 'head':
            rig.add_part(part_name, test_path, 50, 80)  # Bottom center
        else:
            rig.add_part(part_name, test_path, 10, 0)  # Top corner
    
    # Test each pose
    for pose_name, pose_config in POSES.items():
        rig.set_pose(pose_config)
        output = f"{OUTPUT_DIR}/rig_{pose_name}.png"
        rig.render(output)
        print(f"  ✅ {pose_name}: {output}")
    
    print("\nRig test complete!")

if __name__ == "__main__":
    test_rig()